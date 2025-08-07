# ThingsBoard MCP Server

MCP server for ThingsBoard REST API.
Actual implemented version of API is `v3.9.1`

## Setup environment using uv

### Windows
```
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create virtual environment
uv venv

# Activate virtual environment
.venv\Scripts\activate
```

### Linux

```
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate
```

## Add environment variables

Create .env file: `cp .env.example .env`

Set the wanted MCP server transport with `MCP_SERVER_TRANSPORT` environment variable. Default: `streamable-http`
Edit the `THINGSBOARD_*` environment variables to allow the MCP server to connect to ThingsBoard.


## Install dependencies
```
uv pip install -r pyproject.toml
```

## Run server
```
uv run src/thingsboard.py
```
