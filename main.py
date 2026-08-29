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

Identify the 3 most important and realistic operational problems this business is likely to face.

For each problem, provide:

PROBLEM:
Clearly describe the problem.

WHY IT MATTERS:
Explain why this problem could matter to the business.

AI SOLUTION:
Suggest one practical AI or automation solution.

HOW IT HELPS:
Explain how the solution could improve the business.

EXPECTED IMPACT:
Choose Low, Medium, or High and explain why.

IMPORTANT RULES:
- Focus specifically on this type and size of business.
- Avoid generic problems that could apply to every business.
- Do not invent statistics, regulations, revenue figures, or other facts.
- If you make an estimate or assumption, clearly label it as an estimate or assumption.
- Keep the recommendations realistic for a small business.
- Keep the final answer concise and professional.

At the end, provide:

ASSUMPTIONS:
List important assumptions you made.

RECOMMENDATIONS:
Give 3 short recommendations for the business.
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
