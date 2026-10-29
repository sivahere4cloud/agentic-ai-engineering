import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def push(message):
    print(f"Push: {message}")
    payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
    response = requests.post(PUSHOVER_URL, data=payload, timeout=10)
    print("Status:", response.status_code)


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"


def record_unknown_question(question):
    push(f"Recording question I couldn't answer: {question}")
    return "OK"


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a visitor wants to be in touch and has provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this visitor"},
            "name": {"type": "string", "description": "The visitor's name, if they provided it"},
            "notes": {"type": "string", "description": "Any extra context from the conversation worth recording"},
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question you could not answer because you did not know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that could not be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

TOOLS = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

TOOL_FUNCTIONS = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)

        tool_function = TOOL_FUNCTIONS.get(tool_name)

        if tool_function:
            result = tool_function(**arguments)
        else:
            result = "No tool found"

        results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})

    return results