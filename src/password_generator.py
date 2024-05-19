import string
import random

def generate():
    characters = string.ascii_letters + string.digits 
    password = ''.join(random.choice(characters) for i in range(12))
    return password