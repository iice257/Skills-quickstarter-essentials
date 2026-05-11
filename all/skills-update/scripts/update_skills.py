#!/usr/bin/env python3
"""Check and update installed Codex skills from known GitHub sources."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile

DEFAULT_REF = "main"
OPENAI_SKILLS_REPO = "openai/skills"
CONFIG_DIR_NAME = ".skills-update"
CONFIG_FILE_NAME = "sources.json"
STATE_FILE_NAME = "state.json"
METADATA_FILE_NAME = ".skills-update.json"

EXCLUDED_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
    "Thumbs.db",
    METADATA_FILE_NAME,
}


class UpdateError(Exception):
    """Raised for expected updater failures."""


@dataclass(frozen=True)
class SkillSource:
    skill: str
    repo: str
    path: str
    ref: str = DEFAULT_REF
    source_kind: str = "configured"

    def label(self) -> str:
        path = self.path or "."
        return f"{self.repo}:{path}@{self.ref}"


@dataclass
class ReportEntry:
    skill: str
    status: str
    source: str = ""
    detail: str = ""
    backup: str = ""
    old_digest: str = ""
    new_digest: str = ""


class RepoCache:
    def __init__(self) -> None:
        self._tmp_root = Path(tempfile.mkdtemp(prefix="skills-update-"))
        self._repos: dict[tuple[str, str], Path] = {}

    def close(self) -> None:
        shutil.rmtree(self._tmp_root, ignore_errors=True)

    def get(self, repo: str, ref: str) -> Path:
        key = (repo, ref)
        if key not in self._repos:
            self._repos[key] = self._download(repo, ref)
        return self._repos[key]

    def _download(self, repo: str, ref: str) -> Path:
        owner, name = split_repo(repo)
        quoted_ref = urllib.parse.quote(ref, safe="")
        zip_url = f"https://codeload.github.com/{owner}/{name}/zip/{quoted_ref}"
        target = self._tmp_root / safe_segment(f"{owner}-{name}-{ref}")
        target.mkdir(parents=True, exist_ok=True)
        zip_path = target / "repo.zip"
        try:
            zip_path.write_bytes(github_request(zip_url))
        except urllib.error.HTTPError as exc:
            raise UpdateError(f"download failed for {repo}@{ref}: HTTP {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise UpdateError(f"download failed for {repo}@{ref}: {exc.reason}") from exc

        with zipfile.ZipFile(zip_path, "r") as zip_file:
            safe_extract_zip(zip_file, target)
            roots = {name.split("/")[0] for name in zip_file.namelist() if name}
        if len(roots) != 1:
            raise UpdateError(f"unexpected archive layout for {repo}@{ref}")
        return target / next(iter(roots))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def default_skills_dir() -> Path:
    return codex_home() / "skills"


def state_dir(skills_dir: Path) -> Path:
    return skills_dir / CONFIG_DIR_NAME


def state_path(skills_dir: Path) -> Path:
    return state_dir(skills_dir) / STATE_FILE_NAME


def config_path(skills_dir: Path) -> Path:
    return state_dir(skills_dir) / CONFIG_FILE_NAME


def read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise UpdateError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise UpdateError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def github_request(url: str) -> bytes:
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "codex-skills-update")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def safe_extract_zip(zip_file: zipfile.ZipFile, dest_dir: Path) -> None:
    dest_root = dest_dir.resolve()
    for info in zip_file.infolist():
        extracted = (dest_dir / info.filename).resolve()
        if extracted == dest_root or dest_root in extracted.parents:
            continue
        raise UpdateError("archive contains files outside the destination")
    zip_file.extractall(dest_dir)


def safe_segment(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "repo"


def split_repo(repo: str) -> tuple[str, str]:
    parts = normalize_repo(repo).split("/")
    if len(parts) != 2:
        raise UpdateError(f"invalid GitHub repo: {repo}")
    return parts[0], parts[1]


def normalize_repo(repo: str) -> str:
    raw = repo.strip()
    if raw.startswith("https://github.com/"):
        raw = raw[len("https://github.com/") :]
    elif raw.startswith("http://github.com/"):
        raw = raw[len("http://github.com/") :]
    elif raw.startswith("git@github.com:"):
        raw = raw[len("git@github.com:") :]
    raw = raw.removesuffix(".git").strip("/")
    parts = [part for part in raw.split("/") if part]
    if len(parts) < 2:
        raise UpdateError(f"invalid GitHub repo: {repo}")
    return f"{parts[0]}/{parts[1]}"


def parse_github_url(value: str) -> tuple[str, str, str]:
    parsed = urllib.parse.urlparse(value)
    if parsed.netloc.lower() != "github.com":
        raise UpdateError(f"only github.com URLs are supported: {value}")
    parts = [urllib.parse.unquote(part) for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise UpdateError(f"invalid GitHub URL: {value}")
    repo = normalize_repo("/".join(parts[:2]))
    ref = DEFAULT_REF
    path = ""
    if len(parts) > 2:
        if parts[2] not in {"tree", "blob"} or len(parts) < 5:
            raise UpdateError(f"expected GitHub tree URL with a skill path: {value}")
        ref = parts[3]
        path = "/".join(parts[4:])
    return repo, path, ref


def parse_source_value(skill: str, value: object, source_kind: str) -> SkillSource:
    if isinstance(value, dict):
        repo = value.get("repo")
        path = value.get("path")
        ref = value.get("ref", DEFAULT_REF)
        if not isinstance(repo, str) or not isinstance(path, str):
            raise UpdateError(f"source for {skill} needs string repo and path fields")
        if not isinstance(ref, str) or not ref:
            raise UpdateError(f"source for {skill} has invalid ref")
        return SkillSource(skill, normalize_repo(repo), normalize_path(path), ref, source_kind)

    if not isinstance(value, str):
        raise UpdateError(f"source for {skill} must be a string or object")

    raw = value.strip()
    if raw.startswith("https://github.com/") or raw.startswith("http://github.com/"):
        repo, path, ref = parse_github_url(raw)
        return SkillSource(skill, repo, normalize_path(path), ref, source_kind)

    if ":" not in raw:
        raise UpdateError(
            f"source for {skill} must look like owner/repo:path@ref or a GitHub tree URL"
        )
    repo_part, path_part = raw.split(":", 1)
    ref = DEFAULT_REF
    if "@" in path_part:
        path_part, ref = path_part.rsplit("@", 1)
    return SkillSource(
        skill=skill,
        repo=normalize_repo(repo_part),
        path=normalize_path(path_part),
        ref=ref or DEFAULT_REF,
        source_kind=source_kind,
    )


def normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/").strip("/")
    if normalized in {"", "."}:
        return "."
    if normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise UpdateError(f"source path escapes repository: {path}")
    return normalized


def parse_cli_sources(values: list[str]) -> dict[str, SkillSource]:
    sources: dict[str, SkillSource] = {}
    for item in values:
        if "=" not in item:
            raise UpdateError(f"--source must look like skill=owner/repo:path@ref: {item}")
        skill, value = item.split("=", 1)
        skill = skill.strip()
        if not skill:
            raise UpdateError(f"--source has an empty skill name: {item}")
        sources[skill] = parse_source_value(skill, value, "cli")
    return sources


def load_config_sources(skills_dir: Path, explicit_config: Path | None) -> dict[str, SkillSource]:
    path = explicit_config or config_path(skills_dir)
    data = read_json(path)
    raw_sources = data.get("skills", data)
    if not isinstance(raw_sources, dict):
        raise UpdateError(f"{path} must contain an object or a skills object")
    sources: dict[str, SkillSource] = {}
    for skill, raw in raw_sources.items():
        if not isinstance(skill, str):
            raise UpdateError(f"{path} contains a non-string skill key")
        if skill in {"defaults", "version"}:
            continue
        sources[skill] = parse_source_value(skill, raw, "config")
    return sources


def load_metadata_source(skill_name: str, skill_dir: Path) -> SkillSource | None:
    metadata = skill_dir / METADATA_FILE_NAME
    if not metadata.is_file():
        return None
    data = read_json(metadata)
    return parse_source_value(skill_name, data, "metadata")


def git_source(skill_name: str, skill_dir: Path) -> SkillSource | None:
    if not (skill_dir / ".git").exists():
        return None
    try:
        remote = run_git(skill_dir, ["remote", "get-url", "origin"]).strip()
    except UpdateError:
        return None
    try:
        branch = run_git(skill_dir, ["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    except UpdateError:
        branch = DEFAULT_REF
    if branch == "HEAD":
        branch = DEFAULT_REF
    return SkillSource(skill_name, normalize_repo(remote), ".", branch, "git")


def run_git(cwd: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise UpdateError(result.stderr.strip() or "git command failed")
    return result.stdout


def list_skill_dirs(skills_dir: Path, include_system: bool, only: set[str]) -> list[tuple[str, Path]]:
    if not skills_dir.is_dir():
        raise UpdateError(f"skills directory not found: {skills_dir}")
    found: list[tuple[str, Path]] = []
    for child in sorted(skills_dir.iterdir(), key=lambda path: path.name.lower()):
        if not child.is_dir():
            continue
        if child.name == CONFIG_DIR_NAME:
            continue
        if child.name == ".system":
            if include_system:
                for system_child in sorted(child.iterdir(), key=lambda path: path.name.lower()):
                    if system_child.is_dir() and (system_child / "SKILL.md").is_file():
                        skill_name = system_child.name
                        if not only or skill_name in only:
                            found.append((skill_name, system_child))
            continue
        if child.name.startswith("."):
            continue
        if not (child / "SKILL.md").is_file():
            continue
        if only and child.name not in only:
            continue
        found.append((child.name, child))
    missing = only - {name for name, _ in found}
    if missing:
        raise UpdateError(f"requested skill(s) not installed: {', '.join(sorted(missing))}")
    return found


def source_dir(repo_root: Path, source: SkillSource) -> Path:
    if source.path == ".":
        return repo_root
    return repo_root / Path(*source.path.split("/"))


def validate_skill_source(path: Path, source: SkillSource) -> None:
    if not path.is_dir():
        raise UpdateError(f"source path not found: {source.label()}")
    if not (path / "SKILL.md").is_file():
        raise UpdateError(f"source path has no SKILL.md: {source.label()}")


def infer_openai_source(skill_name: str, cache: RepoCache) -> SkillSource | None:
    root = cache.get(OPENAI_SKILLS_REPO, DEFAULT_REF)
    for base in ("skills/.curated", "skills/.experimental"):
        candidate = root / Path(*base.split("/")) / skill_name
        if (candidate / "SKILL.md").is_file():
            return SkillSource(skill_name, OPENAI_SKILLS_REPO, f"{base}/{skill_name}", DEFAULT_REF, "openai")
    return None


def resolve_source(
    skill_name: str,
    skill_dir: Path,
    cli_sources: dict[str, SkillSource],
    config_sources: dict[str, SkillSource],
    cache: RepoCache,
    infer_openai: bool,
) -> SkillSource | None:
    if skill_name in cli_sources:
        return cli_sources[skill_name]
    metadata_source = load_metadata_source(skill_name, skill_dir)
    if metadata_source:
        return metadata_source
    if skill_name in config_sources:
        return config_sources[skill_name]
    git_remote_source = git_source(skill_name, skill_dir)
    if git_remote_source:
        return git_remote_source
    if infer_openai:
        return infer_openai_source(skill_name, cache)
    return None


def should_skip(name: str) -> bool:
    return name in EXCLUDED_NAMES or name.endswith(".pyc") or name.endswith(".pyo")


def digest_dir(path: Path) -> str:
    digest = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if not should_skip(d))
        rel_root = Path(root).relative_to(path)
        for file_name in sorted(files):
            if should_skip(file_name):
                continue
            file_path = Path(root) / file_name
            if not file_path.is_file():
                continue
            rel = (rel_root / file_name).as_posix()
            digest.update(rel.encode("utf-8"))
            digest.update(b"\0")
            digest.update(file_path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def copy_ignore(_dir: str, names: list[str]) -> set[str]:
    return {name for name in names if should_skip(name)}


def backup_path(skills_dir: Path, skill_name: str) -> Path:
    backup_root = state_dir(skills_dir) / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = backup_root / f"{safe_segment(skill_name)}-{stamp}"
    candidate = base
    index = 2
    while candidate.exists():
        candidate = Path(f"{base}-{index}")
        index += 1
    return candidate


def write_installed_metadata(
    dest_dir: Path,
    source: SkillSource,
    old_digest: str,
    new_digest: str,
) -> None:
    write_json(
        dest_dir / METADATA_FILE_NAME,
        {
            "repo": source.repo,
            "path": source.path,
            "ref": source.ref,
            "source_kind": source.source_kind,
            "updated_at": now_iso(),
            "previous_digest": old_digest,
            "installed_digest": new_digest,
        },
    )


def apply_update(skills_dir: Path, skill_name: str, skill_dir: Path, remote_dir: Path, source: SkillSource, old_digest: str, new_digest: str) -> str:
    state_dir(skills_dir).mkdir(parents=True, exist_ok=True)
    staging_parent = Path(tempfile.mkdtemp(prefix=f"{safe_segment(skill_name)}-", dir=state_dir(skills_dir)))
    staged_skill = staging_parent / skill_name
    backup = backup_path(skills_dir, skill_name)
    try:
        shutil.copytree(remote_dir, staged_skill, ignore=copy_ignore)
        write_installed_metadata(staged_skill, source, old_digest, new_digest)
        shutil.move(str(skill_dir), str(backup))
        try:
            shutil.move(str(staged_skill), str(skill_dir))
        except Exception:
            if not skill_dir.exists() and backup.exists():
                shutil.move(str(backup), str(skill_dir))
            raise
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)
    return str(backup)


def check_skill(
    skills_dir: Path,
    skill_name: str,
    skill_dir: Path,
    source: SkillSource,
    cache: RepoCache,
    apply: bool,
) -> ReportEntry:
    try:
        repo_root = cache.get(source.repo, source.ref)
        remote_dir = source_dir(repo_root, source)
        validate_skill_source(remote_dir, source)
        old_digest = digest_dir(skill_dir)
        new_digest = digest_dir(remote_dir)
        if old_digest == new_digest:
            return ReportEntry(skill_name, "current", source.label(), old_digest=old_digest, new_digest=new_digest)
        if not apply:
            return ReportEntry(
                skill=skill_name,
                status="update_available",
                source=source.label(),
                detail="run with --apply to update",
                old_digest=old_digest,
                new_digest=new_digest,
            )
        backup = apply_update(skills_dir, skill_name, skill_dir, remote_dir, source, old_digest, new_digest)
        return ReportEntry(skill_name, "updated", source.label(), "backup created", backup, old_digest, new_digest)
    except UpdateError as exc:
        detail = str(exc)
        status = "source_missing" if detail.startswith("source path ") else "error"
        return ReportEntry(skill_name, status, source.label(), detail)
    except Exception as exc:
        return ReportEntry(skill_name, "error", source.label(), str(exc))


def update_run_state(skills_dir: Path, entries: list[ReportEntry], apply: bool) -> None:
    state = read_json(state_path(skills_dir))
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.status] = counts.get(entry.status, 0) + 1
    state["last_run_at"] = now_iso()
    state["last_run_apply"] = apply
    state["last_run_counts"] = counts
    write_json(state_path(skills_dir), state)


def print_text_report(entries: list[ReportEntry]) -> None:
    if not entries:
        print("No installed skills found.")
        return
    widths = {
        "skill": max(len("skill"), *(len(entry.skill) for entry in entries)),
        "status": max(len("status"), *(len(entry.status) for entry in entries)),
        "source": max(len("source"), *(min(len(entry.source), 72) for entry in entries)),
    }
    print(f"{'skill':<{widths['skill']}}  {'status':<{widths['status']}}  {'source':<{widths['source']}}  detail")
    print(f"{'-' * widths['skill']}  {'-' * widths['status']}  {'-' * widths['source']}  ------")
    for entry in entries:
        source = entry.source
        if len(source) > 72:
            source = source[:69] + "..."
        print(f"{entry.skill:<{widths['skill']}}  {entry.status:<{widths['status']}}  {source:<{widths['source']}}  {entry.detail}")
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.status] = counts.get(entry.status, 0) + 1
    summary = ", ".join(f"{status}: {count}" for status, count in sorted(counts.items()))
    print(f"\nSummary: {summary}")


def first_run_status(skills_dir: Path) -> int:
    state = read_json(state_path(skills_dir))
    prompted = bool(state.get("first_run_prompted"))
    payload = {
        "first_run_required": not prompted,
        "automatic_updates": state.get("automatic_updates"),
        "state_path": str(state_path(skills_dir)),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def mark_first_run(skills_dir: Path, choice: str) -> int:
    state = read_json(state_path(skills_dir))
    state["first_run_prompted"] = True
    state["first_run_prompted_at"] = now_iso()
    state["automatic_updates"] = choice
    write_json(state_path(skills_dir), state)
    print(f"Marked first-run automation choice: {choice}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check and update installed Codex skills.")
    parser.add_argument("--skills-dir", type=Path, default=default_skills_dir(), help="Installed skills directory.")
    parser.add_argument("--config", type=Path, help="Source config JSON path.")
    parser.add_argument("--source", action="append", default=[], help='Source override, e.g. "my-skill=owner/repo:skills/my-skill@main".')
    parser.add_argument("--only", action="append", default=[], help="Only check this installed skill. Repeatable.")
    parser.add_argument("--apply", action="store_true", help="Replace installed skills that have updates.")
    parser.add_argument("--include-system", action="store_true", help="Also scan skills under .system.")
    parser.add_argument("--no-infer-openai", action="store_true", help="Do not infer openai/skills curated or experimental sources.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON report.")
    parser.add_argument("--first-run-status", action="store_true", help="Print whether the automation prompt is still required.")
    parser.add_argument("--mark-first-run", choices=["enabled", "declined"], help="Record the user's first-run automation choice.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    skills_dir = args.skills_dir.expanduser().resolve()
    try:
        if args.first_run_status:
            return first_run_status(skills_dir)
        if args.mark_first_run:
            return mark_first_run(skills_dir, args.mark_first_run)

        only = set(args.only)
        cli_sources = parse_cli_sources(args.source)
        config_sources = load_config_sources(skills_dir, args.config)
        installed = list_skill_dirs(skills_dir, args.include_system, only)
        cache = RepoCache()
        entries: list[ReportEntry] = []
        try:
            for skill_name, skill_dir in installed:
                try:
                    source = resolve_source(
                        skill_name,
                        skill_dir,
                        cli_sources,
                        config_sources,
                        cache,
                        infer_openai=not args.no_infer_openai,
                    )
                    if not source:
                        entries.append(ReportEntry(skill_name, "untracked", detail="add source metadata or config"))
                        continue
                    entries.append(check_skill(skills_dir, skill_name, skill_dir, source, cache, args.apply))
                except Exception as exc:
                    entries.append(ReportEntry(skill_name, "error", detail=str(exc)))
        finally:
            cache.close()

        update_run_state(skills_dir, entries, args.apply)
        if args.json:
            print(json.dumps([asdict(entry) for entry in entries], indent=2, sort_keys=True))
        else:
            print_text_report(entries)
        return 1 if any(entry.status == "error" for entry in entries) else 0
    except UpdateError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
