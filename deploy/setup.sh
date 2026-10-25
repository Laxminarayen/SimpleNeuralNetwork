#!/usr/bin/env bash
# setup.sh
# --------
# Sets up the app on the VM: installs Python and builds the virtual
# environment with all the requirements. It does NOT start the app
# (we do that by hand, see the README).
#
# Usage (from inside the project folder on the VM):
#     bash deploy/setup.sh

set -e  # stop if any command fails

echo "==> Installing Python"
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip

echo "==> Creating virtual environment and installing requirements"
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo ""
echo "==> Done! Now start the app with:"
echo "    ./venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8080 app:app"
