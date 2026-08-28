import os
import requests

api_key = os.getenv("OPENROUTER_API_KEY")

business = input("What type of business do you want to analyze? ")
location = input("Where is the business located? ")
employees = input("How many employees does it have? ")

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": f"""
Analyze this business:

Business type: {business}
Location: {location}
Number of employees: {employees}

Give me 3 common problems this business may face and one practical AI solution for each problem.
Explain the solutions clearly and keep them realistic for a small business.
"""
            }
        ],
    }
)

data = response.json()

print("\n--- AI BUSINESS ANALYSIS ---\n")
print("\n" + "=" * 60)
print("        AI BUSINESS PROBLEM FINDER")
print("=" * 60)
print(f"Business: {business}")
print(f"Location: {location}")
print(f"Employees: {employees}")
print("-" * 60)
print("\nAI ANALYSIS\n")
print(data["choices"][0]["message"]["content"])
print("\n" + "=" * 60)
