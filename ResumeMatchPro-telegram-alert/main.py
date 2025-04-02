import os
import azure.functions as func
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        alert = req.get_json()
        essentials = alert.get("data", {}).get("essentials", {})
        rule = essentials.get("alertRule", "Unknown")
        description = essentials.get("description", "No description")
        severity = essentials.get("severity", "Unknown")
        message = f"🚨 *Alert Triggered*\nRule: {rule}\nDescription: {description}\nSeverity: {severity}"
        send_to_telegram(message)
        return func.HttpResponse("Alert handled", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)
