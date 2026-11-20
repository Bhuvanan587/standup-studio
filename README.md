# 🎤 Standup Studio

A **beginner-friendly Gradio project** that generates stand-up jokes from a topic you choose. It uses LangChain prompt templates and LCEL, and lets you select a chat-model provider and model name.

The project is intentionally small: one Python file, a simple web interface, and environment-based configuration. Use a model you already have access to; the examples below are starting points, not an exhaustive provider list.

## Features

- Enter a topic and choose the number of jokes (1–20).
- Choose a comedy style and humour intensity.
- Configure the provider, model name, and temperature in the interface.
- Use hosted models or a locally running Ollama model.
- Keep API keys in a local `.env` file rather than in source code.

## Requirements

- Python 3.10 or newer
- `pip`
- An API key for your chosen hosted provider, or a locally running Ollama server and a model pulled locally

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Bhuvanan587/standup-studio.git
cd standup-studio
```

### 2. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your provider

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set the default provider and model. Add the matching API key for a hosted provider. **Never commit your `.env` file or share your API key.**

The application also lets you change the provider and model from its interface.

## Choosing a model

The `MODEL_PROVIDER` value uses LangChain's provider identifier. The `MODEL` value is the model identifier accepted by that provider.

| Provider | Provider value | Example model | Authentication / notes |
|---|---|---|---|
| DeepSeek | `deepseek` | `deepseek-chat` | Set `DEEPSEEK_API_KEY` |
| Ollama | `ollama` | `llama3.2` | Run Ollama locally and pull the model first |
| OpenAI | `openai` | `gpt-4o-mini` | Set `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `claude-3-5-sonnet-latest` | Set `ANTHROPIC_API_KEY` |
| Google | `google_genai` | `gemini-2.0-flash` | Set `GOOGLE_API_KEY` |

Model availability and names can change. Use the model ID shown by your provider and check its current LangChain integration documentation if setup differs.

### Ollama example

Install and start Ollama using its official instructions, then pull a model:

```bash
ollama pull llama3.2
```

Set these values in `.env`:

```dotenv
MODEL_PROVIDER=ollama
MODEL=llama3.2
```

No cloud API key is needed for a local Ollama model. The Ollama server must be running and reachable from the machine running Standup Studio.

## Run the app

```bash
python app.py
```

Open the local URL printed in your terminal (usually `http://127.0.0.1:7860`). Choose a provider and model, enter a topic, select the joke settings, and click **Generate jokes**.

## Project structure

```text
standup-studio/
├── app.py             # LangChain chain and Gradio interface
├── requirements.txt   # Python dependencies and provider integrations
├── .env.example       # Safe configuration template (no real secrets)
├── .gitignore         # Excludes credentials and local files
└── README.md          # Setup and usage instructions
```

## How it works

1. `ChatPromptTemplate` builds a system instruction and a user request from the interface values.
2. `PROMPT | model` composes the prompt and selected chat model using LangChain Expression Language (LCEL).
3. The Gradio button calls the Python function and displays the returned model response.

## Troubleshooting

- **Authentication error:** Confirm the selected provider's API key is set in `.env`, then restart the app.
- **Unknown model:** Check that the model identifier is valid for the selected provider.
- **Ollama connection error:** Start Ollama, verify it is reachable, and confirm that the model has been pulled.
- **Missing integration package:** Reinstall dependencies with `pip install -r requirements.txt`.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
