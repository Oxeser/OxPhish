#!/bin/bash

clear

echo "====================================="
echo "    OxPhish Setup Script"
echo "====================================="

if [ -f /data/data/com.termux/files/usr/bin/bash ]; then
  TERMUX=true
else
  TERMUX=false
fi

if [ "$TERMUX" = true ]; then
  PACKAGE_MANAGER="pkg"
  PYTHON="python"
  PIP="pip"
else
  PACKAGE_MANAGER="apt"
  PYTHON="python3"
  PIP="pip3"
fi

echo "[+] Updating package list..."
$PACKAGE_MANAGER update -y

echo "[+] Checking for Python and pip..."
if ! command -v $PYTHON &> /dev/null; then
  echo "[+] Python not found, installing..."
  $PACKAGE_MANAGER install python -y
else
  echo "[+] Python is already installed."
fi

if ! command -v $PIP &> /dev/null; then
  echo "[+] pip not found, installing..."
  $PACKAGE_MANAGER install python-pip -y
else
  echo "[+] pip is already installed."
fi

echo "[+] Installing required Python packages..."
$PIP install --user -r requirements.txt

echo "[+] Checking for Git..."
if ! command -v git &> /dev/null; then
  echo "[+] Git not found, installing..."
  $PACKAGE_MANAGER install git -y
else
  echo "[+] Git is already installed."
fi

echo "[+] Checking for OpenSSH..."
if ! command -v ssh &> /dev/null; then
  echo "[+] OpenSSH not found, installing..."
  $PACKAGE_MANAGER install openssh -y
else
  echo "[+] OpenSSH is already installed."
fi

chmod +x setup.sh

echo "[+] Running OxPhish..."
cd OxPhish
$PYTHON main.py

echo "[+] Setup completed!"
echo "[+] If you want to update, run the script again or use: git pull"
