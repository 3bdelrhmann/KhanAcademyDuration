import xmltodict
import requests
import json

url = "https://en.wikipedia.org/w/api.php"

params = {
    'access_token' : 'asafsassafasf56465465465as5d6a4sf'}

r = requests.post(url=url, params=params)

r.content # XML , JSON Response

