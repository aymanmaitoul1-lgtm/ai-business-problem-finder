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

Find the 3 most important and realistic operational problems this business is likely to face.

For EACH problem, use exactly this format:

1. PROBLEM NAME
Problem: [1-2 short sentences]
AI Solution: [1-2 short sentences]
Impact: [Low / Medium / High + one short reason]

Keep each problem under 40 words.

After the 3 problems, provide:

ASSUMPTIONS:
- [maximum 3 short bullet points]

RECOMMENDATIONS:
1. [short recommendation]
2. [short recommendation]
3. [short recommendation]

IMPORTANT:
- Be specific to this business and its size.
- Avoid generic advice.
- Do not invent statistics, regulations, revenue figures, or facts.
- Clearly label estimates or assumptions.
- Keep everything concise and professional.
- Do not write long explanations.
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
