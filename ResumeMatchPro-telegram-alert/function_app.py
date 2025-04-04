import os
import azure.functions as func
import requests
import json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})


@app.function_name(name="ResumeMatchProTelegramAlert")
@app.route(route="telegram-webhook")
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get the raw request body
        req_body = req.get_body().decode('utf-8')
        # Send the raw body to Telegram
        send_to_telegram(req_body)
        return func.HttpResponse("Alert handled", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=500)
