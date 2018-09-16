#!/bin/bash

a=`which python3`
sed -i s/<python3_path>/$a/g pycommit.py
chmod +x pycommit.py
cp pycommit.py /usr/local/bin/pycommit
source ~/.bashrc
if [ $# -eq 1]
  then
    cp .pycommit.json $1/.pycommit.json
    cd $1
    nano .pycommit.json
fi
