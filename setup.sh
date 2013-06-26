#!/bin/bash

sudo pip install docopt
git clone https://github.com/hph/mov.git
mv mov/ ~/.mov
chmod +x ~/.mov/mov.py
sudo ln -s ~/.mov/mov.py /usr/bin/mov
