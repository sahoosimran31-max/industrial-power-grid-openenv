#!/usr/bin/env python3
"""Debug script to capture exact 422 error details"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("DEBUGGING 422 ERROR")
print("=" * 70)

# Test different payload formats
test_payloads = [
    {"action": 0},
    {"action": 0, "message": "test"},
    {"action": 0, "message": ""},
    {"action": {"action": 0}},
    {"action": {"action": 0, "message": ""}},
]

for i, payload in enumerate(test_payloads, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}: Payload = {json.dumps(payload)}")
    print(f"{'='*70}")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ SUCCESS!")
            print(f"Response: {json.dumps(response.json(), indent=2)[:300]}")
        else:
            print(f"✗ ERROR")
            print(f"Response Body:\n{json.dumps(response.json(), indent=2)}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Is it running on port 8000?")
        break
    except Exception as e:
        print(f"✗ Exception: {e}")

print("\n" + "=" * 70)
