#!/usr/bin/env python3
"""
Authentication Test Script
=========================

This script tests the authentication behavior of the Virtual Try-On application
to help diagnose login issues.
"""

import requests
import sys
from requests.auth import HTTPBasicAuth

def test_authentication():
    """Test the authentication endpoint"""

    # Test configuration
    base_url = "http://127.0.0.1:8000"  # Default port
    username = "admin"
    password = "tryon2024"

    print("Authentication Test for Virtual Try-On Application")
    print("=" * 55)
    print(f"Testing URL: {base_url}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print()

    try:
        # Test 1: Access without credentials (should get 401)
        print("Test 1: Accessing without credentials...")
        response = requests.get(base_url, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 401:
            print("✓ PASS: Server correctly requires authentication")

            # Check if WWW-Authenticate header is present
            auth_header = response.headers.get('WWW-Authenticate')
            if auth_header and 'Basic' in auth_header:
                print("✓ PASS: Server sends proper Basic auth challenge")
                print(f"  Auth Header: {auth_header}")
            else:
                print("✗ FAIL: Missing or incorrect WWW-Authenticate header")
                print(f"  Headers: {dict(response.headers)}")
        else:
            print("✗ FAIL: Server should return 401 without credentials")
            print(f"  Response: {response.text[:200]}...")

    except requests.exceptions.ConnectionError:
        print("✗ FAIL: Cannot connect to server")
        print("  Make sure the server is running with: python3 run_app.py")
        return False
    except Exception as e:
        print(f"✗ FAIL: Unexpected error: {e}")
        return False

    print()

    try:
        # Test 2: Access with correct credentials (should get 200)
        print("Test 2: Accessing with correct credentials...")
        auth = HTTPBasicAuth(username, password)
        response = requests.get(base_url, auth=auth, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✓ PASS: Authentication successful")

            # Check if the response contains expected content
            if "Virtual Try-On" in response.text:
                print("✓ PASS: Page content loaded correctly")
            else:
                print("✗ FAIL: Unexpected page content")

        else:
            print("✗ FAIL: Authentication failed with correct credentials")
            print(f"  Response: {response.text[:200]}...")

    except Exception as e:
        print(f"✗ FAIL: Error with authentication: {e}")
        return False

    print()

    try:
        # Test 3: Access with wrong credentials (should get 401)
        print("Test 3: Accessing with wrong credentials...")
        wrong_auth = HTTPBasicAuth("wrong", "credentials")
        response = requests.get(base_url, auth=wrong_auth, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 401:
            print("✓ PASS: Server correctly rejects wrong credentials")
        else:
            print("✗ FAIL: Server should reject wrong credentials")

    except Exception as e:
        print(f"✗ FAIL: Error testing wrong credentials: {e}")
        return False

    print()

    # Test 4: Test API status endpoint
    try:
        print("Test 4: Testing API status endpoint...")
        auth = HTTPBasicAuth(username, password)
        response = requests.get(f"{base_url}/api/status", auth=auth, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✓ PASS: API status endpoint accessible")
            try:
                data = response.json()
                print(f"  Status: {data.get('status', 'unknown')}")
                print(f"  Primary Provider: {data.get('primary_provider', 'unknown')}")
            except:
                print("  Could not parse JSON response")
        else:
            print("✗ FAIL: API status endpoint not accessible")

    except Exception as e:
        print(f"✗ FAIL: Error testing API status: {e}")

    print()
    print("=" * 55)
    print("Authentication Test Complete")
    print()
    print("Browser Login Instructions:")
    print("1. Open your browser")
    print(f"2. Go to: {base_url}")
    print("3. When prompted, enter:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print()
    print("If no login prompt appears:")
    print("- Try a different browser (Chrome, Firefox, Safari)")
    print("- Clear browser cache and cookies")
    print("- Try incognito/private browsing mode")
    print("- Check if browser has saved incorrect credentials")

    return True

def test_different_ports():
    """Test common ports to find where the server might be running"""

    print("\nPort Discovery Test")
    print("-" * 30)

    common_ports = [8000, 8080, 3000, 5000, 8888]

    for port in common_ports:
        try:
            url = f"http://127.0.0.1:{port}"
            response = requests.get(url, timeout=2)
            print(f"Port {port}: Server responding (Status: {response.status_code})")

            if response.status_code == 401:
                print(f"  ✓ Found Virtual Try-On server at {url}")
                return port

        except requests.exceptions.ConnectionError:
            print(f"Port {port}: No server")
        except Exception as e:
            print(f"Port {port}: Error - {e}")

    print("\nNo server found on common ports.")
    print("Make sure to start the server first with: python3 run_app.py")
    return None

if __name__ == "__main__":
    print("Starting authentication diagnostics...\n")

    # First, try to find the server
    port = test_different_ports()

    if port:
        print(f"\nTesting authentication on port {port}...")
        test_authentication()
    else:
        print("\nPlease start the server first:")
        print("python3 run_app.py")
        print("\nThen run this test again:")
        print("python3 test_auth.py")
