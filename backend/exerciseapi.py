#!/usr/bin/python3
import requests

def exerciseapi(muscle):
    """this is the function to get api endpoint of various exercises"""
    api_key = '3/Kb2JoHakfKPDIWAfNvNQ==XpvNetsEkph5CJ9d'
    url = f'https://api.api-ninjas.com/v1/exercises?muscle={muscle}'
    headers= {
        'X-API-KEY': api_key
    }
    response = requests.get(url=url, headers=headers)
    data = response.json()
    return data
