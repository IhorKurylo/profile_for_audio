from fastapi import APIRouter, Form
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube, get_title_from_youtube
from app.Utils.extract_keywords import extract_data, complete_profile
import time

router = APIRouter()


def pipeline(value, functions):
    result = value
    for func in functions:
        result = func(result)
    return result


@router.post("/extract_mentioned_data")
def extract_mentioned_data(url: str = Form(...)):
    if url == "":
        return {}
    print("start")
    start_time = time.time()
    video_id = extract_video_id(url)
    if (video_id == None):
        return {}
    # print("video_id: ", video_id)
    title = get_title_from_youtube(video_id)
    functions = [get_transcript_from_youtube, extract_data, complete_profile]
    result = pipeline(video_id, functions)
    result['title'] = title
    current_time = time.time()
    print("Total Time: ", current_time - start_time)
    return result
