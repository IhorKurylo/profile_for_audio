from fastapi import APIRouter, Form, UploadFile, File
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube, get_title_from_youtube
from app.Utils.extract_keywords import complete_profile, update_answer
from app.Models.Chatbot_Model import check_already_searched, insert_url_database
from app.Utils.elevenlabs import text_to_speech
import time
import asyncio
import os
import shutil
import youtube_dl
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
    # video_author = extract_video_author(url)
    with youtube_dl.YoutubeDL({}) as ydl:
        video = ydl.extract_info(url, download=False)
        # video_author = video.author
        # title = video.title
        print(video.get("uploader", None),  video.get("id", None), video.get("title", None))


    if (video_id == None):
        return {}
    
    title = get_title_from_youtube(video_id)
    print("Title Time: ", time.time() - start_time)

    transcript = get_transcript_from_youtube(video_id)
    print(time.time() - start_time)
    # print(transcript)
    # content = extract_data(transcript)
    result = asyncio.run(complete_profile(transcript))
    #print(result)
    if 'media' in result:
        # result['media'] = sorted(result['media'], key=lambda x: x['Category'])
        current_category = "---"
        for item in result['media']:
            if item["Category"] == current_category:
                item["Category"] = ""
            else:
                current_category = item["Category"]
    result['author'] = video_author
    result['title'] = title
    result['url'] = url
    result['share_link'] = f"https://recc.ooo/list02ProductsShare?url={url}"

    current_time = time.time()
    print("Total Time: ", current_time - start_time)
    # insert_url_database(url, result)
    return result


@router.post("/transcript-audio-file")
async def transcript_audio_file(file: UploadFile = File(...)):
    text_to_speech()
    print(file.filename)

    UPLOAD_DIRECTORY = "./data"
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file.filename + " - goldrace"
