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

print("### Issue count changes")
if result:
    for key, val in sorted(result.items()):
        print("- **%s**: %s" % (key, val))
else:
    print("None")
