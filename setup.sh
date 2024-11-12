#!/bin/bash

clear

echo "====================================="
echo "    OxPhish Setup Script"
echo "====================================="

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] This script must be run as root or with sudo."
  exit 1
fi

echo "[+] Updating package list..."
apt update -y

echo "[+] Checking for Python and pip..."
if ! command -v python &> /dev/null; then
  echo "[+] Python not found, installing..."
  apt install python -y
else
  echo "[+] Python is already installed."
fi

if ! command -v pip &> /dev/null; then
  echo "[+] pip not found, installing..."
  apt install python-pip -y
else
  echo "[+] pip is already installed."
fi

echo "[+] Installing required Python packages..."
pip install -r requirements.txt

echo "[+] Checking for Git..."
if ! command -v git &> /dev/null; then
  echo "[+] Git not found, installing..."
  apt install git -y
else
  echo "[+] Git is already installed."
fi

if [ ! -d "OxPhish" ]; then
  echo "[+] Cloning the OxPhish repository..."
  git clone https://github.com/Oxeser/OxPhish.git
else
  echo "[+] OxPhish repository already exists."
fi

chmod +x setup.sh

echo "[+] Running OxPhish..."
cd OxPhish
python main.py

echo "[+] Setup completed!"
echo "[+] If you want to update, run the script again or use: git pull"
