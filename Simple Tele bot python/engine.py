API_KEY = "5058869449:AAHC-2E3quVzrQKvWbyABYfjH8wqZwTRRvU"
import datetime
from datetime import date

def sample_responses(input_text):
    user_messages = str(input_text).lower()
    
    if user_messages in ("hello", "hi", "sup"):
        return "hows it going?"
    if user_messages in ("who are you?", "who r u"):
        return "I am a bot"
    if user_messages in ("what time?", "wat time?"):
        now = date.today()
        date_time = now.strftime("%d/%m/%y")
        
        return str(date_time)
    
    return "huh what u talking"