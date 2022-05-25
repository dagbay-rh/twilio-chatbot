db_name = "chatbot.db"

create_user_table = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        phoneNumber TEXT, 
        lastMessage TEXT
    );
"""

check_for_user = "SELECT phoneNumber FROM user WHERE phoneNumber = ?"

insert_new_user = "INSERT INTO user (phoneNumber, lastMessage) values (?, ?)"