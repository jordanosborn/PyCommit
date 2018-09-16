# PyCommit

Small script to automatically generate configurable commit messages in python

### Create standardised git messages


Create a .pycommit.json file in your git repository (see example .pycommit.json)

Add pycommit to your path (/usr/bin/ etc.) (may need to change python interpreter path in pycommit.py)

Make pycommit script executable for example by running (chmod +x pycommit.py)

Run pycommit.py in your repository when you want to commit

An interactive prompt will appear to fill out your template

If the template is satisfactory your changes will be commited automatically


### TODO:

Add more complex formatting options including format of new lines, upper/lower case operators etc

Placeholders that run commands and use stdout as their input ( list files to be commited). Run functions on inputs using eval

Add spellcheck based on locale in .pycommit.jspn 
