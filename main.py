import os
import requests

api_key = os.getenv("OPENROUTER_API_KEY")

business = input("What type of business do you want to analyze? ")
location = input("Where is the business located? ")
employees = input("How many employees does it have? ")

prompt = f"""
Analyze this business:

Business type: {business}
Location: {location}
Number of employees: {employees}

Act as an AI business automation consultant.

Analyze the business based on its type, location, and size.

Identify the 3 most important and realistic operational problems this business is likely to face.

For each problem:

1. Explain the problem clearly.
2. Explain why it matters to the business.
3. Propose one practical AI or automation solution.
4. Explain how the solution would help.
5. Estimate the potential impact as Low, Medium, or High.

Avoid generic advice. Focus on problems that are specifically relevant to this type and size of business.

Give the answer in a clear and professional format.
"""

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
                "content": prompt
            }
        ],
    },
    timeout=60
)

response.raise_for_status()

data = response.json()

print("\n" + "=" * 60)
print("AI BUSINESS PROBLEM FINDER")
print("=" * 60)
print(f"Business: {business}")
print(f"Location: {location}")
print(f"Employees: {employees}")
print("=" * 60)
print("\nAI ANALYSIS\n")
print(data["choices"][0]["message"]["content"])
print("\n" + "=" * 60)
