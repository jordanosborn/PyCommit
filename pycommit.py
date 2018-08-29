#!/usr/bin/python3
from subprocess import call
from sys import argv
import json

class config:
    def __init__(self, defaults):
        self._values = defaults
    def get(self, k):
        if k in self._values:
            return self._values[k]
    def set(self, k, v):
        if k in self._values.keys():
            self._values[k] = v

defaults = {
        "inputs": {
            "type": "Type (Bug/Feature/Documentation/Etc): ",
            "id": "ID: ",
            "subject": "Subject: ",
            "reviewer": "Reviewer: ",
            "description": "Description: "
        },
        "enums": {},
        "fixed": {},
        "multiline": ["description"],
        "optional": ["description"],
        "form": "[<type> - <id>] <subject>\nRev: <reviewer>\n\n<description>"
    }
#enum types
c = config(defaults)
try:
    with open(".pycommit.json", 'r') as f:
        data = json.loads(f.read())
except FileNotFoundError:
    print("Using default configuration")
else:
    for k, v in data.items():
        if type(c.get(k)) == type(v):
            c.set(k, v)
        else:
            print("Malformatted key (k) using defaults.")

inputs = c.get("inputs")
fixed = c.get("fixed")
multiline = c.get("multiline")
optional = c.get("optional")
form = c.get("form")

outputs = {k: "" if k not in multiline else [] for k in inputs.keys()}
outputs.update(fixed)

def prettify(out):
    #if any blank move surrounding newlines
    p = form
    for k in multiline:
        out[k] = "\n".join(out[k])
    for k, v in out.items():
        p = p.replace("<" + k + ">", v)
    return p

while True:
    for k, v in inputs.items():
        opt = k in optional
        if k in multiline:
            print("Type <END> to complete paragraph.")
            val = input(("(optional) " if opt else "") + v).strip()
            if val == "" and opt:
                continue
            while val != "<END>":
                outputs[k].append(val)
                val = input().strip()
        else:
            val = input(("(optional) " if opt else "") + v).strip()
            while val.strip() == "" and not opt:
                    val = input("(Non-Empty) " + v).strip()
            outputs[k] = val
    if input("Are you happy with this commit message (y/n)? ")[0] == 'y':
        break
p = prettify(outputs)
print("Commit message:\n{}".format(p))
if p.strip() == "":
    print("Not Committed. Commit message empty")
elif input("Are you happy with the formatted commit message (y/n)? ")[0] == 'y':
    call(["git", "commit", "-m", p])
    print("Committed")
else:
    print("Not Committed")
