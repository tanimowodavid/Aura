

# Get user financial snapshot
def get_financial_snapshot(user_id: int) -> dict:
    """
    Returns the user's current financial state.
    """
    return {
        "current_balance": Decimal,
        "monthly_income": Decimal,
        "monthly_expenses": Decimal,
        "top_expense_categories": [
            {"category": str, "amount": Decimal}
        ],
        "active_goals": [
            {
                "goal_id": int,
                "title": str,
                "target_amount": Decimal,
                "current_amount": Decimal,
                "deadline": date | None
            }
        ]
    }

# Record balance update
def record_balance_snapshot(
    user_id: int,
    amount: Decimal,
    date: date,
    note: str = ""
) -> dict:
    """
    Records a new balance snapshot.
    """
    return {
        "status": "success",
        "recorded_balance": Decimal,
        "date": date
    }

# Record income or expense
def record_transaction(
    user_id: int,
    transaction_type: str,  # "income" | "expense"
    amount: Decimal,
    category: str,
    date: date,
    note: str = ""
) -> dict:
    """
    Records an income or expense entry.
    """
    return {
        "status": "success",
        "transaction_type": str,
        "amount": Decimal,
        "category": str
    }

# Evaluate goal progress
def evaluate_goal_progress(user_id: int, goal_id: int) -> dict:
    """
    Returns progress metrics for a specific goal.
    """
    return {
        "goal_id": int,
        "progress_percentage": float,
        "remaining_amount": Decimal,
        "on_track": bool
    }


# Schedule next check-in
def schedule_checkin(
    user_id: int,
    scheduled_for: datetime
) -> dict:
    """
    Schedules the user's next check-in.
    """
    return {
        "status": "scheduled",
        "scheduled_for": datetime
    }
