#!/usr/bin/env python3
"""
AI Virtual Try-On Application - Simple Launcher
==============================================

A simple script to start the virtual try-on application.

Usage:
    python run.py
    python run.py --port 3000
    python run.py --dev
"""

import sys
import os
import subprocess
import argparse

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Virtual Try-On Application")
    parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--dev", action="store_true", help="Development mode")

    args = parser.parse_args()

    print("🚀 Starting AI Virtual Try-On Application")
    print(f"📍 Server will run on: http://{args.host}:{args.port}")
    print(f"👤 Login credentials: admin / tryon2024")
    print("=" * 50)

    # Build uvicorn command
    cmd = [
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--host", args.host,
        "--port", str(args.port)
    ]

    if args.dev:
        cmd.extend(["--reload", "--log-level", "debug"])
        print("🔧 Running in development mode")
    else:
        cmd.extend(["--log-level", "info"])
        print("⚡ Running in production mode")

    print("=" * 50)
    print("🛑 Press Ctrl+C to stop the server")
    print()

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
