from pprint import pprint
from flask import Flask, request, session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def sms_reply():
    query = request.form['Body']

    pprint(query)

    resp = MessagingResponse()
    resp.message("PANIK: " + query)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)