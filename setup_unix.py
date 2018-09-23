"""Install Pycommit"""

import sys
from subprocess import call

if __name__ == "__main__":
    call(["git", "pull"])
    print("Installing PyCommit.")
    with open("pycommit.py") as f:
        d = f.readlines()
    d = list(map(lambda s: s.replace("<python3_path>", sys.executable), d))
    output = "/usr/local/bin/pycommit"
    with open(output, "w") as f:
        f.writelines(d)
    call(["chmod", "+x", output])

    if len(sys.argv) > 1:
        for repo in sys.argv[1:]:
            call(["cp",".pycommit.json", repo])

    print("Installed PyCommit.")