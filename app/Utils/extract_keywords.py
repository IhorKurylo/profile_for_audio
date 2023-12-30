from app.Utils.google_API import get_source_url, get_image_url, get_map_image_url
import time
import json
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
import aiohttp
import asyncio
import os
import ast

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
   
# def check_media(item):
#     if ('Title' not in item) or ('Category' not in item):
#         return False
#     else:
#         return True

# def check_place(item):
#     if ('Title' not in item) or ('Category' not in item):
#         return False
#     else:
#         return True

# def convert_media_to_dict(item):
#     try:
#         if not check_media(item):
#             return {}
        
#         if "Author" not in item:
#             item["Author"] = ""
        
#         if "Description" not in item:
            
#             item["Description"] = ""
            
#         if "unknown" in (item["Title"].lower()):
#             return {}

#         if "unknown" in (item["Author"].lower()):
#             item["Author"] = ""
        
#         title = google_result[item["Title"]]
#         author = "" if item["Author"] == "" else google_result[item["Author"]]
#         image = google_image_result[item["Title"]]
#         result = {
#             "Category": item["Category"],
#             "Title": item["Title"],
#             "Title_Source": title,
#             "Author": item["Author"],
#             "Author_Source": author,
#             "Description": item['Description'],
#             "Image": image,
#             "Launch_URL": title,
#             "Key": 'Author'
#         }
#         return result
#     except Exception as e:
#         print(e)
#         result = {
#             "Category": "OpenAI Server Error",
#             "Title": "OpenAI Server Error",
#             "Title_Source": "",
#             "Author": "OpenAI Server Error",
#             "Author_Source": "",
#             "Description": "OpenAI Server Error",
#             "Image": "",
#             "Launch_URL": "",
#             "Key":""
#         }
#         print("convert media to dict error!")
#         return result

# def convert_place_to_dict(item):
#     try:
#         if not check_place(item):
#             return {}
        
#         if "Subtitle" not in item:
#             item["Subtitle"] = ""
        
#         if "Description" not in item:
#             item["Description"] = ""
        
#         if "unknown" in (item["Title"].lower()):
#             return {}

#         if "unknown" in (item["Subtitle"].lower()):
#             item["Subtitle"] = ""
#         image = google_image_result[item["Category"] + ' ' + item["Title"]]
#         map_image = serp_result[item["Category"] + ' ' + item["Title"]]
#         result = {
#             "Category": item["Category"],
#             "Title": item["Title"],
#             "Title_Source": map_image,
#             "Author": item["Subtitle"],
#             "Author_Source": map_image,
#             "Description": item["Description"],
#             "Image": image,
#             "Launch_URL": map_image,
#             "Key": 'Subtitle'
#         }
#         return result
#     except Exception as e:
#         print(e)
#         result = {
#             "Category": "OpenAI Server Error",
#             "Title": "OpenAI Server Error",
#             "Title_Source": "",
#             "Author": "OpenAI Server Error",
#             "Author_Source": "",
#             "Description": "OpenAI Server Error",
#             "Image": "",
#             "Launch_URL": "",
#             "Key":""
#         }
#         print("convert place to dict error!")
#         return result

serp_list = []
serp_result = ""
google_list = []
google_image_list = []
google_result = ""
google_image_result = []

# def insert_item_to_serp_list(item):
#     if check_place(item):
#         serp_list.append(item["Category"] + ' ' + item["Title"])
#         google_image_list.append(item["Category"] + ' ' + item["Title"])
    
# def insert_item_to_google_list(item):
#     if check_media(item):
#         google_list.append(item["Title"])
#         if "Author" in item:
#             google_list.append(item["Author"])
#         google_image_list.append(item["Title"])            

cx = os.getenv("CX_ID")

async def fetch_google_results(session, query, flag):
    params = {
        'q': query,
        'cx': cx,
        'key': os.getenv("GOOGLE_API_KEY"),
    }
    if flag:
        params['searchType'] = 'image'
        params['num'] = 3
    #print("fetch_start")
    try:
        async with session.get("https://www.googleapis.com/customsearch/v1", params=params) as response:
            results = await response.json()
        #print("results: ", results)
        # print("query: ", query, "  result: ", results['items'][0]['link'])
        if flag:
            return results['items'][0]['link']
            # print("image: ", results['items'][0]['link'])
        else:
            return results['items'][0]['link']
            # print("google: ", results['items'][0]['link'])
    except:
        if flag:
            return "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
        else:
            return "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
    
