"""Standup Studio: a beginner-friendly Gradio app powered by LangChain."""

from __future__ import annotations

import os
from typing import Any

import gradio as gr
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

DEFAULT_MODEL = os.getenv("MODEL", "deepseek:deepseek-chat")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an experienced stand-up comedian.
Use this comedy style: {style}
Humour intensity: {intensity}

Write original jokes with clever setups, unexpected punchlines, and absurd
comparisons. Keep the humour accessible, avoid generic jokes and clichés,
and format the response as a numbered list. Do not explain the jokes.""",
        ),
        ("human", "Write {count} stand-up jokes about: {topic}"),
    ]
)


def build_chain(provider: str, model_name: str, temperature: float) -> Any:
    """Create the selected chat model and compose it with the prompt."""
    model = init_chat_model(
        model=model_name,
        model_provider=provider,
        temperature=temperature,
    )
    return PROMPT | model


def generate_jokes(
    topic: str,
    style: str,
    intensity: str,
    count: float,
    provider: str,
    model_name: str,
    temperature: float,
) -> str:
    """Generate jokes and return the model response as plain text."""
    if not topic or not topic.strip():
        raise gr.Error("Enter a topic before generating jokes.")
    if not model_name or not model_name.strip():
        raise gr.Error("Enter a model name.")
    if count is None or int(count) < 1 or int(count) > 20:
        raise gr.Error("Choose a joke count between 1 and 20.")

    try:
        chain = build_chain(provider, model_name.strip(), temperature)
        response = chain.invoke(
            {
                "topic": topic.strip(),
                "style": style,
                "intensity": intensity,
                "count": int(count),
            }
        )
        return str(response.content)
    except gr.Error:
        raise
    except Exception as exc:  # Show a useful UI error without exposing secrets.
        raise gr.Error(
            "Could not generate jokes. Check your provider, model name, API key, "
            "and network connection, then try again."
        ) from exc


with gr.Blocks(title="Standup Studio") as demo:
    gr.Markdown(
        "# 🎤 Standup Studio\n"
        "A beginner-friendly Gradio project for generating stand-up jokes "
        "with LangChain and the chat model of your choice."
    )

    topic = gr.Textbox(label="Enter a topic", placeholder="e.g. engineering in India")
    count = gr.Number(label="Joke count", value=5, precision=0, minimum=1, maximum=20)

    with gr.Row():
        style = gr.Dropdown(
            choices=["Observational", "Sarcastic", "Dark Humor"],
            value="Observational",
            label="Style of comedy",
        )
        intensity = gr.Dropdown(
            choices=["Mild", "Savage", "Brutal"],
            value="Mild",
            label="Humour intensity",
        )

    gr.Markdown("### Model settings")
    with gr.Row():
        provider = gr.Dropdown(
            choices=["deepseek", "ollama", "openai", "anthropic", "google_genai"],
            value=os.getenv("MODEL_PROVIDER", "deepseek"),
            label="Provider",
        )
        model_name = gr.Textbox(
            label="Model name",
            value=DEFAULT_MODEL,
            placeholder="e.g. deepseek-chat, llama3.2, gpt-4o-mini",
        )
        temperature = gr.Slider(
            minimum=0,
            maximum=1.5,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
            label="Temperature",
        )

    generate = gr.Button("Generate jokes", variant="primary")
    output = gr.Textbox(label="Your jokes", lines=15, interactive=False)

    generate.click(
        fn=generate_jokes,
        inputs=[topic, style, intensity, count, provider, model_name, temperature],
        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()
