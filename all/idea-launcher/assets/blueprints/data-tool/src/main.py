from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def summarize(rows: list[dict[str, str]]) -> dict:
    return {
        "project": "{{PROJECT_NAME}}",
        "workflow": "{{CORE_WORKFLOW}}",
        "record_count": len(rows),
        "columns": sorted(rows[0].keys()) if rows else [],
        "status": "ready",
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} data-tool starter")
    parser.add_argument("--input", default="data/fixtures/sample.csv")
    parser.add_argument("--out", default="output/report.json")
    args = parser.parse_args()

    rows = read_csv(Path(args.input))
    report = summarize(rows)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
