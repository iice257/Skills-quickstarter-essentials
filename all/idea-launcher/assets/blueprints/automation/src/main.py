from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def run(input_text: str, dry_run: bool = True) -> dict:
    summary = input_text.strip() or "{{ONE_LINE_CONCEPT}}"
    return {
        "project": "{{PROJECT_NAME}}",
        "dry_run": dry_run,
        "workflow": "{{CORE_WORKFLOW}}",
        "summary": summary[:240],
        "next_action": "Replace this starter transform with the real automation action.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} automation starter")
    parser.add_argument("--input", default="{{ONE_LINE_CONCEPT}}", help="Input text for the first automation run.")
    parser.add_argument("--out", default="output/run.json", help="Output JSON path.")
    parser.add_argument("--live", action="store_true", help="Disable dry-run mode.")
    args = parser.parse_args()

    result = run(args.input, dry_run=not args.live)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
