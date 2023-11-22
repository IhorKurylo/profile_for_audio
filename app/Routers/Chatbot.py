from fastapi import APIRouter, Form, UploadFile, File
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube, get_title_from_youtube
from app.Utils.extract_keywords import extract_data, complete_profile
from app.Models.Chatbot_Model import check_already_searched, insert_url_database
import time

router = APIRouter()


def pipeline(value, functions):
    result = value
    for func in functions:
        result = func(result)
    return result


@router.post("/extract_mentioned_data")
def extract_mentioned_data(url: str = Form(...)):
    print(url)
    if url == "":
        return {}
    # search_result = check_already_searched(url)
    # if search_result != None:
    #     return search_result
        
    print("start")
    start_time = time.time()
    video_id = extract_video_id(url)
    if (video_id == None):
        return {}
    # print("video_id: ", video_id)
    title = get_title_from_youtube(video_id)
    functions = [get_transcript_from_youtube, extract_data, complete_profile]
    result = pipeline(video_id, functions)
    if 'media' in result:
        result['media'] = sorted(result['media'], key=lambda x: x['Category'])
        current_category = "---"
        for item in result['media']:
            if item["Category"] == current_category:
                item["Category"] = ""
            else:
                current_category = item["Category"]
    result['title'] = title
    result['url'] = url
    result['share_link'] = f"https://recc.ooo/list02ProductsShare?url={url}"

    current_time = time.time()
    print("Total Time: ", current_time - start_time)
    # insert_url_database(url, result)
    return result


@router.post("/transcript-audio-file")
async def transcript_audio_file(file: UploadFile = File(...)):
    print(file.filename)
    return file.filename + " - goldrace"
