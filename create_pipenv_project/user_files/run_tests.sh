#!/bin/bash

mypy .
coverage run -m pytest
