from app.Utils.google_API import get_source_url, get_image_url
import time
import openai
import json
import tiktoken
from dotenv import load_dotenv

load_dotenv()

tokenizer = tiktoken.get_encoding('cl100k_base')

transcript = ''


def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)


def convert_to_dict(item):
    # print("media 2: ", item)
    if "unknown" in (item["Title"].lower()) or "unknown" in (item["Author"].lower()):
        return "--------unknown---------------"

    title = get_source_url(item["Title"])
    author = get_source_url(item["Author"])
    image = get_image_url(item["Title"])
    result = {
        "Category": item["Category"],
        "Title": item["Title"],
        "Title Source": title,
        "Author": item["Author"],
        "Author Source": author,
        "Description": item['Description'],
        "Image": image
    }
#     result = f"""
# Category: {item["Category"]}
# Title: {item["Title"]} (source: {title})
# Author: {item["Author"]} (source: {author})
# Description:
# {item['Description']}
# Image: {image}
#     """
    # print("result: ", result)
    return result


def update_answer(sub_answer):
    # with open("./data/answer.txt", "w") as txt_file:
    answer = []
    for item in sub_answer['media']:
        answer.append(convert_to_dict(item))
        # txt_file.write(answer)
    return answer


def run_conversation(context: str):
    # Step 1: send the conversation and available functions to GPT
    start_time = time.time()
    instructor = f"""
        Get the mentioned media information from the body of the input content.
        You have to provide me all of the mentioned medias such as book, movie, article, poscast.
        And then provide me detailed information about the category, author, title, description about each media with your knowledge.
        You have to analyze below content carefully and then extract all medias mentioned in that content.
        You shouldn't miss any one of the media such as book, movie, article, poscast.
        But you should extract medias both title and author of which you know already.
    """
    functions = [
        {
            'name': 'extract_media_info',
            'description': f"{instructor}",
            'parameters': {
                'type': 'object',
                'properties': {
                    "media": {
                        'type': 'array',
                        'description': "Extract all of the mentioned medias such as book, movie, article, podcast in the body of the input text and description about that with your knowledge.",
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Category': {
                                    'type': 'string',
                                    'description': 'The most suitable category of the media. Such as book, movie, article, podcast.'
                                },
                                'Title': {
                                    'type': 'string',
                                    'description': "This item can't contain the content of not specified or not mentioned but only exact name of title for this media. But don't say unknown or you don't know it. You must come up with it with your own knowledge only if title of which is not mentioned in the input context. If you don't know the exact title, you should print 'unknown'. In short, you should not print out that you do not know the exact title. In that case, print 'unown'."
                                },
                                'Author': {
                                    'type': 'string',
                                    'description': "This item can't contain the content of not specified or not mentioned but only exact name of Author for this media. Don't say unknown or you don't know it. You must come up with it with your own knowledge if author of which is not mentioned in the input context. If you don't know the exact author, you should print 'unknown'. In short, you should not print out that you do not know the exact title. In that case, print 'unown'."
                                },
                                'Description': {
                                    'type': 'string',
                                    'description': "This item can't contain the content of not specified or not mentioned but only detailed description about the media. Output as much as possible with your own knowledge as well as body of above text."
                                },

                            }
                        }
                    }

                }

            }
        }
    ]
    print('here2')

    response = openai.ChatCompletion.create(
        model='gpt-4',
        max_tokens=1000,
        messages=[
            {'role': 'system', 'content': instructor},
            {'role': 'user', 'content': f"""
                This is the input content you have to analyze.
                {context}
                Please provide me the data about medias such as books, movies, articles, podcasts mentioned above.
            """}
        ],
        functions=functions,
        function_call={"name": "extract_media_info"}
    )

    response_message = response["choices"][0]["message"]
    current_time = time.time()
    print("Elapsed Time: ", current_time - start_time)
    if response_message.get("function_call"):
        json_response = json.loads(
            response_message['function_call']['arguments'])
        # print(json_response)
        print('--------------------')
        answer = update_answer(json_response)
        return {"transcript": transcript, "media": answer}
    else:
        print("function_call_error!\n")
        return {}


def extract_data(context: str):
    global transcript
    transcript = context[:100]
    length = len(context)
    sub_len = 28000
    current = 0
    result = ""
    while current < length:
        start_time = time.time()
        start = max(0, current - 50)
        end = min(current + sub_len, length - 1)
        current += sub_len
        subtext = context[start: end]
        # print(subtext)
        instructor = f"""
            This is context from with you have to analyze and extract information about medias.
            {subtext}
            Please analyze above context carefully and then extract information about medias such as book, movie, article, podcast that are mentioned in the context in detail.
            Please output the data as much as possible with your own knowledge focusing on category, author, title, description.
            But you should output only the medias whose title was mentioned in the given context.
            And If you don't know the exact name of author of extracted media, you should output as 'unknown'.
            When you output description about each media, please output as much as possible with several sentence about that media.
            Please check each sentence one by one so that you can extract all books, movies, articles, podcasts discussed or mentioned or said by someone in the context above.        
        """

        print("tiktoken_len: ", tiktoken_len(instructor), '\n')
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4',
                max_tokens=800,
                messages=[
                    {'role': 'system', 'content': instructor},
                    {'role': 'user', 'content': f"""
                        Please provide me extracted data about books, movies, articles, podcasts mentioned above.
                        Output one by one as a list looks like below format.

                        --------------------------------
                        This is sample output format.

                        Category: Book
                        Title: Stolen Focus
                        Author: Johann Hari
                        Description:
                        This book by Johann Hari explores the issue of how our attention is being constantly stolen by various distractions. He delves into the impact of this on our capability to think and work efficiently and on fulfilling our lives. The author has conducted extensive research and interviews with experts in fields like technology, psychology, and neuroscience to support his findings.

                        Category: Podcasts
                        Title: unknown
                        Author: unknown
                        This particular episode on Dr. Andrew Huberman's podcast is not specified, but he mentions having various guests on.

                        Movie:
                        Title: "Mad Men".
                        Author: unknown
                        This is an American period drama television series. The series ran on the cable network AMC from 2007 to 2015, consisting of seven seasons and 92 episodes. Its main character, Don Draper, is a talented advertising executive with a mysterious past. This is the character with whom Rob Dyrdek identified himself in the context.
                        ...
                    """}
                ],
                # stream=True
            )
            result += response.choices[0].message.content + '\n'
            # print("context: ", result)
            current_time = time.time()
            # print(response.choices[0].message.content + '\n')
            # result = run_conversation(result)
            current_time = time.time()
            print("Elapsed time: ", current_time - start_time)
            delta_time = current_time - start_time
            time.sleep(max(0, 60-delta_time))
        except Exception as e:
            print(e)
    return result


def complete_profile(context: str):
    print("context: ", context, '\n')
    print("---------------------------------------------------\n")

    return run_conversation(context)
