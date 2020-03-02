#!/bin/bash

# Create a virtualenv if it doesn't exist
[[ -d .venv ]] || python3 -m venv .venv || exit 1

source .venv/bin/activate || exit 1

pip3 install . || exit 1

python3 garmin-share-to-aprs.py