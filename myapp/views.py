
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoginForm  # Import the LoginForm from models.py
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
import json
import requests
from django.conf import settings
from .firebase_auth import signup_firebase_user, login_firebase_user


# cred = credentials.Certificate("C:/Users/AleenaS/Downloads/LullabeamAuth/firebase_auth_django/firebase_auth_django/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if email and password and confirm_password:
            if password == confirm_password:
                # Call the Firebase signup API
                response = signup_firebase_user(email, password)

                if 'uid' in response:
                    # Signup successful
                    messages.success(request, 'User created successfully! A verification link has been sent to your email. Please verify your email before logging in.')
                    return redirect('login')
                else:
                    # Handle error response
                    error_message = response.get('error', {}).get('message', 'Something went wrong')
                    messages.error(request, f"Error: {error_message}")
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Please enter all required fields.')

    return render(request, 'signup.html')


   
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                # Authenticate with Firebase using REST API
                response = login_firebase_user(email, password)

                if 'idToken' in response:
                    # Fetch the user's details using Firebase Admin SDK
                    user = auth.get_user_by_email(email)

                    if user.email_verified:
                        # Login successful and email is verified
                        return redirect('dashboard')
                    else:
                        messages.error(request, 'Please verify your email before logging in.')
                else:
                    error_message = response.get('error', {}).get('message', 'Something went wrong')
                    messages.error(request, f"Error: {error_message}")

            except FirebaseError as e:
                messages.error(request, f"Firebase Error: {e}")
        else:
            messages.error(request, 'Please enter both email and password.')

    return render(request, 'login.html')


def dashboard(request):
    return render(request,'dashboard.html')

def reset_password(request):
    return render(request, 'reset_password.html')

# login is worked through backend views code, but signup and reset password functions are not using views, 
# which only for page redirection, bcoz those two functionalities are send email and email verification that's 
# only done in firebase client SDK(javascript).
