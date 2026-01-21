import json


def onboarding_system_prompt(user):
    firstname = user.first_name
    return f"""
    You are Aura, a warm and empathetic AI financial companion. You're onboarding a new user named {firstname}.

Your goal is to have a natural, friendly conversation to understand their financial situation. You need to collect:
1. Their current estimated balance/savings
2. Their primary financial goal
3. Any additional context (income sources, expenses, challenges, dreams)

Be conversational and encouraging. Don't ask for everything at once - let it flow naturally. When you have enough information, call the complete_onboarding function.
"""

def checkin_system_prompt(user):
    firstname = user.first_name
    profile = user.financial_profile
    last_checkin = user.checkins.first()
    return f"""You are Aura, a supportive AI financial companion checking in with {firstname}.

Current financial snapshot:
- Balance: ${profile.estimated_balance}
- Primary Goal: {profile.primary_goal}
- Last Check-in: {last_checkin.created_at.strftime('%B %d, %Y') if last_checkin else 'This is their first check-in'}
{f"- Last Focus: {last_checkin.focus_until_next}" if last_checkin else ""}

Additional context: {json.dumps(profile.financial_context)}

Have a warm, encouraging conversation about:
1. How they've been doing financially
2. Any progress toward their goal
3. New income or expenses
4. Challenges or wins
5. Their current balance

When you have enough information, call the save_checkin function to record this session."""

# OpenAI Function Definitions
ONBOARDING_FUNCTIONS = [
    {
        "name": "complete_onboarding",
        "description": "Complete user onboarding by saving their financial profile",
        "parameters": {
            "type": "object",
            "properties": {
                "estimated_balance": {
                    "type": "number",
                    "description": "User's current estimated balance/savings"
                },
                "primary_goal": {
                    "type": "string",
                    "description": "User's primary financial goal"
                },
                "financial_context": {
                    "type": "object",
                    "description": "Additional financial context about the user (income sources, expenses, challenges, etc.)",
                    "properties": {}
                }
            },
            "required": ["estimated_balance", "primary_goal", "financial_context"]
        }
    }
]

CHECKIN_FUNCTIONS = [
    {
        "name": "save_checkin",
        "description": "Save the check-in session with user updates and guidance",
        "parameters": {
            "type": "object",
            "properties": {
                "estimated_balance": {
                    "type": "number",
                    "description": "User's current estimated balance"
                },
                "user_update": {
                    "type": "object",
                    "description": "What the user shared during this check-in (spending, income changes, challenges, wins, etc.)"
                },
                "summary": {
                    "type": "string",
                    "description": "Concise summary of this check-in session"
                },
                "advice": {
                    "type": "string",
                    "description": "Actionable financial advice for the user"
                },
                "focus_until_next": {
                    "type": "string",
                    "description": "Single primary focus area until next check-in"
                },
                "confidence_score": {
                    "type": "integer",
                    "description": "Confidence in data accuracy (0-100)",
                    "minimum": 0,
                    "maximum": 100
                },
                "financial_context_updates": {
                    "type": "object",
                    "description": "Updates to financial context based on new information"
                }
            },
            "required": ["estimated_balance", "summary", "advice", "focus_until_next"]
        }
    }
]
