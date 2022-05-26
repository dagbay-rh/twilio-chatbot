db_name = "chatbot.db"

create_user_table = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        phoneNumber TEXT UNIQUE,
        personality TEXT,
        lastMessage TEXT
    );
"""

check_for_user = "SELECT phoneNumber, personality, lastMessage FROM user WHERE phoneNumber = ?"

insert_new_user = "INSERT INTO user (phoneNumber, personality, lastMessage) values (?, ?, ?)"

update_user_personality = "UPDATE user SET personality = ? WHERE phoneNumber = ?"

update_user_last_message = "UPDATE user SET lastMessage = ? WHERE phoneNumber = ?"