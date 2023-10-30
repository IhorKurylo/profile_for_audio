from fastapi import APIRouter, Form
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube, extract_data, complete_profile
import time
import asyncio

router = APIRouter()


def pipeline(value, functions):
    result = value
    for func in functions:
        result = func(result)
    return result


@router.post("/extract_mentioned_data")
def extract_mentioned_data(url: str = Form(...)):
    start_time = time.time()
    functions = [extract_video_id, get_transcript_from_youtube, extract_data, complete_profile]
    result = pipeline(url, functions)
    # print("here")
    # extract_data(result)
    # # asyncio.run(extract_data(result))
    # result = complete_profile(context)
    current_time = time.time()
    print("Total Time: ", current_time - start_time)
    return result
