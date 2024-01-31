from app.Utils.google_API import get_source_url, get_image_url, get_map_image_url
import time
import json
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
import aiohttp
import asyncio
import os
import random
import requests

client = OpenAI()

load_dotenv()

tokenizer = tiktoken.get_encoding('cl100k_base')

transcript = ''

substring_to_replace = "https://www.google.com/maps/place/"

def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)
   
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def get_localImageURL(category, url, idx):
    if not os.path.exists("./data/text"):
        os.makedirs("./data/text")
    with open(f"./data/text/{category}_{idx}.jpg", 'wb') as handle:
        response = requests.get(url, stream=True, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

def nullCheck(data: str):
    match data.lower():
        case 'n/a':
            return ''
        case 'not applicable':
            return ''
        case 'unknown':
            return ''
        case _:
            return data

def convert_media_to_dict(item, idx):
    try:
        # if not check_media(item):
        #     return {}
        title = google_result[item[0] + ' ' + item[1]]
        get_localImageURL('media', google_image_result[item[0] + ' ' + item[1]], idx)
        author = google_author_result[item[0] + ' '+ item[1] + ' ' + item[2]]
        image = f"https://api.recc.ooo/static/text/media_{idx}.jpg"
        result = {
            "Category": item[0],
            "Title": nullCheck(item[1]),
            "Author": nullCheck(item[2]),
            "Description": item[3],
            "imgURL": image,
            "launchURL": title,
            "authorURL": author,
        }
        return result
    except Exception as e:
        print(e)
        result = {
            "Category": "OpenAI Server Error",
            "Title": "OpenAI Server Error",
            "Title_Source": "",
            "Author": "OpenAI Server Error",
            "Author_Source": "",
            "Description": "OpenAI Server Error",
            "Image": "",
            "Launch_URL": "",
            "Key":""
        }
        print("convert media to dict error!")
        return result

def convert_place_to_dict(item):
    try:     
        image = serp_image_result[item[2] + ' ' + item[1] + ' ' + item[0]]
        map_image = serp_result[item[2] + ' ' + item[1] + ' ' + item[0]]
        result = {
            "Category": item[0],
            "Title": nullCheck(item[1]),
            "Author": nullCheck(item[2]),
            "Description": item[3],
            "imgURL": image,
            "launchURL": map_image,
            "authorURL": "",
        }
        return result
    except Exception as e:
        print(e)
        result = {
            "Category": "OpenAI Server Error",
            "Title": "OpenAI Server Error",
            "Title_Source": "",
            "Author": "OpenAI Server Error",
            "Author_Source": "",
            "Description": "OpenAI Server Error",
            "Image": "",
            "Launch_URL": "",
            "Key":""
        }
        print("convert place to dict error!")
        return result

serp_list = []
serp_result = {}
serp_image_result = {}
google_list = []
google_author_list = []
google_result = {}
google_author_result = {}
google_image_result = {}


async def fetch_serp_results(session, query):
    alt_query = ' '.join(unique_list(query.split()))
    try:
        params = {
            'api_key': os.getenv("SERP_API_KEY"),      # your serpapi api key: https://serpapi.com/manage-api-key
            "engine": "google_maps",
            "type": "search",  # from which device to parse data
            'q': alt_query, # search query
        }
        print('fetch place')
        try:
            async with session.get('https://serpapi.com/search.json', params=params) as response:
                results = await response.json()
        except Exception as error:
            print(error)

        first_place = results.get('place_results')
        if not first_place:
            first_place = results.get('local_results')[0]
        if 'gps_coordinates' in first_place:
            lat = first_place['gps_coordinates']['latitude']
            lng = first_place['gps_coordinates']['longitude']
            data_id = first_place['data_id']
            params = {
                "engine": "google_maps",
                "type": "place",
                "data": f"!4m5!3m4!1s{data_id}!8m2!3d{lat}!4d{lng}",
                "api_key": os.getenv("SERP_API_KEY")
            }
            try:
                async with session.get('https://serpapi.com/search.json', params=params) as response:
                    results = await response.json()
            except Exception as error:
                print(error)
            map_url = results['search_metadata']['google_maps_url']
            if substring_to_replace in map_url:
                map_url = map_url.replace(substring_to_replace, substring_to_replace + f"@{lat},{lng},17z/")
            serp_result[query] = map_url
            photo_params = {
                "engine": "google_maps_photos",
                "data_id": data_id,
                "api_key": os.getenv("SERP_API_KEY")
            }
            try:
                async with session.get('https://serpapi.com/search.json', params=photo_params) as response:
                    results = await response.json()
            except Exception as error:
                print(error)
            
            photo_url = results['photos'][0]['image']
            serp_image_result[query] = photo_url
            # print(serp_image_result[query])
            #print(serp_result[query])
    except Exception as error:
        print ("SERP fetch error:" ,error)
        serp_result[query] = "https://www.google.com/maps/place/Granite/@38.038073,-75.7687759,3z/data=!4m10!1m2!2m1!1sgranite+restaurant+paris!3m6!1s0x47e66f1a1fb579eb:0x265362fbe8c6f7b5!8m2!3d48.8610438!4d2.3419215!15sChhncmFuaXRlIHJlc3RhdXJhbnQgcGFyaXNaGiIYZ3Jhbml0ZSByZXN0YXVyYW50IHBhcmlzkgEXaGF1dGVfZnJlbmNoX3Jlc3RhdXJhbnSaASRDaGREU1VoTk1HOW5TMFZKUTBGblNVTlNYMk54VFRkM1JSQULgAQA!16s%2Fg%2F11ny2076x0?entry=ttu"

cx = os.getenv("CX_ID")

async def fetch_google_results(session, query, flag):
    alter_query = query + ' IMDB'
    params = {
        'q': alter_query,
        'cx': cx,
        'key': os.getenv("GOOGLE_API_KEY"),
    }
    if flag:
        params['searchType'] = 'image'
        params['num'] = 3
    try:
        async with session.get("https://www.googleapis.com/customsearch/v1", params=params) as response:
            results = await response.json()
        # print("results: ", results)
        # print("query: ", query, "  result: ", results['items'][0]['link'])
        if flag:
            google_image_result[query] = results['items'][0]['link']
            print("image: ", results['items'][0]['link'])
        else:
            google_result[query] = results['items'][0]['link']
            # print("results: ", results)
            # print("google: ", results['items'][0]['link'])
    except:
        if flag:
            google_image_result[query] = "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
        else:
            google_result[query] = "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"

async def fetch_google_author_results(session, query):
    alter_query = query + ' IMDB'
    params = {
        'q': alter_query,
        'cx': cx,
        'key': os.getenv("GOOGLE_API_KEY"),
    }
    try:
        async with session.get("https://www.googleapis.com/customsearch/v1", params=params) as response:
            results = await response.json()
        google_author_result[query] = results['items'][0]['link']
    except Exception as error:
        print('author result error:', error)
        google_author_result[query] = ""


# async def get_all_url_for_profile():
    # async with aiohttp.ClientSession() as session:
    #     tasks = []
    #     for query in serp_list:
    #         task = asyncio.ensure_future(fetch_serp_results(session, query))
    #         tasks.append(task)
    #     for query in google_list:
    #         task = asyncio.ensure_future(fetch_google_results(session, query, 0))
    #         tasks.append(task)
    #         task = asyncio.ensure_future(fetch_google_results(session, query, 1))
    #         tasks.append(task)
    #     results = await asyncio.gather(*tasks)

async def get_all_url_for_profile(typeCheckflag):
    if typeCheckflag == 'media':
        async with aiohttp.ClientSession() as session:
            tasks = []
            for query in google_list:
                task = asyncio.ensure_future(fetch_google_results(session, query, 0))
                tasks.append(task)
                task = asyncio.ensure_future(fetch_google_results(session, query, 1))
                tasks.append(task)
            for query in google_author_list:
                task = asyncio.ensure_future(fetch_google_author_results(session, query))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
    else:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for query in serp_list:
                task = asyncio.ensure_future(fetch_serp_results(session, query))
                tasks.append(task)
            results = await asyncio.gather(*tasks)

def insert_item_to_serp_list(item):
    serp_list.append(item[2] + ' ' + item[1] + ' ' + item[0])
    
def insert_item_to_google_list(item):
    google_list.append(item[0] + ' ' + item[1])
    google_author_list.append(item[0] + ' ' + item[1] + ' '+ item[2])

# async def update_answer(apiResponse):
#     answer = {'media': []}
#     try:
#         if 'media' in apiResponse:
#             for item in apiResponse['media']:
#                 insert_item_to_google_list(item)
#         if 'place' in apiResponse:
#             for item in apiResponse['place']:
#                 result = insert_item_to_serp_list(item)
        
#         await get_all_url_for_profile()
#         print("here")

#         if 'media' in apiResponse:
#             for index, item in enumerate(apiResponse['media']):
#                 result = convert_media_to_dict(item, index)
#                 if not result:
#                     continue
#                 else:
#                     answer['media'].append(result)
#         if 'place' in apiResponse:
#             for item in apiResponse['place']:
#                 result = convert_place_to_dict(item)
#                 if not result:
#                     continue
#                 else:
#                     answer['media'].append(result)
#         return answer
#     except Exception as e:
#         print(e)
#         print("update answer error!")
#         return []

async def update_answer(apiResponse, typeCheckflag):
    answer = {'media': []}
    try:
        if typeCheckflag == 'media':
            for item in apiResponse['media']:
                insert_item_to_google_list(item)
        if typeCheckflag == 'place':
            for item in apiResponse['place']:
                result = insert_item_to_serp_list(item)
        
        await get_all_url_for_profile(typeCheckflag)
        print("here")

        if typeCheckflag == 'media':
            for index, item in enumerate(apiResponse['media']):
                result = convert_media_to_dict(item, index)
                if not result:
                    continue
                else:
                    answer['media'].append(result)
        if typeCheckflag == 'place':
            for item in apiResponse['place']:
                result = convert_place_to_dict(item)
                if not result:
                    continue
                else:
                    answer['media'].append(result)
        return answer
    except Exception as e:
        print(e)
        print("update answer error!")
        return []

async def get_structured_answer_not_functionCalling(context: str):
    # Step 1: send the conversation and available functions to GPT
    start_time = time.time()  
    print(tiktoken_len(context))
    try:
        response = client.chat.completions.create(
            model='gpt-4-0125-preview',
            max_tokens=2000,
            messages=[
                {'role': 'system', 'content': "Get the 'media's and 'place's from the input content in json, Dont' forget that the category of media must be the media type, not the place like restaurant, museum or other words associated to places. Dont' forget that category of place must be the place type, not the media like book, movies and other words associated to media type."},
                {'role': 'user', 'content': f"""
                    This is the input content you have to analyze.
                    {context}""" +
                    """
                    Please extract the following information from the above text:
                    In the input, there will be'media's such as books, movies, articles, podcasts, attractions, and places such as restaurants, museums, hotels, tourist destinations, and bars.

                    For media, please output category, title, author, and description.
                    Dont' forget that the category of media must be the media type, not the place like restaurant, museum or other words associated to places.
                    Don't forget that the description must be in the input content and should be the simple part (less than 100 words) of the input, not your knowledge.
                    Dont' forget that author must be the person's name and the most famous, only one person and you should.
                    Dont' forget that if 1 or 2 of the other 3 properties (category, title, and author) are not mentioned in the input content, then you must come up with them using your knowledge.
                    Dont' forget you must find title and author using your knowledge and must not output 'unknown'. It is illegal.
                    
                    For place, please output category, title, subtitle, and only one sentence description.
                    Dont' forget that category of place must be the place type, not the media like book, movies and other words associated to media type.
                    Don't forget that the description must be in the input content and should be the simple part (less than 100 words) of the input, not your knowledge.
                    Dont' forget that if 1 or 2 of the other 3 properties (category, title and subtitle) are not mentioned in the input content, then you must come up with them using your knowledge.                 
                    Dont' forget you must find the title using your knowledge and not output 'unknown'. It is illegal.

                    Sample output format is below:
                        {"media": [["book", "Fight Club", "Chuck Palahniuk", "Abcdefefddd"]],"place": [["bookstore", "The Painted Porch", "Historical bookstore in Bastrop, Texas", "This bookstore "]]}
                    You should output this type.
                """}
            ],
            seed=2425,
            temperature = 0.7,
            response_format={"type": "json_object"}
        )
        response_message = response.choices[0].message.content
        json_response = json.loads(response_message)
        print(json_response)
        # system_fingerprint = response.system_fingerprint
        print("Elapsed Time: ", time.time() - start_time)

        answer = await update_answer(json_response)
        return answer
    except Exception as e:
        print(e)
        print("hello")
        return {}

async def get_structured_media_answer(context: str):
    # Step 1: send the conversation and available functions to GPT
    start_time = time.time()
    print(tiktoken_len(context))
    try:
        response = client.chat.completions.create(
            model='gpt-4-0125-preview',
            max_tokens=2000,
            messages=[
                {'role': 'system', 'content': "Get the 'media's from the input content."},
                {'role': 'user', 'content': f"""
                    This is the input context you have to analyze.
                    {context}""" +
                    """
                    Extract and Output category, title, author, and description of media.
                    Category of 'media' should be media type such as book, movie, article, podcasts, attractions.
                    Always focus on the category of media and dont' forget that the category of media must be the media type, not the place like restaurant, museum or other words associated to places.
                    Don't forget that the description must be in the input content and should be the simple part (less than 50 words) of the input, not your knowledge.
                    Dont' forget that author must be the person's name and the most famous, only one person and you should.
                    Dont' forget that if 1 or 2 of the other 3 properties (category, title, and author) are not mentioned in the input content, then you must come up with them using your knowledge.
                    Dont' forget you must find title and author using your knowledge and must not output 'unknown'. It is illegal.
                    Sample output json format is below:
                        {'media':[["book", "Fight Club", "Chuck Palahniuk", "Abcdefefddd"],["movie", "World War 2", "Allen AMsi", "Amcifer"]]}
                    You should output this type.
                """}
            ],
            seed= 4826,
            temperature = 0.5,
            response_format={"type": "json_object"}
        )
        response_message = response.choices[0].message.content
        json_response = json.loads(response_message)
        print(json_response)
        system_fingerprint = response.system_fingerprint
        print("media_fingerprint: ", system_fingerprint)
        # print(randon_seed)
        print("Elapsed Time: ", time.time() - start_time)
    except Exception as e:
        print(e)
        print("hello")
        return {}
    try:
        answer = await update_answer(json_response, 'media')
        return answer
    except Exception as error:
        print(error)
        return {}

async def get_structured_place_answer(context: str):
    # Step 1: send the conversation and available functions to GPT
    start_time = time.time()
    print(tiktoken_len(context))
    try:
        response = client.chat.completions.create(
            model='gpt-4-0125-preview',
            max_tokens=2000,
            messages=[
                {'role': 'system', 'content': "Get 'place's from the input content in json"},
                {'role': 'user', 'content': f"""
                    This is the input content you have to analyze.
                    {context}""" +
                    """
                    Extract and Output category, title, subtitle, and description of place.
                    Category of 'place' should be place type such as restaurants, museums, hotels, tourist destinations and bars.
                    Dont' forget that category of place must be the place type, not the media like book, movies and other words associated to media type.
                    Don't forget that the description must be in the input content and should be the simple part (less than 50 words) of the input, not your knowledge.
                    Dont' forget that if 1 or 2 of the other 3 properties (category, title and subtitle) are not mentioned in the input content, then you must come up with them using your knowledge and must contain the area or country in title or subtitle that helps to find correct place among the places which has same names.                 
                    Dont' forget you must find the title using your knowledge and not output 'unknown'. It is illegal.

                    Sample output format is below:
                        {"place": [["bookstore", "The Painted Porch in Bastrop, Texas", "Historical bookstore in Bastrop, Texas", "This bookstore "]]}
                    You should output this type.
                """}
            ],
            seed= 6601,
            temperature = 0.5,
            response_format={"type": "json_object"}
        )
        response_message = response.choices[0].message.content
        json_response = json.loads(response_message)
        print(json_response)
        system_fingerprint = response.system_fingerprint
        # print(random_seed)
        print("place_fingerprint: ", system_fingerprint)
        print("Elapsed Time1: ", time.time() - start_time)
    except Exception as e:
        print(e)
        print("hello")
        return {}

    try: 
        answer = await update_answer(json_response,'place')
        return answer
    except Exception as error:
        print(error)
        return {}

async def complete_text(context: str):
    current_time =  time.time()
    result = await asyncio.gather(get_structured_media_answer(context), get_structured_place_answer(context))
    result = {'media' : result[0]['media'] + result[1]['media']}
    # result =  await get_structured_media_answer(context)
    print("Total time: ", time.time() - current_time)
    # print(google_image_result)
    # print(google_result)
    # result = await get_structured_answer_not_functionCalling(context)
    return result