async def fetch_serp_results(session, query):
    try:
        params = {
            'api_key': os.getenv("SERP_API_KEY"),      # your serpapi api key: https://serpapi.com/manage-api-key
            "engine": "google_maps",
            "type": "search",  # from which device to parse data
            'q': query, # search query
        }
        
        async with session.get('https://serpapi.com/search.json', params=params) as response:
            results = await response.json()
        # print(results)

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
            
            async with session.get('https://serpapi.com/search.json', params=params) as response:
                results = await response.json()

            map_url = results['search_metadata']['google_maps_url']
            if substring_to_replace in map_url:
                map_url = map_url.replace(substring_to_replace, substring_to_replace + f"@{lat},{lng},17z/")
            return  map_url
            #print(serp_result[query])
    except:
        return "https://www.google.com/maps/place/Granite/@38.038073,-75.7687759,3z/data=!4m10!1m2!2m1!1sgranite+restaurant+paris!3m6!1s0x47e66f1a1fb579eb:0x265362fbe8c6f7b5!8m2!3d48.8610438!4d2.3419215!15sChhncmFuaXRlIHJlc3RhdXJhbnQgcGFyaXNaGiIYZ3Jhbml0ZSByZXN0YXVyYW50IHBhcmlzkgEXaGF1dGVfZnJlbmNoX3Jlc3RhdXJhbnSaASRDaGREU1VoTk1HOW5TMFZKUTBGblNVTlNYMk54VFRkM1JSQULgAQA!16s%2Fg%2F11ny2076x0?entry=ttu"

async def getUrl_for_profile(inputType, item):
    async with aiohttp.ClientSession() as session:
        tasks = []
        if inputType == 'media':
            task = asyncio.ensure_future(fetch_google_results(session, item[2], 0)) #linkUrl
            tasks.append(task)
            task = asyncio.ensure_future(fetch_google_results(session, item[1], 1)) #imageUrl
            tasks.append(task)
        else:
            param = item[0] + ' ' + item[1]
            task = asyncio.ensure_future(fetch_serp_results(session, param)) #linkUrl
            tasks.append(task)
            task = asyncio.ensure_future(fetch_google_results(session, param, 1)) #imagUrl
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

# async def get_all_url_for_profile():
#     print(len(google_list))
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for query in serp_list:
#             task = asyncio.ensure_future(fetch_serp_results(session, query))
#             tasks.append(task)
#         for query in google_list:
#             task = asyncio.ensure_future(fetch_google_results(session, query, 0))
#             tasks.append(task)
#         for query in google_image_list:
#             task = asyncio.ensure_future(fetch_google_results(session, query, 1))
#             tasks.append(task)
#         results = await asyncio.gather(*tasks)

# async def update_answer(sub_answer):
#     answer = []
#     try:
#         if 'media' in sub_answer:
#             for item in sub_answer['media']:
#                result = insert_item_to_google_list(item)
#         if 'place' in sub_answer:
#             for item in sub_answer['place']:
#                 result = insert_item_to_serp_list(item)
        
#         await get_all_url_for_profile()
#         print("here")
#         if 'media' in sub_answer:
#             for item in sub_answer['media']:
#                 result = convert_media_to_dict(item)
#                 if not result:
#                     continue
#                 else:
#                     answer.append(result)
#         if 'place' in sub_answer:
#             for item in sub_answer['place']:
#                 result = convert_place_to_dict(item)
#                 if not result:
#                     continue
#                 else:
#                     answer.append(result)
#         #print(answer)
#         return answer
#     except Exception as e:
#         print(e)
#         print("update answer error!")
#         return []

async def formatItem(inputType, item):
    results = await getUrl_for_profile(inputType, item)
    itemBlock = {
        'Category': item[0],
        'Title': item[1],
        'Author': item[2],
        'Description': item[3],
        'LaunchUrl': results[0],
        'Image': results[1]
    }
    return itemBlock



# async def get_structured_answer(context: str):
#     # Step 1: send the conversation and available functions to GPT
#     start_time = time.time()
#     # instructor = f"""
#     #     Get the mentioned media and place information from the body of the input content.
#     #     You have to provide me all of the mentioned medias and places such as book, movie, article, poscast, attractions, restaurant, museum, hotel, Tourist destination.
#     #     And then provide me detailed information about the category, author(only for media), subtitle(only for place), title, description about each media and place with your knowledge.
#     #     Don't forget to output author and description for each media.
#     #     Don't forget to output subtitle and description for each media.
#     #     You have to analyze below content carefully and then extract all medias and places mentioned in that content.
#     #     You shouldn't miss any one of the media and place such as book, movie, article, poscast, attractions, restaurant, museum, hotel, Tourist destination.
#     #     But you should extract medias both title and author of which you know already.
#     #     And you should extract all places.
#     # """

