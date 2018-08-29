#!/usr/bin/python3
from subprocess import call
from sys import argv
import json

form = ""
#enum types
try:
    with open(".pycommit.json", 'r') as f:
        data = json.loads(f.read())
except FileNotFoundError:
    inputs = {
        "type": "Type (Bug/Feature/Documentation/Etc): ",
        "id": "ID: ",
        "subject": "Subject: ",
        "reviewer": "Reviewer: ",
        "description": "Description: "
    }
    enum = {"test":["1", "2"]}
    fixed = {}
    multiline = ["description"]
    optional = ["description"]
    form = "[<type> - <id>] <subject>\nRev: <reviewer>\n\n<description>"
finally:


outputs = {k: "" if k not in multiline else [] for k in inputs.keys()}
outputs.update(fixed)

def prettify(out):
    p = form
    for k in multiline:
        out[k] = "\n".join(out[k])

    for k, v in out.items():
        p = p.replace("<" + k + ">", v)
    return p

while True:
    for k, v in inputs.items():
        if k in multiline:
            print("Type <END> to complete paragraph.")
            val = input(("(optional) " if k in optional else "") + v).strip()
            if val == "" and k in optional:
                continue
            while val != "<END>":
                outputs[k].append(val)
                val = input().strip()
        else:
            val = input(("(optional) " if k in optional else "") + v).strip()
            while val.strip() == "" and k not in optional:
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
