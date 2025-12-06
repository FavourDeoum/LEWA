import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(subject, question, mode="OL"):
    url = f"{BASE_URL}/{subject}"
    payload = {
        "question": question,
        "mode": mode
    }
    
    print(f"Testing {subject.capitalize()} ({mode})...")
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"Response snippet: {data['response'][:100]}...\n")
            return True
        else:
            print(f"❌ Failed with status code {response.status_code}")
            print(f"Error: {response.text}\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect. Is the server running?\n")
        return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def main():
    print("🚀 Starting API Verification...\n")
    
    results = [
        test_endpoint("geography", "What are the major rivers in Cameroon?", "OL"),
        test_endpoint("chemistry", "Explain the difference between ionic and covalent bonds.", "OL"),
        test_endpoint("economics", "What is opportunity cost?", "OL"),
        test_endpoint("religious_studies", "Who were the first disciples of Jesus?", "OL"),
        test_endpoint("french", "Conjugate the verb être in present tense", "OL")
    ]
    
    if all(results):
        print("✨ All tests passed! The integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the server logs and API key.")

if __name__ == "__main__":
    main()