#     instructor = f"""
#         Get the media and places information from input content.
#     """
#     functions = [
#         {
#             'name': 'extract_info',
#             'description': f"{instructor}",
#             'parameters': {
#                 'type': 'object',
#                 'properties': {
#                     "media": {
#                         'type': 'array',
#                         # 'description': "Extract all of the mentioned medias such as book, movie, article, podcast in the body of the input text and description about them with your knowledge. All items must have Category, Title, Author, Description properties.",
#                         'description': "Extract all of the mentioned media you find from the input content such as book, movie, article, podcast in the input text and description about them with your knowledge. Each item must have Category, Title, Author(only for media, neccessary), Description(perhaps it would be your knowledge) properties.",
#                         'items': { 
#                             'type': 'object',
#                             'properties': {
#                                 'Category': {
#                                     'type': 'string',
#                                     'description': 'The most suitable category of the media. Such as book, movie, article, podcast.'
#                                 },
#                                 'Title': {
#                                     'type': 'string',
#                                     'description': "This item can't contain the content of not specified or not mentioned but only exact name of title for this media. You must come up with it with your own knowledge only if title of which is not mentioned in the input context. If you don't know the exact title, you should print 'unknown'."
#                                 },
#                                 'Author': {
#                                     'type': 'string',
#                                     'description': "In case of movie please provide any director or creator. Don't say you don't know it. You must come up with it with your own knowledge if author of which is not mentioned in the input context. If you don't know the exact author, you should find the Google search and extrach accurate author and if there is no result even in Google then print 'unknown'."
#                                 },
#                                 # 'Description': {
#                                 #     'type': 'string',
#                                 #     'description': "Detailed description about each media mentioned in input text. This item must contain detailed description about each media. Output as much as possible with your own knowledge as well as body of above text."
#                                 # },
#                             }
#                         }
#                     },
#                     "place": {
#                         'type': 'array',
#                         # 'description': "Extract all of the mentioned places such as retaurant, hotel, museum, Tourist destination in the body of the input text and description about that with your knowledge.  All items must have Category, Title, Subtitle, Description properties.",
#                         'description': "Extract all of the mentioned places you find from the input content such as retaurant, hotel, museum, Tourist destination in the body of the input content and description about them with your knowledge. Each item must have Category, Title, Subtitle, Description properties." ,
#                         'items': {
#                             'type': 'object',
#                             'properties': {
#                                 'Category': {
#                                     'type': 'string',
#                                     'description': 'The most suitable category of the place. Such as retaurant, hotel, museum, Tourist destination and etc. '
#                                 },
#                                 'Title': {
#                                     'type': 'string',
#                                     'description': "This item can't contain the content of not specified or not mentioned but only exact name for this place. But don't say unknown or you don't know it. You must come up with it with your own knowledge only if title of which is not mentioned in the input context. If you don't know the exact title, you should print 'unknown'."
#                                 },
#                                 'Subtitle': {
#                                     'type': 'string',
#                                     'description': "Suitable subtitle of given place such as simple introduction. If this subtitle doesn't mentioned in the input, you should create with your knowledge. For example, for the hotel, it can be 5-star tourist hotel and for restaurant, it can be Haute French restaurant."
#                                 },
#                                 # 'Description': {
#                                 #     'type': 'string',
#                                 #     'description': "Detailed description about each place mentioned in input text. This item must contain detailed description about each place. Output as much as possible with your own knowledge as well as body of above text."
#                                 # },
#                             }
#                         }
#                     }
#                 }

#             }
#         },
#     ]

#     print('here2')

#     try:
#         response = client.chat.completions.create(
#             model='gpt-4-1106-preview',
#             max_tokens=2000,
#             messages=[
#                 {'role': 'system', 'content': instructor},
#                 # {'role': 'user', 'content': f"""
#                 #     This is the input content you have to analyze.
#                 #     {context}
#                 #     Please provide me the data about places and media such as books, movies, articles, podcasts, attractions, restaurant, hotel, museum,  mentioned above.
#                 #     Please output the data with your own knowledge focusing on category, title, author, subtitle.
                    
