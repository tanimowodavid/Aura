import json
from .llm import call_llm
from .prompts import ONBOARDING_SYSTEM_PROMPT


def start_onboarding(chat_history):
    """
    chat_history: list of dicts like:
    [
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ]
    """

    messages = [
        {"role": "system", "content": ONBOARDING_SYSTEM_PROMPT},
        *chat_history,
    ]

    response = call_llm(messages)

    # Try to parse JSON (signals onboarding completion)
    try:
        data = json.loads(response)
        return {
            "status": "completed",
            "data": data,
        }
    except json.JSONDecodeError:
        return {
            "status": "in_progress",
            "reply": response,
        }
