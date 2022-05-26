import requests
import json
import config
import static_responses
import sql
import random
from db_ops import *
from pprint import pprint
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# app config
app = Flask(__name__)
app.config.from_object(config.Appsettings)
app.config.from_file("appsettings.json", load=json.load)

gpt3_chatbot_config = config.Gpt3Config(
    app.config.get("GPT3_URL"),
    app.config.get("GPT3_AUTH_KEY")
)

# db config
query_execute(db_connect(), sql.create_user_table)

@app.route("/api/chatbot", methods=['POST'])
def sms_reply():
    raw_body = request.form['Body']
    raw_from = request.form["From"]

    ### error handling
    if raw_body and raw_body.isspace():
        return get_help_response()

    # get user from db
    conn = db_connect()
    rows = query_execute(conn, sql.check_for_user, [raw_from])

    # new user
    if len(rows) == 0:
        query_execute(conn, sql.insert_new_user, [raw_from, None, None])
        return get_help_response()

    split_body = raw_body.split(" ", 1)

    ### commands
    command = split_body[0]
    
    if command == "/help":
        return get_help_response()

    if command == "/personalities":
        return get_personalities_response()

    if command == "/show":
        personality = rows[0][1]
        if not personality or str(personality).isspace():
            personality = "...nothing ¯\_(ツ)_/¯ use /personality to set one!"
        return wrap_in_twiml(static_responses.show_personality_prefix + personality), 200
    
    if command == "/personality":
        if len(split_body) == 1:
            return wrap_in_twiml(static_responses.supply_personality_error), 400
        
        personality = split_body[1]
        
        if not is_personality_valid(personality):
            return wrap_in_twiml(static_responses.invalid_personality_error), 400

        query_execute(conn, sql.update_user_personality, [personality, rows[0][0]])
        return wrap_in_twiml(static_responses.set_personality_success), 200

    ### chat

    # set random personality if not set
    personality = rows[0][1]
    if not personality or str(personality).isspace():
        personality = get_random_personality()
        query_execute(conn, sql.update_user_personality, [personality, rows[0][0]])

    # add existing messages to prompt
    # TODO

    # get response from gpt3
    return get_gpt_response(raw_body, personality), 200

def is_personality_valid(personality: str) -> bool:
    return personality in get_personalities()

def get_help_response() -> str:
    return wrap_in_twiml(static_responses.help)

def get_personalities() -> list:
    raw_response = requests.get(gpt3_chatbot_config.url + "/api/personalities")
    response = json.loads(raw_response.content)
    return [p['id'] for p in response]

def get_personalities_response() -> str:
    personalities = get_personalities()
    response = static_responses.personalities_prefix + ", ".join(personalities) + "!"
    return wrap_in_twiml(response)

def get_random_personality() -> str:
    return random.choice(get_personalities())

def get_gpt_response(prompt: str, personality: str) -> str:
    gpt3_response = requests.post(
        gpt3_chatbot_config.url + "/api/chat",
        params= {
            "prompt": prompt,
            "personality": personality
        },
        headers={
            "Authorization":gpt3_chatbot_config.auth_key
        }
    )
    response = json.loads(gpt3_response.content)["response"]
    return wrap_in_twiml(response)

def wrap_in_twiml(response: str) -> str:
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)