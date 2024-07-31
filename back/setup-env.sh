#!/bin/bash

# 1. Specify the version of Python to use
PYTHON_VERSION="python3.11"

# 2. Create a Python virtual environment using Python 3.11
$PYTHON_VERSION -m venv venv

# 3. Activate the Python virtual environment
source venv/bin/activate  # Note: On Windows, use venv\Scripts\activate

# 4. Upgrade pip and install required packages
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete with Python 3.11.7."