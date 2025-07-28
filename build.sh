#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run our clean setup script
python setup_db.py