#!/usr/bin/python3
from datetime import datetime
import requests

def foodapi(query):
    apikey = 'lloaOOv92V8k7JD3iN2GDjd4oXUCwXaATrsadI6O'
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apikey}&query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        necessary_foodinfo = []
        data = response.json()
        foods = data.get('foods', [])
        for food in foods:
            food_info = {
                'description': food.get('description', ''),
                'food nutritions': food.get('foodNutrients', [])
            }
        necessary_foodinfo.append(food_info)
    return necessary_foodinfo          
