from fastapi import APIRouter, Form
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube, get_title_from_youtube
from app.Utils.extract_keywords import extract_data, complete_profile
import time
import asyncio
import json

router = APIRouter()


def pipeline(value, functions):
    result = value
    for func in functions:
        result = func(result)
    return result


# @router.post("/extract_mentioned_data")
# def extract_mentioned_data(url: str = Form(...)):
#     start_time = time.time()
#     functions = [extract_video_id, get_transcript_from_youtube, extract_data]
#     pipeline(url, functions)
#     # print("here")
#     # extract_data(result)
#     # # asyncio.run(extract_data(result))
#     # result = complete_profile(context)
#     current_time = time.time()
#     print("Total Time: ", current_time - start_time)
#     # return result


@router.post("/extract_mentioned_data")
def extract_mentioned_data(url: str = Form(...)):
    # start_time = time.time()

    # video_id = extract_video_id(url)
    # title = get_title_from_youtube(video_id)

    # functions = [get_transcript_from_youtube, extract_data, complete_profile]
    # # functions = [extract_video_id, get_transcript_from_youtube]
    # result = pipeline(video_id, functions)
    # result['title'] = title
    result = {
        "transcript": "Goldrace-Welcome to the Lifespan podcast, where we discuss the science of aging and how to be healthier\nat ",
        "media": [
            {
                "Category": "Goldrace-Podcast",
                "Title": "Goldrace-Lifespan",
                "Title Source": "https://www.amazon.com/Stolen-Focus-Attention-Think-Deeply/dp/0593138511",
                "Author": "Goldrace-David Sinclair and Matthew LaPlante",
                "Author Source": "https://www.amazon.com/Stolen-Focus-Attention-Think-Deeply/dp/0593138511",
                "Description": "Goldrace-The Lifespan podcast is hosted by David Sinclair, a leading researcher on aging, and Matthew LaPlante, a journalist. The podcast tackles different aspects of aging, health, and longevity. In each episode, they discuss different supplements and drugs that can potentially contribute to a longer and healthier life. They advise their listeners to consult with their healthcare providers before starting any new supplement regimen. They also encourage their listeners to support the show through various platforms, including YouTube, Apple Podcasts, Spotify, and Patreon.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            }
        ],
        "title": "Goldrace-NMN, NR, Resveratrol, Metformin & Other Longevity Molecules | Lifespan with Dr. David Sinclair #4"
    }
    # print(result)
    # # complete_profile(context)
    # print("here")
    # current_time = time.time()
    # print("Total Time: ", current_time - start_time)
    # # json_data = json.dumps(result)
    return result
