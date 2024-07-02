#!/usr/bin/python3
import requests

def foodapi(query):
    apikey = 'lloaOOv92V8k7JD3iN2GDjd4oXUCwXaATrsadI6O'
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apikey}&query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None