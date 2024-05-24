import os
import requests
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
load_dotenv()

# Keycloak server configuration from environment variables
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TOTAL_USERS = int(os.getenv("TOTAL_USERS"))
NUM_THREADS = 10  # Number of threads to use for parallel execution


# Authenticate with Keycloak to get an access token
def get_access_token():
    url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    payload = {
        "client_id": CLIENT_ID,
        "username": USERNAME,
        "password": PASSWORD,
        "grant_type": "password"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]


# Check if the realm exists
def realm_exists(token):
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200


# Create the realm if it doesn't exist
def create_realm(token):
    url = f"{KEYCLOAK_URL}/admin/realms"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    realm_data = {
        "realm": REALM,
        "enabled": True
    }
    response = requests.post(url, json=realm_data, headers=headers)
    response.raise_for_status()


# Create a new user in Keycloak
def create_user(token, user_data):
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=user_data, headers=headers)
    response.raise_for_status()


# Generate user data
def generate_user_data(index):
    username = f"user{index}"
    first_name = f"First{index}"
    last_name = f"Last{index}"
    email = f"{username}@example.com"
    return {
        "username": username,
        "enabled": True,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "emailVerified": True,
        "credentials": [
            {
                "type": "password",
                "value": email,
                "temporary": False
            }
        ]
    }


# Function to handle user creation
def handle_user_creation(index):
    global token
    user_data = generate_user_data(index)
    try:
        create_user(token, user_data)
        return f"User {index} created."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:  # Unauthorized
            token = get_access_token()
            create_user(token, user_data)
            return f"User {index} created after refreshing token."
        else:
            raise


def main():
    global token
    token = get_access_token()

    # Ensure the realm exists
    if not realm_exists(token):
        create_realm(token)
        print(f"Realm '{REALM}' created.")

    start_time = time.time()

    # Use ThreadPoolExecutor to create users in parallel
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(handle_user_creation, i) for i in range(1, TOTAL_USERS + 1)]
        for i, future in enumerate(as_completed(futures)):
            try:
                result = future.result()
                if i % 100 == 0:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")
                break

    end_time = time.time()
    print(f"Finished creating {TOTAL_USERS} users in {end_time - start_time} seconds.")


if __name__ == "__main__":
    main()
