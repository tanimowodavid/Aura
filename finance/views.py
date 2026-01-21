from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import FinancialProfile, FinanceHistory



@login_required
def dashboard_view(request):
    """Show user dashboard with financial summary"""
    try:
        profile = request.user.financial_profile
        history = FinanceHistory.objects.filter(profile=profile).order_by('timestamp')
        last_checkin = request.user.checkins.first()
        
        context = {
            'profile': profile,
            'history': list(history.values('estimated_total', 'timestamp')),
            'last_checkin': last_checkin,
            'next_checkin': request.user.next_check_in_at,
            'can_checkin': not request.user.next_check_in_at or timezone.now() >= request.user.next_check_in_at
        }
        return render(request, 'finance/dashboard.html', context)
    except FinancialProfile.DoesNotExist:
        # If profile doesn't exist, send back to onboarding
        request.user.is_onboarded = False
        request.user.save()
        return redirect('aura:onboarding')
