#!/usr/bin/env python3
"""
Integration Test Script for KlingAI Virtual Try-On
=================================================

This script tests the KlingAI integration to ensure everything is working properly.
"""

import asyncio
import os
import sys
from kling_ai_client import KlingAIClient, process_virtual_tryon_kling

# Test credentials (same as in new_file.py)
ACCESS_KEY = "AJeTKte39b4nNKTGmh8ErCQEb9yM9pDg"
SECRET_KEY = "ef4G4CeGYfkDmTgfBdGhLJAkFCeGyANE"

# Test image paths
TEST_PERSON_IMAGE = "./sample_images/man-with-arms-crossed.jpg"
TEST_GARMENT_IMAGE = "./sample_images/10334540.jpg"

def load_test_image_as_base64(image_path):
    """Load test image and convert to base64 data URL"""
    import base64

    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return None

    with open(image_path, 'rb') as f:
        image_data = f.read()

    base64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_data}"

async def test_client_initialization():
    """Test 1: Client Initialization"""
    print("🧪 Test 1: Client Initialization")
    print("-" * 40)

    try:
        client = KlingAIClient(ACCESS_KEY, SECRET_KEY)
        print("✅ KlingAI client initialized successfully")
        print(f"   Base URL: {client.base_url}")
        print(f"   Model: {client.model_name}")
        return True
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False

async def test_jwt_token_generation():
    """Test 2: JWT Token Generation"""
    print("\n🧪 Test 2: JWT Token Generation")
    print("-" * 40)

    try:
        client = KlingAIClient(ACCESS_KEY, SECRET_KEY)
        token = client._encode_jwt_token()
        print("✅ JWT token generated successfully")
        print(f"   Token preview: {token[:50]}...")

        # Test auth headers
        headers = client._get_auth_headers()
        print("✅ Auth headers generated successfully")
        print(f"   Authorization header present: {'Authorization' in headers}")
        return True
    except Exception as e:
        print(f"❌ JWT token generation failed: {e}")
        return False

async def test_image_preparation():
    """Test 3: Image Preparation"""
    print("\n🧪 Test 3: Image Preparation")
    print("-" * 40)

    try:
        client = KlingAIClient(ACCESS_KEY, SECRET_KEY)

        # Load test images
        person_b64 = load_test_image_as_base64(TEST_PERSON_IMAGE)
        garment_b64 = load_test_image_as_base64(TEST_GARMENT_IMAGE)

        if not person_b64 or not garment_b64:
            print("❌ Could not load test images")
            return False

        # Test image preparation
        prepared_person = client._prepare_image(person_b64)
        prepared_garment = client._prepare_image(garment_b64)

        print("✅ Person image prepared successfully")
        print(f"   Prepared size: {len(prepared_person)} characters")
        print("✅ Garment image prepared successfully")
        print(f"   Prepared size: {len(prepared_garment)} characters")
        return True
    except Exception as e:
        print(f"❌ Image preparation failed: {e}")
        return False

async def test_health_check():
    """Test 4: API Health Check"""
    print("\n🧪 Test 4: API Health Check")
    print("-" * 40)

    try:
        client = KlingAIClient(ACCESS_KEY, SECRET_KEY)
        is_healthy = await client.health_check()

        if is_healthy:
            print("✅ API health check passed")
            print("   KlingAI API is accessible")
        else:
            print("⚠️  API health check failed")
            print("   KlingAI API may be temporarily unavailable")

        return is_healthy
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

async def test_full_integration():
    """Test 5: Full Integration Test"""
    print("\n🧪 Test 5: Full Integration Test")
    print("-" * 40)

    try:
        # Load test images
        person_b64 = load_test_image_as_base64(TEST_PERSON_IMAGE)
        garment_b64 = load_test_image_as_base64(TEST_GARMENT_IMAGE)

        if not person_b64 or not garment_b64:
            print("❌ Could not load test images for full test")
            return False

        print("🚀 Starting virtual try-on process...")
        print("   This may take 1-2 minutes...")

        # Test the full process
        result = await process_virtual_tryon_kling(person_b64, garment_b64)

        if result.get("success"):
            print("✅ Full integration test passed!")
            print(f"   Provider: {result.get('provider', 'unknown')}")
            print(f"   Result image URL: {result.get('result_image', 'No URL')[:100]}...")
            if result.get('task_id'):
                print(f"   Task ID: {result.get('task_id')}")
            return True
        else:
            print("❌ Full integration test failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            print(f"   Message: {result.get('message', 'No message')}")
            return False

    except Exception as e:
        print(f"❌ Full integration test failed: {e}")
        return False

async def main():
    """Run all integration tests"""
    print("🔧 KlingAI Integration Test Suite")
    print("=" * 50)

    # Check if test images exist
    if not os.path.exists(TEST_PERSON_IMAGE):
        print(f"❌ Test person image not found: {TEST_PERSON_IMAGE}")
        print("   Please ensure test images are in the project directory")
        return

    if not os.path.exists(TEST_GARMENT_IMAGE):
        print(f"❌ Test garment image not found: {TEST_GARMENT_IMAGE}")
        print("   Please ensure test images are in the project directory")
        return

    # Run tests
    tests = [
        test_client_initialization,
        test_jwt_token_generation,
        test_image_preparation,
        test_health_check,
        test_full_integration
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("-" * 30)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")

    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
    elif passed >= total - 1:
        print("⚠️  Most tests passed. Some issues may need attention.")
    else:
        print("❌ Multiple tests failed. Please check the configuration.")

    print("\n💡 Tips:")
    print("   - If health check fails, the API might be temporarily down")
    print("   - If full integration fails, check your credentials and network")
    print("   - Images must be in JPEG format for best results")

if __name__ == "__main__":
    asyncio.run(main())
