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
                'foodNutrients': food.get('foodNutrients', [])
            }
        necessary_foodinfo.append(food_info)
        formatted_food_info = []
        for food_info in necessary_foodinfo:
            food_dict = {
                'Description': food_info['description'],
                'Nutrients': []
            }
            for nutrient in food_info['foodNutrients']:
                nutrient_dict = {
                    'Nutrient ID': nutrient.get('nutrientId', 'N/A'),
                    'Nutrient Name': nutrient.get('nutrientName', 'N/A'),
                    'Value': nutrient.get('value', 'N/A'),
                    'Unit Name': nutrient.get('unitName', 'N/A')
                }
                food_dict['Nutrients'].append(nutrient_dict)
            formatted_food_info.append(food_dict)
        return formatted_food_info
