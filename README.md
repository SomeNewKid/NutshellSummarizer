# Nutshell Summarizer

Nutshell Summarizer is a small Python command-line and AWS Bedrock AgentCore
sample for exploring AWS Strands Agents. It accepts a request for a known story,
fetches that story from a bundled Project Gutenberg text collection, and prints
a short summary.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project was created to take first steps with Strands Agents and Bedrock
AgentCore. The story collection is intentionally small so the tool-calling
workflow stays visible: the agent should only summarize stories that exist in
the local manifest.

## What It Does

The CLI accepts a prompt such as:

```powershell
.\.venv\Scripts\python.exe -m nutshell_summarizer "Summarize the story about Snow White and Rose Red"
```

The agent then:

- reads the local story manifest
- includes the available story titles in the system prompt
- calls the `fetch_story_tool` tool when the user asks for a known story
- reads the matching bundled text file from `stories`
- asks the Bedrock-hosted model to summarize the story in about 100 words
- declines or asks for clarification when the requested story is not available

The same application package can run locally as a Python module or through the
AgentCore runtime adapter.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- Node.js 20 or later.
- npm.
- AWS CLI configured for an AWS identity that can use Bedrock and AgentCore.
- AgentCore CLI installed globally:

```powershell
npm install -g @aws/agentcore
```

The selected Bedrock model must also be enabled for the AWS account and region.

## Setup

Create the virtual environment, install the Python project with development
dependencies, and restore the generated AgentCore CDK dependencies:

```powershell
.\scripts\setup-dev.ps1
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`. It also expects `node`, `npm`, and `agentcore` to be
available on `PATH`.

## Running

Run the agent from the repository root:

```powershell
.\.venv\Scripts\python.exe -m nutshell_summarizer "Summarize the story of Iron Hans"
```

You can also run the installed console script:

```powershell
.\.venv\Scripts\nutshell-summarizer.exe "Summarize the story of Iron Hans"
```

Run the same agent through the local AgentCore runtime with:

```powershell
agentcore dev "Summarize the story about Snow White and Rose Red"
```

For runtime logs:

```powershell
agentcore dev --logs
```

## Deployment

Validate the AgentCore configuration:

```powershell
agentcore validate
```

Preview the deployment:

```powershell
agentcore deploy --dry-run
```

Deploy to AWS Bedrock AgentCore:

```powershell
agentcore deploy -y -v
```

Invoke the deployed runtime:

```powershell
agentcore invoke --runtime NutshellSummarizer "Summarize the story about Snow White and Rose Red" --stream
```

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
app/NutshellSummarizer/
  entrypoint.py          Bedrock AgentCore runtime entry point
  pyproject.toml         Minimal runtime package metadata
  nutshell_summarizer/
    __main__.py          Package entry point for python -m nutshell_summarizer
    cli.py               Local command-line adapter
    bedrock.py           AgentCore runtime adapter
    agent.py             Strands Agent setup and system prompt
    tools.py             Story-fetching Strands tool
    library.py           Story manifest and content loading
    stories/             Bundled Project Gutenberg story texts

agentcore/
  agentcore.json         AgentCore project configuration
  cdk/                   Generated CDK deployment project

tests/
  test_smoke.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

The story collection is deliberately small. If the user asks for a story that is
not listed in the manifest, the agent is instructed not to invent the story
contents.

The `agentcore` directory should be committed because it is the infrastructure
configuration for this sample. Generated folders such as
`agentcore/cdk/node_modules`, `agentcore/cdk/cdk.out`, `agentcore/.cache`, and
local virtual environments should not be committed.

Agent behavior and final wording can vary between runs because tool selection
and final response generation are model-driven. Bedrock model calls may incur
usage costs.

To remove temporary AgentCore resources after experimenting:

```powershell
agentcore remove all -y
agentcore deploy -y -v
```

## Third-Party Notices

This project has direct runtime dependencies on third-party Python packages,
including `bedrock-agentcore`, `botocore`, `strands-agents`, and
`aws-opentelemetry-distro`. It also uses generated AgentCore CDK dependencies
under `agentcore/cdk`. See each package's registry license metadata for full
license and notice terms.

The bundled story texts are public-domain works sourced from Project Gutenberg.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.
