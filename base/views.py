from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm


# Signup view
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base:home')
    else:
        form = SignUpForm()
    
    return render(request, 'base/signup.html', {'form': form})


# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('base:home')
    else:
        form = LoginForm()
    
    return render(request, 'base/login.html', {'form': form})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('base:login')


# Home view
@login_required
def home_view(request):
    """Route to dashboard or onboarding based on user status"""
    if request.user.is_onboarded:
        return redirect('aura:dashboard')
    else:
        return redirect('aura:onboarding')

