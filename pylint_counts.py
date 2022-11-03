#!/usr/bin/env python3

from io import StringIO
import json
import sys

from pylint.lint import Run
from pylint.reporters.text import TextReporter

paths_to_check = sys.argv[1:]
pylint_params = ["-j", "12",]

output = StringIO()
reporter = TextReporter(output=output)
result = Run(pylint_params + paths_to_check, reporter=reporter, do_exit=False, exit=False)

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
