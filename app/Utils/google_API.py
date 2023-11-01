import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

cx = os.getenv("CX_ID")
api_key = os.getenv("GOOGLE_API_KEY")


def get_source_url(keyword):
    # print("keyword: ", keyword)
    # print(cx)
    # print(api_key)
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': keyword,
        'cx': cx,
        'key': api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    # print(data)
    return "https://www.amazon.com/Stolen-Focus-Attention-Think-Deeply/dp/0593138511"
    return data['items'][0]['link']


def get_image_url(search_term):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': search_term,
        'cx': cx,
        'key': api_key,
        'searchType': 'image',
        'num': 3
    }
    response = requests.get(url, params=params)
    response_json = json.loads(response.text)
    return "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
    return response_json['items'][0]['link']


# print(get_image_url("Stolen Focus - Johann Hari"))
