#!/bin/bash

# Create a virtualenv if it doesn't exist
[[ -d .venv ]] || python3 -m venv .venv

source .venv/bin/activate

pip3 install .

python3 garmin-share-to-aprs.py