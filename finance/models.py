# from django.conf import settings
# from django.db import models

# User = settings.AUTH_USER_MODEL

# class FinancialProfile(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="financial_profile"
#     )

#     estimated_balance = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         null=True,
#         blank=True
#     )

#     primary_goal = models.CharField(
#         max_length=255
#     )


#     # Flexible, AI-friendly context
#     financial_context = models.JSONField(
#         default=dict,
#         blank=True
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)




# class CheckIn(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="check_ins"
#     )

#     # When this check-in happened
#     check_in_at = models.DateTimeField(auto_now_add=True)

#     # Aura’s qualitative assessment
#     budget_health = models.CharField(
#         max_length=50,
#         choices=[
#             ("on_track", "On Track"),
#             ("slightly_off", "Slightly Off"),
#             ("off_track", "Off Track"),
#             ("unclear", "Unclear"),
#         ]
#     )

#     # Optional user-reported changes
#     reported_balance_change = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         null=True,
#         blank=True
#     )

#     # Flexible conversational summary
#     check_in_context = models.JSONField(
#         default=dict,
#         blank=True
#     )

#     # One-sentence Aura insight shown on dashboard
#     aura_insight = models.CharField(
#         max_length=255
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
