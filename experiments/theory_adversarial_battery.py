from __future__ import annotations

import json

from skill_conscious.adversarial_battery import (
    run_adversarial_battery,
    summarize_battery,
)


def main() -> None:
    results = run_adversarial_battery()
    print("THEORY_MECHANISM_ADVERSARIAL_BATTERY")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("SUMMARY")
    print(json.dumps(summarize_battery(results), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
