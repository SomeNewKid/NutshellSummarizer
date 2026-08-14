# Nutshell Summarizer

Nutshell Summarizer is a small Python agent built with AWS Strands Agents and
deployed to AWS Bedrock AgentCore. It includes a handful of public-domain story
texts from Project Gutenberg and can summarize a known story on request.

Example:

```powershell
.\.venv\Scripts\python.exe -m nutshell_summarizer "Summarize the story about Snow White and Rose Red"
```

## Project Layout

```text
app/NutshellSummarizer/
  entrypoint.py                  # Bedrock AgentCore runtime entrypoint
  pyproject.toml                 # Minimal runtime package metadata
  nutshell_summarizer/
    __main__.py                  # python -m nutshell_summarizer
    cli.py                       # Local CLI adapter
    bedrock.py                   # AgentCore adapter
    agent.py                     # Strands Agent construction
    tools.py                     # Strands tools
    library.py                   # Story manifest and content loading
    stories/                     # Bundled Project Gutenberg story texts
agentcore/
  agentcore.json                 # AgentCore project configuration
  cdk/                           # Generated CDK deployment project
scripts/
  setup-dev.ps1                  # Restore Python and AgentCore/CDK dependencies
  check.ps1                      # Format, lint, type-check, and test
tests/
```

The application package lives under `app/NutshellSummarizer`. There is no
separate `src` package; this avoids duplicating the agent code used locally and
in AgentCore.

## Prerequisites

- Python 3.11
- Node.js 20 or later
- npm
- AWS CLI configured for an AWS identity that can use Bedrock and AgentCore
- AgentCore CLI:

```powershell
npm install -g @aws/agentcore
```

The selected Bedrock model must also be enabled for the AWS account and region.

## Setup

From the repository root:

```powershell
.\scripts\setup-dev.ps1
```

This script:

- creates or reuses the root `.venv`
- installs the Python package in editable mode with dev tools
- verifies `node`, `npm`, and `agentcore`
- restores `agentcore/cdk/node_modules` with `npm ci`
- builds the AgentCore CDK project

## Local CLI

Run the agent directly as a Python module:

```powershell
.\.venv\Scripts\python.exe -m nutshell_summarizer "Summarize the story of Iron Hans"
```

Or use the installed console script:

```powershell
.\.venv\Scripts\nutshell-summarizer.exe "Summarize the story of Iron Hans"
```

## AgentCore Local Runtime

Run through the AgentCore local development runtime:

```powershell
agentcore dev --logs
```

In another terminal:

```powershell
agentcore dev "Summarize the story about Snow White and Rose Red"
```

## Checks

After meaningful code changes:

```powershell
.\scripts\check.ps1
```

This runs Ruff formatting, Ruff linting, Pyright, and Pytest.

## Deploy

Validate the AgentCore configuration:

```powershell
agentcore validate
```

Preview deployment:

```powershell
agentcore deploy --dry-run
```

Deploy:

```powershell
agentcore deploy -y -v
```

Invoke the deployed runtime:

```powershell
agentcore invoke --runtime NutshellSummarizer "Summarize the story about Snow White and Rose Red" --stream
```

## Git Notes

Commit the AgentCore configuration and CDK source under `agentcore/`, including
`agentcore/cdk/package-lock.json`. Do not commit generated folders such as:

```text
.venv/
app/NutshellSummarizer/.venv/
agentcore/cdk/node_modules/
agentcore/cdk/cdk.out/
agentcore/cdk/dist/
agentcore/.cache/
agentcore/.cli/logs/
agentcore/.cli/traces/
```

## Cleanup

For a temporary experiment, remove deployed AgentCore resources when finished:

```powershell
agentcore remove all -y
agentcore deploy -y -v
```

Then delete any temporary IAM access keys or users created only for this project.
