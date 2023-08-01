#!/bin/bash

echo "Run: mypy ."
mypy .
echo ""

echo "Run: coverage run -m pytest"
coverage run -m pytest
