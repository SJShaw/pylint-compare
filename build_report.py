#!/usr/bin/env python3

import json
import sys

default = json.load(open(sys.argv[1]))
pull = json.load(open(sys.argv[2]))

result = {}
for key, val in default.items():
    new = pull.get(key, 0)
    diff = new - val
    if diff:
        result[key] = diff

print("### Pylint count changes")
if result:
    print("|Category|Count|Proportional|")
    print("|:---|---:|---:|")
    for key, diff in sorted(result.items()):
        old = default.get(key, 0)
        change = "was 0"
        if old:
            change = "{:+.1f}%".format((diff / old) * 100)
        print("|**{}**|{:+}|{}|".format(key, diff, change))
else:
    print("None")
