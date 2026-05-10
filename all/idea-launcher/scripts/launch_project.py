#!/usr/bin/env python3
"""Generate an Idea Launcher starter project from bundled templates."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
STARTER_PACKS = ROOT / "assets" / "starter-packs"
BLUEPRINTS = ROOT / "assets" / "blueprints"

DOC_TEMPLATES = {
    "docs/SPEC.md": "SPEC.md",
    "docs/TASKS.md": "TASKS.md",
    "docs/IMPLEMENTATION-CHECKLIST.md": "IMPLEMENTATION-CHECKLIST.md",
    "docs/TEST-PLAN.md": "TEST-PLAN.md",
    "docs/DEPLOY-PLAN.md": "DEPLOY-PLAN.md",
    "docs/FIRST-BUILD-PROMPT.md": "FIRST-BUILD-PROMPT.md",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "idea-project"


def load_pack(pack_name: str) -> dict:
    path = STARTER_PACKS / f"{pack_name}.json"
    if not path.exists():
        choices = ", ".join(sorted(p.stem for p in STARTER_PACKS.glob("*.json")))
        raise SystemExit(f"Unknown starter pack '{pack_name}'. Available: {choices}")
    return json.loads(path.read_text(encoding="utf-8"))


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def starter_values(name: str, idea: str, pack: dict) -> dict[str, str]:
    project_type = pack["project_type"]
    core_workflow = pack["core_workflow"]
    stack = pack["stack"]
    non_goals = "\n".join(f"- {item}" for item in pack["default_non_goals"])
    constraints = "\n".join(f"- {item}" for item in pack["constraints"])
    return {
        "PROJECT_NAME": name,
        "PROJECT_SLUG": slugify(name),
        "ONE_LINE_CONCEPT": idea,
        "WHY_THIS_IS_WORTH_BUILDING": pack["good_side"],
        "WHY_THIS_MIGHT_FAIL_OR_SPRAWL": pack["bad_side"],
        "CORE_PROOF": pack["core_proof"],
        "V1_FEATURE": core_workflow,
        "NON_GOAL": pack["default_non_goals"][0],
        "NON_GOALS": non_goals,
        "STEP_ONE": pack["workflow_steps"][0],
        "STEP_TWO": pack["workflow_steps"][1],
        "STEP_THREE": pack["workflow_steps"][2],
        "ENTITY": pack["entity"],
        "PURPOSE": pack["entity_purpose"],
        "FIELDS": ", ".join(pack["fields"]),
        "RELATIONSHIPS": pack["relationships"],
        "OWNER": pack["owner"],
        "RISK": pack["risk"],
        "IMPACT": "medium",
        "LIKELIHOOD": "medium",
        "MITIGATION": pack["mitigation"],
        "QUESTION": pack["open_question"],
        "DECISION": f"Use the {project_type} starter pack",
        "RATIONALE": "It matches the first workflow with the least operational overhead.",
        "LATER_TASK": pack["later_task"],
        "RISKY_BEHAVIOR": pack["risk"],
        "CORE_ASSERTION": pack["core_assertion"],
        "UNIT_CHECK": pack["unit_check"],
        "TOOL": pack["test_tool"],
        "ACCEPTANCE": pack["acceptance"],
        "INTEGRATION_CHECK": pack["integration_check"],
        "E2E_CHECK": pack["e2e_check"],
        "ENV_VAR": pack["env_var"],
        "CORE_WORKFLOW": core_workflow,
        "CONSTRAINTS": constraints,
    } | stack


def write_root_files(target: Path, values: dict[str, str], pack: dict, force: bool) -> None:
    agents = f"""# AGENTS.md

## Project Commands

- Install: {pack["commands"]["install"]}
- Dev server: {pack["commands"]["dev"]}
- Build: {pack["commands"]["build"]}
- Test: {pack["commands"]["test"]}
- Lint: {pack["commands"]["lint"]}
- Deploy: {pack["commands"]["deploy"]}

## Working Rules

- Keep v1 focused on the workflow in `docs/SPEC.md`.
- Update `MEMORY.md` when durable project facts or user preferences are established.
- Do not add auth, payments, background jobs, or new services unless the spec requires them.
- Commit and push after major tasks when the workspace instructions require it.

## Verification Before Completion

- Run the test and build commands above when available.
- Manually complete the core workflow before calling the task done.
"""
    memory = f"""# Memory

- Generated with Idea Launcher from starter pack `{pack["slug"]}`.
- Initial idea: {values["ONE_LINE_CONCEPT"]}
"""
    env_example = "\n".join(f"{name}=" for name in pack["env_vars"]) + "\n"
    write_file(target / "AGENTS.md", agents, force)
    write_file(target / "MEMORY.md", memory, force)
    write_file(target / ".env.example", env_example, force)


def write_pack_files(target: Path, pack: dict, force: bool) -> None:
    for directory in pack["directories"]:
        (target / directory).mkdir(parents=True, exist_ok=True)
    for file_path, content in pack["files"].items():
        write_file(target / file_path, content.rstrip() + "\n", force)


def copy_blueprint(target: Path, pack: dict, values: dict[str, str], force: bool) -> None:
    blueprint = BLUEPRINTS / pack["slug"]
    if not blueprint.exists():
        return
    for source in blueprint.rglob("*"):
        if source.is_dir():
            continue
        relative = source.relative_to(blueprint)
        destination = target / relative
        if destination.exists() and not force:
            raise SystemExit(f"Refusing to overwrite existing file: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copy2(source, destination)
            continue
        destination.write_text(render(content, values), encoding="utf-8", newline="\n")


def build_project(args: argparse.Namespace) -> Path:
    pack = load_pack(args.type)
    name = args.name.strip()
    folder_name = args.folder or slugify(name)
    target = Path(args.out).resolve() / folder_name
    if target.exists() and any(target.iterdir()) and not args.force:
        raise SystemExit(f"Target exists and is not empty: {target}. Use --force to overwrite files.")

    values = starter_values(name, args.idea.strip(), pack)
    for output_path, template_name in DOC_TEMPLATES.items():
        template = (TEMPLATES / template_name).read_text(encoding="utf-8")
        write_file(target / output_path, render(template, values), args.force)
    write_root_files(target, values, pack, args.force)
    write_pack_files(target, pack, args.force)
    copy_blueprint(target, pack, values, args.force)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an Idea Launcher starter project.")
    parser.add_argument("--name", required=True, help="Human-readable project name.")
    parser.add_argument("--idea", required=True, help="One-line project idea.")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(p.stem for p in STARTER_PACKS.glob("*.json")),
        help="Starter pack type.",
    )
    parser.add_argument("--out", default=".", help="Output parent directory.")
    parser.add_argument("--folder", help="Optional output folder name.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files if they exist.")
    args = parser.parse_args()

    target = build_project(args)
    print(f"Created Idea Launcher starter at {target}")
    print("Next: review docs/SPEC.md, run the project commands in AGENTS.md, then run scripts/validate_placeholders.py.")


if __name__ == "__main__":
    main()
