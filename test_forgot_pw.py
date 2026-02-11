import requests
import json

BASE_URL = "http://127.0.0.1:8000"  # Adjust if your backend runs on a different port

def test_forgot_password():
    url = f"{BASE_URL}/auth/forgot-password"
    payload = {"email": "muzzushaik1619@gmail.com"}
    headers = {"Content-Type": "application/json"}
    
    print(f"Testing POST {url}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200 and response.json().get("status") == "success":
            print("✅ Success! Check your email for the 4-digit OTP.")
        else:
            print("❌ Failed. Check backend logs.")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure your FastAPI server is running at http://127.0.0.1:8000")

if __name__ == "__main__":
    test_forgot_password()
