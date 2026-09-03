import os
import json
import requests
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


api_key = os.getenv("OPENROUTER_API_KEY")


PROMPT_TEMPLATE = """
Analyze this business:

Business: {business}
Location: {location}
Employees: {employees}

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


def analyze_business(business, location, employees):
    prompt = PROMPT_TEMPLATE.format(
        business=business,
        location=location,
        employees=employees
    )

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

    content = data["choices"][0]["message"]["content"]

    return content


class RequestHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        if self.path.split("?", 1)[0] == "/":
            try:
                with open("index.html", "rb") as file:
                    html = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()

                self.wfile.write(html)

            except FileNotFoundError:
                self.send_json(
                    {"error": "index.html was not found."},
                    404
                )

        else:
            self.send_json(
                {"error": "Page not found."},
                404
            )

    def do_POST(self):

        if self.path != "/analyze":
            self.send_json(
                {"error": "Endpoint not found."},
                404
            )
            return

        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            user_data = json.loads(body)

            business = user_data.get("business", "").strip()
            location = user_data.get("location", "").strip()
            employees = user_data.get("employees", "").strip()

            if not business or not location or not employees:
                self.send_json(
                    {"error": "Please fill in all fields."},
                    400
                )
                return

            result = analyze_business(
                business,
                location,
                employees
            )

            self.send_json(
                {
                    "success": True,
                    "analysis": result
                }
            )

        except requests.exceptions.RequestException as error:
            self.send_json(
                {
                    "error": f"AI request failed: {str(error)}"
                },
                500
            )

        except Exception as error:
            self.send_json(
                {
                    "error": str(error)
                },
                500
            )


print("=" * 60)
print("AI BUSINESS PROBLEM FINDER")
print("=" * 60)
print("Server running at:")
print("http://localhost:8000")
print("=" * 60)

server = ThreadingHTTPServer(
    ("localhost", 8000),
    RequestHandler
)

server.serve_forever()
