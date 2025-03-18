# import firebase_admin
# from firebase_admin import auth, credentials
#
# # Initialize Firebase Admin SDK
# cred = credentials.Certificate("waiter-firebase.json")
# firebase_admin.initialize_app(cred)
#
# # Generate a custom token for a test user
# custom_token = auth.create_custom_token("+919986905655")
# print("Custom Token:", custom_token.decode("utf-8"))
#
#
# # UPDATE users SET is_admin = TRUE WHERE phone_number = '+911234567891';
# # UPDATE users SET is_admin = TRUE WHERE phone_number = '+911234567892';
# # UPDATE users SET is_admin = TRUE WHERE phone_number = '+911234567893';
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("waiter-firebase.json")  # Ensure this path is correct
firebase_admin.initialize_app(cred)

id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJjNDAxN2U3MGE4MWM5NTMxY2YxYjY4MjY4M2Q5OThlNGY1NTg5MTkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2FpdGVyLWQ1ZTJkIiwiYXVkIjoid2FpdGVyLWQ1ZTJkIiwiYXV0aF90aW1lIjoxNzQxODY4MjM3LCJ1c2VyX2lkIjoiSkRvVXhzV2hjVmhWRDQ1UVZVWVg1QU01Nmc2MyIsInN1YiI6IkpEb1V4c1doY1ZoVkQ0NVFWVVlYNUFNNTZnNjMiLCJpYXQiOjE3NDE4NjgyMzcsImV4cCI6MTc0MTg3MTgzNywicGhvbmVfbnVtYmVyIjoiKzkxMTIzNDU2Nzg5MyIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsicGhvbmUiOlsiKzkxMTIzNDU2Nzg5MyJdfSwic2lnbl9pbl9wcm92aWRlciI6InBob25lIn19.rJufOmFBeqiBv5Nl3NJ3RJDzjciKtUwqoakVOVt6SHpXpThJzRs_cXtRZGQ4auzvqNXMYNPHlbE9S68kw7MkmV6G8hn3lJwMHJHVdYWZIVBHiVALXN7Kk2AnCu5jCOrx6rJpkUNPpEpLRG0im70zEy29TMlcazxoLOhdXeJUR4TyRteQENU5APbXpkvCqDa3-_yk3nXmp0hq0ONEQ_UwnniYksddPi1bQz-Rdpm984d8lgdi6DDWRQaw3Pkhs0szSdPT7ABKrQO6wKWzxM3Ypu2rj_Wkgn0IEIrBITE45fCKNspVh_e6z3NzbeWkbHnnIOuDKeCOwj2bDOB1lDRiKQ"
try:
    decoded_token = auth.verify_id_token(id_token)
    print("Token Verified:", decoded_token)
except Exception as e:
    print("Firebase Error:", e)
