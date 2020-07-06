import requests
import os
from dotenv import load_dotenv
load_dotenv()

COVID_URL = os.getenv('COVID_URL') 
req = requests.get(url = COVID_URL)
response = req.json()

confirmed = response['confirmed']['value']
recovered = response['recovered']['value']
deaths = response['deaths']['value']
print(f'Confirmados: {confirmed}, Recuperados: {recovered} , Muertitos: {deaths}')