#!/usr/bin/env bash
# startup.sh
# ----------
# Run this ON the GCP Compute Engine VM to set everything up.
# It installs Python, copies the app into /opt/salarynet, installs the
# requirements into a virtual environment, and starts the app as a service.
#
# Usage (from inside the project folder on the VM):
#     sudo bash deploy/startup.sh

set -e  # stop if any command fails

APP_DIR=/opt/salarynet

echo "==> Installing system packages"
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip

echo "==> Copying app to ${APP_DIR}"
sudo mkdir -p "${APP_DIR}"
sudo cp -r . "${APP_DIR}"
cd "${APP_DIR}"

echo "==> Creating virtual environment and installing requirements"
sudo python3 -m venv venv
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install -r requirements.txt

echo "==> Letting the service user own the files"
sudo chown -R www-data:www-data "${APP_DIR}"

echo "==> Installing and starting the systemd service"
sudo cp deploy/salarynet.service /etc/systemd/system/salarynet.service
sudo systemctl daemon-reload
sudo systemctl enable salarynet
sudo systemctl restart salarynet

echo "==> Done! The app is running on port 8080."
echo "    Check status with:  sudo systemctl status salarynet"
