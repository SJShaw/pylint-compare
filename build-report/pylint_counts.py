#!/usr/bin/env python3

from io import StringIO
import json
from importlib.metadata import version
import sys

from pylint.lint import Run
from pylint.reporters.text import TextReporter

PYLINT_PARAMS = [
    "-j", "12",
]


def run_pylint(paths_to_check: list[str]) -> Run:
    output = StringIO()
    reporter = TextReporter(output=output)
    pylint_kwargs = {
        "reporter": reporter,
    }
    try:
        pylint_version = tuple(int(part) for part in version("pylint").split("."))
        if pylint_version >= (2, 5, 1):
            pylint_kwargs["exit"] = False
        else:
            pylint_kwargs["do_exit"] = False
    except Exception:
        # unknown version, default to pre-2.5.1
        pylint_kwargs["do_exit"] = False

    return Run(PYLINT_PARAMS + paths_to_check, **pylint_kwargs)


def get_summary(result: Run) -> None:
    # somewhere between 2.10 and 2.15, pylint stopped using a dictionary, so handle both cases
    if isinstance(result.linter.stats, dict):  # pylint <= 2.10
        simple = {
            "Errors": result.linter.stats["error"],
            "Convention": result.linter.stats["convention"],
            "Refactor": result.linter.stats["refactor"],
            "Warnings": result.linter.stats["warning"],
            "Syntax/Fatal errors": result.linter.stats["fatal"],
        }
    else:  # pylint >= 2.15
        simple = {
            "Errors": result.linter.stats.error,
            "Convention": result.linter.stats.convention,
            "Refactor": result.linter.stats.refactor,
            "Warnings": result.linter.stats.warning,
            "Syntax/Fatal errors": result.linter.stats.fatal,
        }
    return simple


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: no paths provided", file=sys.stderr)
        sys.exit(1)
    try:
        print(json.dumps(get_summary(run_pylint(sys.argv[1:]))))
    except ImportError as err:
        print(f"Error: {err}")
        sys.exit(1)
