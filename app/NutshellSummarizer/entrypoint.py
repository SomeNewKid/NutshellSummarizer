"""AgentCore runtime entrypoint."""

from nutshell_summarizer.bedrock import app

if __name__ == "__main__":
    app.run()
