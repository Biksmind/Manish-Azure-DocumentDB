from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from common import get_database


HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Azure DocumentDB Workshop Agents</title>
  <style>
    body { font-family: Segoe UI, Arial, sans-serif; max-width: 900px; margin: 32px auto; line-height: 1.5; }
    textarea { width: 100%; height: 90px; }
    button { padding: 8px 14px; margin-top: 8px; }
    pre { background: #f5f5f5; padding: 16px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>Azure DocumentDB Workshop Agents</h1>
  <p>This app runs from the current repository only. It uses your local .env and Azure DocumentDB collections.</p>
  <label>Agent</label>
  <select id="agent">
    <option>MobileAdvisor</option>
    <option>RetailOfferFinder</option>
  </select>
  <p><textarea id="question">Recommend a phone under 50000 for camera and battery</textarea></p>
  <button onclick="ask()">Ask</button>
  <pre id="answer">Answer will appear here.</pre>
  <script>
    async function ask() {
      const body = new URLSearchParams();
      body.set("agent", document.getElementById("agent").value);
      body.set("question", document.getElementById("question").value);
      const response = await fetch("/ask", { method: "POST", body });
      document.getElementById("answer").textContent = await response.text();
    }
  </script>
</body>
</html>
"""


def mobile_advisor(db, question: str) -> str:
    query = question.lower()
    filters: dict = {}
    if "under 50000" in query or "below 50000" in query:
        filters["priceInr"] = {"$lte": 50000}
    if "premium" in query:
        filters["segment"] = "Premium"
    if "budget" in query:
        filters["segment"] = "Budget"

    projection = {"_id": 0, "title": 1, "brand": 1, "segment": 1, "priceInr": 1, "description": 1}
    results = list(db.mobiles.find(filters, projection).sort("priceInr", 1).limit(5))
    if not results:
        return "No matching phones found in the mobiles collection."

    lines = ["MobileAdvisor found these options:"]
    for item in results:
        lines.append(
            f"- {item.get('title')} ({item.get('brand')}) | {item.get('segment')} | INR {item.get('priceInr')}"
        )
    return "\n".join(lines)


def retail_offer_finder(db, question: str) -> str:
    query = question.lower()
    filter_doc = {}
    if "flipkart" in query:
        filter_doc = {"offers.retailer": {"$regex": "Flipkart", "$options": "i"}}
    elif "amazon" in query:
        filter_doc = {"offers.retailer": {"$regex": "Amazon", "$options": "i"}}
    elif "oneplus" in query:
        filter_doc = {"title": {"$regex": "OnePlus", "$options": "i"}}

    results = list(db.retail_offers.find(filter_doc, {"_id": 0}).limit(5))
    if not results:
        return "No matching retail offers found."

    lines = ["RetailOfferFinder found these offers:"]
    for item in results:
        lines.append(f"\n{item.get('title')}")
        for offer in item.get("offers", [])[:3]:
            lines.append(
                f"- {offer.get('retailer')} | INR {offer.get('priceInr')} | {offer.get('availability')}"
            )
    return "\n".join(lines)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def do_POST(self) -> None:
        if self.path != "/ask":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        agent = form.get("agent", ["MobileAdvisor"])[0]
        question = form.get("question", [""])[0]

        client, db, _ = get_database()
        try:
            if agent == "RetailOfferFinder":
                answer = retail_offer_finder(db, question)
            else:
                answer = mobile_advisor(db, question)
        except Exception as exc:
            answer = f"Error: {exc}"
        finally:
            client.close()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(answer.encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    server = HTTPServer(("localhost", 8080), Handler)
    print("Workshop agents are running at http://localhost:8080")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
