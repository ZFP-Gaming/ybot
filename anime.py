import requests
import os
from dotenv import load_dotenv
load_dotenv()

ANIME_URL = os.getenv('ANIME_URL')
query = 'Naruto'
req = requests.get(url = ANIME_URL + query)
response = req.json()

score = response['results'][0]['score'] 
print(score)