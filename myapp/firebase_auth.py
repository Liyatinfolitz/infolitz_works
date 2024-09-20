import json
import requests
import firebase_admin
from firebase_admin import auth, credentials, exceptions


cred = credentials.Certificate("C:/Users/AleenaS/Downloads/LullabeamAuth/firebase_auth_django/firebase_auth_django/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

FIREBASE_WEB_API_KEY = "AIzaSyDbsC7CsSlEIRLi_eus5WXotruot8QYL6Y"
rest_api_signup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"



def signup_firebase_user(email, password):
    try:
        # Create the user in Firebase using Admin SDK
        user = auth.create_user(
            email=email,
            password=password
        )
        # After creating the user, send the email verification via Firebase REST API
        # send_verification_email(user.uid)
        print('----id-------',user.uid)
        verification_link = auth.generate_email_verification_link(email)
        send_verification_email_via_firebase(email, verification_link)

        return {"uid": user.uid}  # Return user UID if creation was successful
    except exceptions.FirebaseError as e:
        return {"error": {"message": str(e)}}

def send_verification_email_via_firebase(email, verification_link):
    """
    Automatically trigger Firebase to send the verification email using the built-in template.
    Firebase takes care of sending the email once you have generated the verification link.
    """
    print(f"A verification email has been sent to {email} with the following link: {verification_link}")
    # No need to use Django's email backend; Firebase takes care of this.

    
def send_verification_email(uid):
    """Send a verification email using Firebase REST API"""
    verification_url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}'
    payload = {
        "requestType": "VERIFY_EMAIL",
        "idToken": get_user_id_token(uid)  # You'll need the ID token of the user to send the verification email
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(verification_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Verification email sent successfully")
    else:
        print(f"Failed to send verification email: {response.json()}")


def get_user_id_token(uid):
    """Get the ID token of the user using Firebase Admin SDK"""
    user = auth.get_user(uid)
    return user.tokens_valid_after_timestamp  # Get the user ID token



def login_firebase_user(email, password):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload,
                      headers={"Content-Type": "application/json"})
    return r.json()