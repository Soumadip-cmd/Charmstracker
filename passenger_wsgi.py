"""
WSGI Entry Point for Hostinger Deployment
This file is used by Passenger/WSGI servers to start the FastAPI application
"""

import sys
import os
from pathlib import Path

# Get the absolute path to the application directory
CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

# Import the FastAPI application
from backend.server import app as application

# For debugging purposes
if __name__ == "__main__":
    print("=" * 50)
    print("CharmTracker WSGI Application")
    print(f"Current Directory: {CURRENT_DIR}")
    print(f"Python Path: {sys.path}")
    print("=" * 50)
