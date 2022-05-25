import requests
import json
import config
import static_responses
import sqlite3 as sl
import sql
import random
from db_ops import *
from pprint import pprint
from flask import Flask, request, session
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

    # error handling
    if raw_body and raw_body.isspace():
        return get_help_response()

    # get user from db
    conn = db_connect()
    rows = query_execute(conn, sql.check_for_user, [raw_from])

    if len(rows) == 0:
        query_execute(conn, sql.insert_new_user, [raw_from, ""])
        return get_help_response()
    
    split_body = raw_body.split(" ", 1)

    # check for commands
    command = split_body[0]
    
    if command == "/help":
        return get_help_response()

    if command == "/personalities":
        return get_personalities_response()

    # determine personality and prompt
    prompt = ""
    personality = ""
    
    if is_personality_present(command):
        personality = command
        if len(split_body) == 1 or split_body[1].isspace():
            return wrap_in_twiml(static_responses.missing_prompt_error), 400
        prompt = split_body[1]
    
    else:
        personality = get_random_personality()
        prompt = command

    # add existing messages to prompt

    # get response from gpt3
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

    return wrap_in_twiml(json.loads(gpt3_response.content)["response"]), 200

def is_personality_present(chunk: str):
    return chunk[-4] == "-bot"

def is_personality_valid(personality: str, personalities: list):
    return personality in personalities

def get_help_response():
    return wrap_in_twiml(static_responses.help)

def get_personalities():
    raw_response = requests.get(gpt3_chatbot_config.url + "/api/personalities")
    response = json.loads(raw_response.content)
    return response

def get_personalities_response():
    personalities = get_personalities()
    p_ids = [p['id'] for p in personalities]

    response = static_responses.personalities_prefix + ", ".join(p_ids) + "!"

    return wrap_in_twiml(response)

def get_random_personality():
    personalities = get_personalities()
    p_ids = [p['id'] for p in personalities]

    return random.choice(p_ids)

def wrap_in_twiml(response: str):
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)