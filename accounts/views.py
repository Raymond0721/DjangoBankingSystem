from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from functools import wraps
from django.contrib.auth.models import User

# Assuming you have these forms defined similarly in your forms.py
from .forms import RegistrationForm, AuthenticationForm, ProfileForm


# auth check
def auth_check(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


# Registration View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Login View
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None:
                auth_login(request, user)
                return redirect('profile_view')
            else:
                form.add_error(None, "Username or password is invalid")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# Logout View
def logout(request):
    auth_logout(request)
    return redirect('login')


# User Profile View
@auth_check
def profile_view(request):
    user_details = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return JsonResponse(user_details)


@auth_check
# User Profile Edit View
def profile_edit(request):
    saved = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, initial=saved)
        if profile_form.is_valid():
            user = profile_form.save(request.user)
            auth_login(request, user)
            return redirect('profile_view')
    else:
        # Instantiate the form with the current user instance for initial data
        profile_form = ProfileForm(initial=saved)

    return render(request, 'accounts/profile.html', {'form': profile_form})
