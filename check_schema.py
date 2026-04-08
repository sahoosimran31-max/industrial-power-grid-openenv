#!/usr/bin/env python3
"""Test script to debug the /step endpoint 422 error"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("Checking schema endpoint...")
try:
    response = requests.get(f"{BASE_URL}/schema")
    if response.status_code == 200:
        schema = response.json()
        print("\nAction Schema:")
        print(json.dumps(schema.get('action', {}), indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Exception: {e}")
