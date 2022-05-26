help = """
Welcome to Everybotty! If you would like to chat with a bot, select a personality or send a message.\n
Available commands: /help to see this message, /personalities to see available personalities, /personality <...> to set a personality, /show to show your set personality.\n
If you start chatting without selecting a personality, a random one will be chosen for you!\n
Example messages: '/help', '/personality lonely-bot', '/show', 'How are you today?'
"""

personalities_prefix = "The available personalities are: "

invalid_personality_error = "Error: invalid personality. See '/personalities' for a list of valid options." 

supply_personality_error = "Error: must supply a personality to use when invoking the '/personality' command. \
    See '/personalities' for a list of valid options."

set_personality_success = "Successfully set personality! Start chatting!"

show_personality_prefix = "Your set personality is: "