import requests
import json
import config
from pprint import pprint
from flask import Flask, request, session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config.from_object(config.Appsettings)
app.config.from_file("appsettings.json", load=json.load)

gpt3ChatbotConfig = config.Gpt3Config(
    app.config.get("GPT3_URL"),
    app.config.get("GPT3_AUTH_KEY")
)

@app.route("/api/chatbot", methods=['POST'])
def sms_reply():
    personalities = get_personalities()

    request_body = request.form['Body']
    request_from = request.form["From"]

    bot_response = requests.post(
        gpt3ChatbotConfig.url + "/api/chat", 
        headers={
            "Authorization":gpt3ChatbotConfig.auth_key
        }
    )

    resp = MessagingResponse()
    resp.message("PANIK: " + request_body)

    return str(resp)

def get_personalities():
    return requests.get(gpt3ChatbotConfig.url + "/api/personalities")


if __name__ == "__main__":
    app.run(debug=True)