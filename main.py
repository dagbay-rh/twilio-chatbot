from pprint import pprint
from flask import Flask, request, session
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

GPT3_CHATBOT_URL="https://gpt-chatbot-api.herokuapp.com/"

@app.route("/api/chatbot", methods=['POST'])
def sms_reply():
    print("Request form: ", end="")
    pprint(request.form)

    personalities = get_personalities()
    pprint(personalities.json())

    incoming_sms = request.form['Body']

    # bot_response = requests.post(GPT3_CHATBOT_URL + "/api/chat", )

    resp = MessagingResponse()
    resp.message("PANIK: " + incoming_sms)

    return str(resp), 200

def get_personalities():
    return requests.get(GPT3_CHATBOT_URL + "api/personalities")


if __name__ == "__main__":
    app.run(debug=True)