#                 # """}
#                 {'role': 'user', 'content': f"""
#                     This is the input content you have to analyze.
#                     {context}                    
#                 """}
#             ],
#             seed=2425,
#             functions=functions,
#             function_call={"name": "extract_info"}
#         )
#         response_message = response.choices[0].message
#         system_fingerprint = response.system_fingerprint
#         print(system_fingerprint)
#         current_time = time.time()
#         print("Elapsed Time: ", current_time - start_time)
#         if hasattr(response_message, "function_call"):
#             # print("response_message: ",
#             #       response_message.function_call.arguments)
#             json_response = json.loads(
#                 response_message.function_call.arguments)
#             print(json_response)
#             answer = await update_answer(json_response)

#             return {"transcript": transcript, "media": answer}
#         else:
#             print("function_call_error!\n")
#             return {}
#     except Exception as e:
#         print(e)
#         print("hello")
#         return {}

async def generate_gpt_chunks(context: str):
    # Step 1: send the conversation and available functions to GPT
    #start_time = time.time()
    system_content = """
        Get the media and place from the input content in json.
        Don't forget media has author, not subtitle and place has subtitle, not author.
        Don't forget the author should be one of the person's name and if there is title of item, then author must be existed from your knowledge.
        If you can't find the title not only in the input content but also from your knowledge, then output 'unknown'. But 'unknown' should be the most special option you have.
    """  
    try:
        response = client.chat.completions.create(
            model='gpt-4-1106-preview',
            max_tokens=2000,
            messages=[
                {'role': 'system', 'content': system_content},
                {'role': 'user', 'content': f"This is the input content you have to analyze.{context}" +
"""
Please extract the following information from the given text as json type.
In the input, there will be medias such as books, movies, articles, podcasts, attractions and places such as restaurant, museum, hotel, Tourist destination, bars.
For media, please output category, title, author(must inclued), description, and if some of properties of each item are not mentioned in the input content, then come up with them using your knowledge.
Each property of each item must be only the famous one.  But the description especially must be in the input content and should be the part of the input, not your knowledge.
For place, please output category, title, subtitle(must include), and one sentence description even if some of properties of each item are not mentioned in the input content, then come up with them using your knowledge. But description especially must be in the input content and should be the part of the input, not your knowledge.
If you can't find the title not only in the input content but also from your knowledge, then output 'unknown'. But 'unknown' should be the most special option you have.
Don't forget media has author, not subtitle and place has subtitle, not author.
Don't forget the author should be one of the person's name and if there is title of item, then author must be existed from your knowledge.
Sample output is below:
{"media":[["book","Fight Club","Chuck Palahniuk","Abcdefefddd"],["book","unknown","Sue Johnson","Abcdefefddd"]],"place":[["bookstore","The Painted Porch","Historical bookstore in Bastrop, Texas","This bookstore"]]}
"""}
            ],
            seed=2425,
            temperature = 0.7,
            response_format={"type": "json_object"},
            stream=True
        )
        #response_message = response.choices[0].message.content
        for chunk in response:
            yield chunk
        # json_response = json.loads(response_message)
        # print(json_response)
        # system_fingerprint = response.system_fingerprint
        #print("Elapsed Time: ", time.time() - start_time)
        #answer = ""#await update_answer(json_response)
        #return {"transcript": transcript, "media": answer}
        #yield {"transcript": transcript, "media": answer}
    except Exception as e:
        print(e)
        print("hello")
        yield {}

# def extract_data(context: str):
#     global transcript, serp_list, google_image_list, google_list
#     serp_list = []
#     google_image_list = []
#     google_list = []
#     transcript = context[:250]
#     transcript += "..."
#     length = len(context)
#     sub_len = 74000
#     current = 0
#     result = ""
#     time_init = time.time()

#     while current < length:
#         start_time = time.time()
#         start = max(0, current - 50)
#         end = min(current + sub_len, length - 1)
#         current += sub_len
#         subtext = context[start: end]
#         instructor = f"""
#             This is context from with you have to analyze and extract information about medias, places.
#             {subtext}
#             Please analyze above context carefully and then extract information about medias and places such as book, movie, article, podcast and places such as attractions, restaurant, bar, museum, Tourist destination etc that are mentioned in the context in detail.
#             Please output the data as much as possible with your own knowledge focusing on category, title, author, subtitle, description.
#             Don't output subtitle for medias.
#             Don't output author for places.
#             But you should output subtitle, description for places.
#             And you should output author, description for medias.
#             But you should output only the medias and places whose title was mentioned in the given context.
#             And If you don't know the exact name of author of extracted media, you should output as 'unknown'.
#             When you output description about each media and place, please output as much as possible with several sentence about that media and place.
#             Please check each sentence one by one so that you can extract all books, movies, articles, podcasts, attractions, restaurant, museum, hotel, Tourist destination, attractions, etc discussed or mentioned or said by someone in the context above.        
#         """
        
