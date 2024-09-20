import firebase_admin # type: ignore
from firebase_admin import credentials, auth # type: ignore

# Path to the Firebase service account key JSON file
# cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
cred = credentials.Certificate('C:/Users/AleenaS/Downloads/LullabeamAuth/firebase_auth_django/firebase_auth_django/serviceAccountKey.json')

# Initialize Firebase app
firebase_admin.initialize_app(cred)
