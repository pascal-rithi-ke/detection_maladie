#!/bin/bash

# Specify the URL for Python 3.11.7 source
PYTHON_VERSION="3.11.7"
PYTHON_INSTALLER_URL="https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz"

# Specify the path to download the installer
PYTHON_INSTALLER_PATH="/tmp/Python-$PYTHON_VERSION.tgz"

# Specify the installation directory
PYTHON_INSTALL_DIR="$HOME/python-$PYTHON_VERSION"

# Download Python 3.11.7 source if it's not already downloaded
if [ ! -f "$PYTHON_INSTALLER_PATH" ]; then
    echo "Downloading Python $PYTHON_VERSION source..."
    curl -o "$PYTHON_INSTALLER_PATH" "$PYTHON_INSTALLER_URL"
fi

# Extract the installer and install Python 3.11.7 if it's not already installed
if [ ! -d "$PYTHON_INSTALL_DIR" ]; then
    echo "Extracting and installing Python $PYTHON_VERSION..."
    tar -xzf "$PYTHON_INSTALLER_PATH" -C /tmp
    cd /tmp/Python-$PYTHON_VERSION
    ./configure --prefix="$PYTHON_INSTALL_DIR"
    make
    make install
fi

# Add the newly installed Python to the PATH
export PATH="$PYTHON_INSTALL_DIR/bin:$PATH"

# Create a Python virtual environment using the installed Python 3.11.7
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete with Python $PYTHON_VERSION."
