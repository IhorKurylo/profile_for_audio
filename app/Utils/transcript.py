from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from dotenv import load_dotenv
import os
import tiktoken
from googleapiclient.discovery import build

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


def get_title_from_youtube(video_id: str):
    api_key = os.getenv("YouTube_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    title = response['items'][0]['snippet']['title']
    # print("title: ", title)
    return title


def get_transcript_from_youtube(video_id: str):
    # nltk.download('punkt')
    # video_id = extract_video_id(url)
    # Get the transcript of the video

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([segment['text'] for segment in transcript_list])
    sentences = nltk.sent_tokenize(transcript)
    context = ""
    # with open("./data/script.txt", "w") as txt_file:
    for sentence in sentences:
        # txt_file.write(sentence + '.\n')
        context += sentence + '.\n'
    return context


# def complete_profile(context: str):
#     print("context: ", context, '\n')
#     print("---------------------------------------------------\n")
#     run_conversation(context)
#     return
