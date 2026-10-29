import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from career_twin.context import build_system_prompt
from career_twin.tools import TOOLS, handle_tool_calls

load_dotenv(override=True)

MODEL = "gpt-5.4-mini"

client = OpenAI()
system_prompt = build_system_prompt()


def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)

    while response.choices[0].finish_reason == "tool_calls":
        assistant_message = response.choices[0].message
        tool_results = handle_tool_calls(assistant_message.tool_calls)

        messages.append(assistant_message)
        messages.extend(tool_results)

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)

    return response.choices[0].message.content


def main():
    gr.ChatInterface(chat).launch(inbrowser=True)


if __name__ == "__main__":
    main()