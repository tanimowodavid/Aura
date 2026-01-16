from django.shortcuts import render
from aura.service.onboarding import start_onboarding
from finance.services import complete_onboarding

# Create your views here.
def onboarding_chat(request):
    user = request.user
    chat_history = request.session.get("chat_history", [])

    user_message = request.POST["message"]
    chat_history.append({"role": "user", "content": user_message})

    result = start_onboarding(chat_history)

    if result["status"] == "completed":
        complete_onboarding(user, result["data"])
        request.session.pop("chat_history", None)
        return {"message": "Onboarding complete 🎉"}

    else:
        chat_history.append({
            "role": "assistant",
            "content": result["reply"]
        })
        request.session["chat_history"] = chat_history
        return {"message": result["reply"]}