#         #print("tiktoken_len: ", tiktoken_len(instructor), '\n')
#         try:
#             response = client.chat.completions.create(
#                 model='gpt-4-1106-preview',
#                 max_tokens=2500,
#                 messages=[
#                     {'role': 'system', 'content': instructor},
#                     {'role': 'user', 'content': f"""
#                         Please provide me extracted data about books, movies, articles, podcasts, attractions, restaurant, museum, hotel, Tourist destination mentioned above.
#                         Output one by one as a list looks like below format.

#                         --------------------------------
#                         This is sample output format.

#                         Category: Book
#                         Title: Stolen Focus
#                         Author: Johann Hari
#                         Description: This book by Johann Hari explores the issue of how our attention is being constantly stolen by various distractions. He delves into the impact of this on our capability to think and work efficiently and on fulfilling our lives. The author has conducted extensive research and interviews with experts in fields like technology, psychology, and neuroscience to support his findings.

#                         Category: Podcasts
#                         Title: unknown
#                         Author: unknown
#                         Description: This particular episode on Dr. Andrew Huberman's podcast is not specified, but he mentions having various guests on.
                        
#                         Category: Movie
#                         Title: "Mad Men".
#                         Author: unknown
#                         Description: This is an American period drama television series. The series ran on the cable network AMC from 2007 to 2015, consisting of seven seasons and 92 episodes. Its main character, Don Draper, is a talented advertising executive with a mysterious past. This is the character with whom Rob Dyrdek identified himself in the context.
                        
#                         Category: Museums
#                         Title: Louvre Museum
#                         Subtitle: Museum in Paris, France
#                         Description: The Louvre, or the Louvre Museum, is a national art museum in Paris, France
                        
#                         Category: Attractions
#                         Title: Eiffel Tower
#                         Subtitle: Tower in Paris, France
#                         Description: The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.
#                         ...
#                     """}
#                 ],
#                 # stream=True
#             )
            
            
#             result += response.choices[0].message.content + '\n'
#             current_time = time.time()
#             #print("Elapsed time: ", current_time - start_time)

#             delta_time = current_time - start_time
#             if current >= length:
#                 if tiktoken_len(instructor + result) > 70000:
#                     time.sleep(max(0, 60-delta_time))
#         except Exception as e:
#             print("extract data error!")
#             print(e)
#             current = max(0, current - sub_len)
#             current_time = time.time()
#             if current_time - time_init > 600:
#                 return result
#             time.sleep(60)
#             continue
#     return result


# async def complete_profile(context: str, constantResponse: str, url: str):
    # result = await get_structured_answer_not_functionCalling(context)

async def stream_media(context: str, constantResponse: str, url: str):
    [videoTitle, videoUploader, videoAvatarUrl] = constantResponse
    print("here")
    # Initialize the response format
    response_data = {
        "url": url,
        "title": videoTitle,
        "author": videoUploader,
        "avatar": videoAvatarUrl,
        "sharelink": f"list02ProductsShare?url={url}",
        "media": [],
        "place": [],
    }

    items_string = ""
    t = time.time()
    async for chunk in generate_gpt_chunks(context):  # Replace with your GPT chunk generator
        # Parse chunk and append to current_item
        # ... (implement parsing logic)
        chunk_string = chunk.choices[0].delta.content
        if chunk_string:
            items_string += chunk_string
            if ']' in chunk_string:
                if not '"place"' in items_string:
                    item_string = '[' + items_string.split('[')[-1].split(']')[0] + ']'
                    item_string = item_string.replace('\n', '')
                    item_string = item_string.replace('    ', '')
                    if item_string == "[]":
                        item = {}
                    else:
                        item = await formatItem('media', ast.literal_eval(item_string))
                    if item not in response_data['media']:
                        print(item)
                        print(time.time()-t)
                        t = time.time()           
                        response_data["media"].append(item)
                        yield json.dumps(response_data.copy()).encode("utf-8")  # Yield updated response
                else:
                    item_string = '[' + items_string.split('[')[-1].split(']')[0] + ']'
                    item_string = item_string.replace('\n', '')
                    item_string = item_string.replace('    ', '')
                    if item_string == "[]":
                        item = {}
                    else:
                        item = await formatItem('place', ast.literal_eval(item_string))
                    if item not in response_data['place']:
                        print(item)
                        print(time.time()-t)
                        t = time.time()
                        response_data["place"].append(item)
                        yield json.dumps(response_data.copy()).encode("utf-8")  # Yield updated response
