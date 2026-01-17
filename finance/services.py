# from .models import FinancialProfile


# def complete_onboarding(user, onboarding_data):
#     profile = FinancialProfile.objects.create(
#         user=user,
#         estimated_balance=onboarding_data.get("estimated_balance"),
#         primary_goal=onboarding_data.get("primary_goal"),
#         goal_time_horizon=onboarding_data.get("goal_time_horizon"),
#         financial_context=onboarding_data.get("financial_context", {}),
#     )

#     user.is_onboarded = True
#     user.save(update_fields=["is_onboarded"])

#     return profile
