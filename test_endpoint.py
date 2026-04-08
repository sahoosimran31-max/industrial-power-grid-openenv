#!/usr/bin/env python3
import requests
import json
import time

# Wait a moment for server to be ready
time.sleep(1)

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Industrial Power Grid Environment")
print("=" * 60)

# Test 1: Reset
print("\n1. Testing /reset endpoint...")
try:
    response = requests.post(f"{BASE_URL}/reset")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 2: Step with different action formats
print("\n2. Testing /step endpoint...")

test_payloads = [
    {"action": 0},
    {"action": 1},
    {"action": 2},
]

for payload in test_payloads:
    try:
        print(f"\n   Payload: {payload}")
        response = requests.post(f"{BASE_URL}/step", json=payload)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Response keys: {list(data.keys())}")
        else:
            print(f"   Error Response:")
            print(f"   {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

print("\n" + "=" * 60)
