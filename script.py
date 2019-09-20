import requests
import random

#сюда можно добавить свои keywords
list_values = ['taxi', 'combination', 'immune', 'tie', 'expression', 'chase']

for v in list_values:
    requests.get(f'http://localhost:5000/script?keyword={v}')
