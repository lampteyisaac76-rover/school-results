#!/usr/bin/env bash
# Exit on error
set -o errexit

# Detect python and pip command
if [ -n "$VIRTUAL_ENV" ]; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
elif [ -d "venv" ]; then
    PYTHON_CMD="./venv/bin/python"
    PIP_CMD="./venv/bin/pip"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

# Install dependencies
$PIP_CMD install -r requirements.txt

# Collect static files
$PYTHON_CMD manage.py collectstatic --no-input

# Apply database migrations
$PYTHON_CMD manage.py migrate

# Populate standard subjects
$PYTHON_CMD manage.py populate_subjects

# Import registered students
$PYTHON_CMD manage.py import_basic9_students

# Configure admin and teacher accounts
$PYTHON_CMD manage.py setup_default_accounts
