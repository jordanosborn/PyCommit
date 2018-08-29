#!/usr/bin/python3
from subprocess import call
from sys import argv
import json

#TODO: Add formatting options within angled brackets
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
enums = c.get("enums")
form = c.get("form")

outputs = {k: "" if k not in multiline else [] for k in inputs.keys()}
outputs.update(fixed)

def pretty_enum(ls):
    s = "("
    for i, el in enumerate(ls):
        s += str(i) + ": " + str(el)
        if i + 1 == len(ls):
            s += ")"
        else:
            s += ", "
    return s

def prettify(out):
    #if any blank move surrounding newlines
    p = form
    for k in multiline:
        out[k] = "\n".join(out[k])
    for k, v in out.items():
        p = p.replace("<" + k + ">", enums[k][int(v)] if k in enums else v)
    return p

def in_enum_range(i, e):
    return i in list(map(lambda s: str(s), range(0, len(e))))

while True:
    for k, v in inputs.items():
        isOptional = k in optional
        isEnum = k in enums
        if k in multiline:
            print("Type <END> to complete paragraph.")
            val = input(("(optional) " if isOptional else "") + v).strip()
            if val == "" and isOptional:
                continue
            while val != "<END>":
                outputs[k].append(val)
                val = input().strip()
        else:
            notInRange = False
            val = input(("(optional) " if isOptional else "") + v).strip()
            if isEnum:
                notInRange = not in_enum_range(val, enums[k])
                if notInRange and not (val == "" and isOptional):
                    print("Choose one of " + pretty_enum(enums[k]))
            while ((val.strip() == "" or notInRange) and not isOptional) or (val.strip() != "" and notInRange):
                    val = input(("(Choose-Valid-Enum)" +(" (optional) " if isOptional else "") if notInRange else "(Non-Empty) ")  + v).strip()
                    if isEnum:
                        notInRange = not in_enum_range(val, enums[k])
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
