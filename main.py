import os
import json
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

Find the 3 most important and realistic operational problems this business is likely to face.

Return ONLY valid JSON.
Do not use markdown.
Do not use code fences.
Do not write anything before or after the JSON.

Use exactly this structure:

{{
  "problems": [
    {{
      "name": "Short problem name",
      "problem": "1-2 short sentences",
      "solution": "1-2 short sentences",
      "impact": "High"
    }},
    {{
      "name": "Short problem name",
      "problem": "1-2 short sentences",
      "solution": "1-2 short sentences",
      "impact": "Medium"
    }},
    {{
      "name": "Short problem name",
      "problem": "1-2 short sentences",
      "solution": "1-2 short sentences",
      "impact": "Low"
    }}
  ],
  "assumptions": [
    "Short assumption",
    "Short assumption"
  ],
  "recommendations": [
    "Short recommendation",
    "Short recommendation",
    "Short recommendation"
  ]
}}

IMPORTANT:
- Create exactly 3 problems.
- Make the problems specific to this business and its size.
- Avoid generic advice.
- Do not invent statistics, regulations, revenue figures, or other facts.
- Clearly label uncertain information as assumptions.
- Keep everything concise.
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

ai_text = data["choices"][0]["message"]["content"]

analysis = json.loads(ai_text)

print("\n" + "=" * 60)
print("AI BUSINESS PROBLEM FINDER")
print("=" * 60)
print(f"Business: {business}")
print(f"Location: {location}")
print(f"Employees: {employees}")
print("=" * 60)

print("\nAI ANALYSIS\n")

for number, problem in enumerate(analysis["problems"], start=1):
    print(f"{number}. {problem['name']}")
    print(f"Problem: {problem['problem']}")
    print(f"AI Solution: {problem['solution']}")
    print(f"Impact: {problem['impact']}")
    print()

print("ASSUMPTIONS")
for assumption in analysis["assumptions"]:
    print(f"- {assumption}")

print("\nRECOMMENDATIONS")
for number, recommendation in enumerate(analysis["recommendations"], start=1):
    print(f"{number}. {recommendation}")

print("\n" + "=" * 60)
