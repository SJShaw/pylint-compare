#!/usr/bin/env python3

from io import StringIO
import json
from importlib.metadata import version
import sys

from pylint.lint import Run
from pylint.reporters.text import TextReporter

paths_to_check = sys.argv[1:]
pylint_params = ["-j", "12",]

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

result = Run(pylint_params + paths_to_check, **pylint_kwargs)

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
print(json.dumps(simple))
