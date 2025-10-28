#!/usr/bin/env python3

import requests
import json
import time

def test_hugging_face_space():
    """Test the deployed Hugging Face Space"""
    
    base_url = "https://huggingface.co/spaces/Ramji2311/Skin-diseases"
    # Note: HF Spaces may need some time to start up
    
    print("🧪 Testing Hugging Face Space API")
    print("=" * 40)
    
    # Test 1: Health check
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data.get('message', 'OK')}")
            print(f"🧠 Model loaded: {data.get('model_loaded', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    
    # Test 2: Get diseases list
    print("📋 Testing diseases endpoint...")
    try:
        response = requests.get(f"{base_url}/diseases")
        if response.status_code == 200:
            diseases = response.json().get('diseases', [])
            print(f"✅ Found {len(diseases)} supported diseases")
            print("   Sample diseases:")
            for disease in diseases[:3]:
                print(f"   - {disease}")
        else:
            print(f"❌ Diseases list failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Diseases error: {e}")
    
    print()
    
    # Test 3: Telegram endpoint (without actual sending)
    print("📱 Testing Telegram endpoint...")
    test_data = {
        "disease": "Test Disease",
        "confidence": 0.95,
        "treatment": "Test treatment information"
    }
    
    try:
        response = requests.post(
            f"{base_url}/share-telegram",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"📡 Telegram endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Telegram endpoint working")
        else:
            print(f"⚠️  Expected error (no config): {response.text[:100]}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")
    
    print()
    print("🎉 Testing complete!")
    print(f"🌐 Visit your space: {base_url}")

if __name__ == "__main__":
    test_hugging_face_space()