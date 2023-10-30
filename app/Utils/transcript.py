from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
import openai
from dotenv import load_dotenv
import os
import tiktoken
import time
import json
from app.Utils.google_API import search

load_dotenv()
tokenizer = tiktoken.get_encoding('cl100k_base')


def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)


def extract_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)

    if parsed_url.netloc == 'youtu.be':
        # The video ID is the path itself for 'youtu.be' URLs
        return parsed_url.path[1:]
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            # The video ID is in the 'v' query parameter for '/watch' paths
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path[:7] == '/embed/':
            # The video ID is the path itself for '/embed/' paths
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            # The video ID is the path itself for '/v/' paths
            return parsed_url.path.split('/')[2]
    # Return None if no video ID could be extracted
    return None


def get_transcript_from_youtube(video_id: str):
    # nltk.download('punkt')
    # video_id = extract_video_id(url)
    # Get the transcript of the video
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([segment['text'] for segment in transcript_list])
    sentences = nltk.sent_tokenize(transcript)
    context = ""
    with open("./data/script.txt", "w") as txt_file:
        for sentence in sentences:
            txt_file.write(sentence + '.\n')
            context += sentence + '.\n'
    return context


def convert_to_context(item):
    result = f"""
Category: {item["Category"]}
Title: {item["Title"]} {"" if (item["Title"] == "N/A" or item["Title"] == "Not specified") else f'(source: {search(item["Title"])})'}
Author: {item["Author"]} {"" if (item["Author"] == "N/A" or item["Author"] == "Not specified") else f'(source: {search(item["Author"])})'   }
Description:
{item['Description']}
    """
    return result


def update_answer(sub_answer):
    global final_answer
    with open("./data/answer.txt", "w") as txt_file:
        for item in sub_answer['media']:
            answer = convert_to_context(item)
            print(answer)
            txt_file.write(answer)


def run_conversation(context: str):
    # Step 1: send the conversation and available functions to GPT

    instructor = f"""
        Get the mentioned media information from the body of the input content.
        You have to provide me all of the mentioned medias such as book, movie, article, poscast.
        And then provide me detailed information about the category, author, title, description about each media with your knowledge.
        You have to analyze below content carefully and then extract all medias mentioned in that content.
        You shouldn't miss any one of the media such as book, movie, article, poscast.
        
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
                        'description': "All of the mentioned medias such as book, movie, article, podcast in the body of the input text and description about that with your knowledge.",
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Category': {
                                    'type': 'string',
                                    'description': 'The most suitable category of the media. Such as book, movie, article, podcast.'
                                },
                                'Title': {
                                    'type': 'string',
                                    'description': "Exact title of the media. But don't say unkown or you don't know it. You must output with your own knowledge in case of unkown. If no author is specified, print 'N/A'."
                                },
                                'Author': {
                                    'type': 'string',
                                    'description': "Author of this media. Don't say unkown or you don't know it. You must output with your own knowledge in case of unkown. If no author is specified, print 'N/A'."
                                },
                                'Description': {
                                    'type': 'string',
                                    'description': 'Detailed description about the media. Output as much as possible with your own knowledge as well as body of above text.'
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
    if response_message.get("function_call"):
        json_response = json.loads(
            response_message['function_call']['arguments'])
        print(json_response)
        update_answer(json_response)
        return json_response
    else:
        print("function_call_error!\n")
        return {}


def extract_data(context: str):
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
                        
                        Book:
                        "Stolen Focus" by Johann Hari
                        This book by Johann Hari explores the issue of how our attention is being constantly stolen by various distractions. He delves into the impact of this on our capability to think and work efficiently and on fulfilling our lives. The author has conducted extensive research and interviews with experts in fields like technology, psychology, and neuroscience to support his findings.
                        
                        Podcasts:
                        "Huberman Lab" by Dr. Andrew Huberman, this particular episode on Dr. Andrew Huberman's podcast is not specified, but he mentions having various guests on.
                        
                        Movie:
                        There's a mention of the TV show "Mad Men".
                        This is an American period drama television series created by Matthew Weiner and produced by Lionsgate Television. The series ran on the cable network AMC from 2007 to 2015, consisting of seven seasons and 92 episodes. Its main character, Don Draper, is a talented advertising executive with a mysterious past. This is the character with whom Rob Dyrdek identified himself in the context.
                        ...
                    """}
                ],
                # stream=True
            )
            result += response.choices[0].message.content + '\n'
            current_time = time.time()
            delta_time = current_time - start_time
            # print(response.choices[0].message.content + '\n')
            time.sleep(max(0, 60-delta_time))
            current_time = time.time()
            print("Elapsed time: ", current_time - start_time)

        except Exception as e:
            print(e)
    return result


def complete_profile(context: str):
    print("context: ", context, '\n')
    print("---------------------------------------------------\n")
    run_conversation(context)
    return
    result = ""
    instructor = f"""
        All information about books, movies, articles, podcasts, etc mentioned in a particular talk is listed in the context given below.
        After carefully analyzing the below context, you need to categorize the information by topic, such as books, movies, articles, podcasts, etc.
        For that you have to check each sentence of below context one by one and extract all mentions about books, movies, articles, podcasts, etc.
        Then based on that information, complete the profile of each subject.
        Additionally, you must write a detailed profile for each topic based on the information given and your own knowledge about the topic.
        Don't say there is no mention about that topic.(In that case please describe with your own knowledge)
        Please ignore the sentences that says there is no mention about specific subject in the context.
        Don't miss any brief mentions of books, movies, articles, podcasts, etc from given context.
        In other word, all information about the books, movies, articles, podcasts, etc from given context below must be listed in your output.
        Avoid outputting too much context for each profile.
        
        --------------------------
        This is the given context you can refer to and it is containing information about books, movies, articles, podcasts, etc
        {context}
        
        Sample output like this.
        - Book
            "Stolen Focus":
            This book written by Johann Hari. The book delves into the modern world's crisis of attention, where our focus is constantly being pulled in different directions, leading to feelings of distraction and dissatisfaction. The author investigates how this state of constant distraction impacts our ability to think, work, and live fulfilling lives. He also provides insights into how we can reclaim our attention and focus. The book is based on extensive research and interviews with experts in various fields including technology, psychology, and neuroscience.
            
        - Movie
            "Mad Men":
            This is an American television series that aired from 2007 to 2015. The show was created by Matthew Weiner and produced by Lionsgate Television. The setting is a prestigious ad agency in 1960s New York City and it primarily focuses on the mysterious and talented ad executive Don Draper.
            The series is known for its historical authenticity, visual style, and character development. It explores themes such as the changing social mores of the United States during the 1960s, the tobacco industry, alcoholism, sexism, feminism, and the American Dream.
            "Mad Men" received critical acclaim and won many awards, including 16 Emmys and 5 Golden Globes. It is often cited as one of the greatest television shows of all time. The main cast includes Jon Hamm, Elisabeth Moss, Vincent Kartheiser, January Jones, Christina Hendricks, and John Slattery, among others.

        - Article
            ...


    """
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            max_tokens=1000,
            messages=[
                {'role': 'system', 'content': instructor},
                {'role': 'user', 'content': f"""
                    Please provide me profiles for each topics such as books, movies, articles, podcasts, etc.
                    All names and titles of books, movies, articles, podcasts, etc mentioned in the given context above should be listed in your output.
                """}
            ],
            # stream=True
        )
        print(response.choices[0].message.content + '\n')
        result = response.choices[0].message.content + '\n'
        return result

    except Exception as e:
        print(e)
