#!/usr/bin/env python3
"""
Virtual Try-On Application Startup Script
=========================================

This script starts the virtual try-on application with proper configuration
and error handling.

Usage:
    python3 run_app.py [--port PORT] [--host HOST] [--dev]

Options:
    --port PORT     Port to run the server on (default: 8000)
    --host HOST     Host to bind to (default: 127.0.0.1)
    --dev           Run in development mode with auto-reload
    --help          Show this help message
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")

    try:
        import fastapi
        import uvicorn
        import jwt
        import requests
        import PIL
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Please run: pip install -r requirements.txt")
        return False

def check_test_images():
    """Check if test images are available"""
    test_images = ["man-with-arms-crossed.jpg", "10334540.jpg"]
    missing_images = []

    for image in test_images:
        if not os.path.exists(image):
            missing_images.append(image)

    if missing_images:
        print(f"⚠️  Test images not found: {', '.join(missing_images)}")
        print("   The application will still work with user-uploaded images")
    else:
        print("✅ Test images are available")

    return len(missing_images) == 0

def check_credentials():
    """Check if KlingAI credentials are configured"""
    access_key = os.getenv('KLING_ACCESS_KEY')
    secret_key = os.getenv('KLING_SECRET_KEY')

    # Check if credentials are in environment or use defaults
    has_env_creds = bool(access_key and secret_key)
    has_default_creds = True  # We have hardcoded defaults in the code

    if has_env_creds:
        print("✅ KlingAI credentials found in environment variables")
    elif has_default_creds:
        print("✅ Using default KlingAI credentials")
    else:
        print("⚠️  No KlingAI credentials found")
        print("   Set KLING_ACCESS_KEY and KLING_SECRET_KEY environment variables")
        print("   The application will fall back to alternative processing")

    return has_env_creds or has_default_creds

def print_startup_info(host, port, dev_mode):
    """Print application startup information"""
    print("\n" + "=" * 60)
    print("🚀 Virtual Try-On Application")
    print("=" * 60)
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Mode: {'Development' if dev_mode else 'Production'}")
    print(f"👤 Login: admin / tryon2024")
    print("=" * 60)
    print("\n💡 Features:")
    print("   • AI-powered virtual clothing try-on")
    print("   • Professional liquid glass UI")
    print("   • Multiple AI provider support")
    print("   • Secure authentication")
    print("   • Real-time processing status")

    print("\n📋 Usage:")
    print("   1. Open the URL above in your browser")
    print("   2. Login with the credentials shown above")
    print("   3. Upload a person image and garment image")
    print("   4. Click 'Generate Try-On' and wait for results")

    print("\n🛑 To stop the server: Press Ctrl+C")
    print("=" * 60)

def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(
        description="Virtual Try-On Application Startup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode with auto-reload"
    )

    args = parser.parse_args()

    print("🔧 Virtual Try-On Application Startup")
    print("-" * 40)

    # Pre-flight checks
    checks_passed = 0
    total_checks = 3

    if check_requirements():
        checks_passed += 1

    if check_test_images():
        checks_passed += 1

    if check_credentials():
        checks_passed += 1

    print(f"\n📊 Pre-flight checks: {checks_passed}/{total_checks} passed")

    if checks_passed < 2:
        print("❌ Too many critical issues found. Please resolve them before starting.")
        sys.exit(1)

    # Print startup information
    print_startup_info(args.host, args.port, args.dev)

    # Prepare uvicorn command
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", args.host,
        "--port", str(args.port)
    ]

    if args.dev:
        cmd.extend(["--reload", "--log-level", "debug"])
    else:
        cmd.extend(["--log-level", "info"])

    try:
        # Start the server
        print("🎬 Starting server...")
        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Thank you for using Virtual Try-On!")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   • Check if the port is already in use")
        print("   • Ensure all dependencies are installed")
        print("   • Try running with --dev flag for more details")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
