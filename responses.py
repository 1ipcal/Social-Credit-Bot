import random

def handle_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'hey there!'

    if p_message == 'roll':
        return str(random.ranint(1,6))
    
    if p_message == '!help':
        return 'some help here'

    # No valid responeses