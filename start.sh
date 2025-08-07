#!/bin/bash
uv venv --clear
source .venv/bin/activate
uv run src/thingsboard.py
