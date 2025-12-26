#!/usr/bin/env python3
"""
Simple script to test API endpoints
Run this after starting the server with: uvicorn app.main:app --reload
"""
import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


def print_response(method: str, url: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{method.upper()} {url}")
    print(f"Status: {response.status_code}")
    print(f"{'='*60}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print()


def test_health():
    """Test health endpoint"""
    print("Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("GET", "/health", response)
    return response.status_code == 200


def test_root():
    """Test root endpoint"""
    print("Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET", "/", response)
    return response.status_code == 200


def test_register(email: str = "test@example.com", password: str = "test123", full_name: str = "Test User"):
    """Test user registration"""
    print("Testing User Registration...")
    data = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
    print_response("POST", "/api/v1/auth/register", response)
    
    if response.status_code == 201:
        return response.json()
    return None


def test_login(email: str = "test@example.com", password: str = "test123") -> Optional[str]:
    """Test user login"""
    print("Testing User Login...")
    data = {
        "username": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", data=data)
    print_response("POST", "/api/v1/auth/login", response)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✓ Access Token: {token[:50]}...")
        return token
    return None


def test_get_current_user(token: str):
    """Test getting current user info"""
    print("Testing Get Current User...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print_response("GET", "/api/v1/auth/me", response)
    return response.status_code == 200


def test_create_lead(token: str):
    """Test creating a lead"""
    print("Testing Create Lead...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "property_address": "123 Main St",
        "property_city": "Los Angeles",
        "property_state": "CA",
        "property_zip": "90001",
        "owner_name": "John Doe",
        "owner_email": "john@example.com",
        "owner_phone": "555-1234"
    }
    response = requests.post(f"{BASE_URL}/api/v1/leads", json=data, headers=headers)
    print_response("POST", "/api/v1/leads", response)
    return response.status_code == 201


def test_get_leads(token: str):
    """Test getting leads"""
    print("Testing Get Leads...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/leads", headers=headers)
    print_response("GET", "/api/v1/leads", response)
    return response.status_code == 200


def test_list_stacking(token: str):
    """Test list stacking search"""
    print("Testing List Stacking Search...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "address": "123 Main St",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90001"
    }
    response = requests.post(f"{BASE_URL}/api/v1/list-stacking/search", json=data, headers=headers)
    print_response("POST", "/api/v1/list-stacking/search", response)
    return response.status_code == 200


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("API Testing Script")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the server is running: uvicorn app.main:app --reload\n")
    
    # Test basic endpoints
    test_health()
    test_root()
    
    # Test authentication flow
    print("\n" + "="*60)
    print("AUTHENTICATION TESTS")
    print("="*60)
    
    # Try to register (might fail if user exists)
    user_data = test_register()
    
    # Login
    token = test_login()
    
    if not token:
        print("\n❌ Login failed. Cannot test authenticated endpoints.")
        print("💡 Tip: Make sure PostgreSQL is set up and the database is running.")
        return
    
    # Test authenticated endpoints
    print("\n" + "="*60)
    print("AUTHENTICATED ENDPOINT TESTS")
    print("="*60)
    
    test_get_current_user(token)
    test_create_lead(token)
    test_get_leads(token)
    test_list_stacking(token)
    
    print("\n" + "="*60)
    print("✓ Testing Complete!")
    print("="*60)
    print("\n💡 Tip: Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("💡 Make sure the server is running:")
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   uvicorn app.main:app --reload")
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

