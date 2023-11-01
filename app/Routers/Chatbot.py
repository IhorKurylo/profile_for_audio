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
    result = {'transcript': '- Welcome to the Lifespan podcast, where we discuss the science of aging and how to be healthier\nat ', 'media': [{'Category': 'Podcast', 'Title': 'Lifespan podcast', 'Title Source': 'https://www.amazon.com/Stolen-Focus-Attention-Think-Deeply/dp/0593138511', 'Author': 'David Sinclair and Matthew LaPlante', 'Author Source': 'https://www.amazon.com/Stolen-Focus-Attention-Think-Deeply/dp/0593138511',
                                                                                                                                                'Description': 'The Lifespan podcast, hosted by David Sinclair and Matthew LaPlante, explores the science behind aging and longevity. In these episodes, they discuss various methods and substances that have shown potential in extending lifespan and improving health. They cover topics like resveratrol, Metformin, NMN, and other supplements. The discussion provides listeners with knowledge on the latest scientific discoveries and health strategies.', 'Image': 'https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg'}], 'title': 'NMN, NR, Resveratrol, Metformin & Other Longevity Molecules | Lifespan with Dr. David Sinclair #4'}
    # print(result)
    # # complete_profile(context)
    # print("here")
    # current_time = time.time()
    # print("Total Time: ", current_time - start_time)
    # # json_data = json.dumps(result)
    return result
