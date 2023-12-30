from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import StreamingResponse
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube, get_title_from_youtube
from app.Utils.extract_keywords import stream_media
from app.Models.Chatbot_Model import check_already_searched, insert_url_database
from app.Utils.elevenlabs import text_to_speech
import time
import asyncio
import os
import shutil

router = APIRouter()


# def pipeline(value, functions):
    # result = value
    # for func in functions:
    #     result = func(result)
    # return result

# @router.post("/extract_mentioned_data")
# async def extract_mentioned_data(url: str = Form(...)):

#     if url == "":
#         print("There is no url typed on..")
#         return {}
#     # search_result = check_already_searched(url)
#     # if search_result != None:
#     #     return search_result
#     video_id = extract_video_id(url)
#     if (video_id == None):
#         print("This is not a Youtube video..")
#         return {}

#     print("start")
#     start_time = time.time()

#     constantData = get_title_from_youtube(video_id)
#     title = data[0]
#     author = data[1]
#     avatar_url = data[2]
#     print("Title Time: ", time.time() - start_time)

#     transcript = get_transcript_from_youtube(video_id)
#     print(time.time() - start_time)
#     # print(transcript)
#     # content = extract_data(transcript)
#     result = asyncio.run(complete_profile(transcript))
#     #print(result)
#     if 'media' in result:
#         # result['media'] = sorted(result['media'], key=lambda x: x['Category'])
#         current_category = "---"
#         for item in result['media']:
#             if item["Category"] == current_category:
#                 item["Category"] = ""
#             else:
#                 current_category = item["Category"]
#     result['author'] = author
#     result['title'] = title
#     result['avatar'] = avatar_url
#     result['url'] = url
#     result['share_link'] = f"list02ProductsShare?url={url}"

#     current_time = time.time()
#     print("Total Time: ", current_time - start_time)
#     # insert_url_database(url, result)
#     return result

# @router.post("/transcript-audio-file")
# async def transcript_audio_file(file: UploadFile = File(...)):
#     text_to_speech()
#     print(file.filename)

#     UPLOAD_DIRECTORY = "./data"
#     file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return file.filename + " - goldrace"

@router.post("/extract_mentioned_data")
async def extract_mentioned_data(url: str = Form(...)):

    # Check the url exist
    if url == "":
        print("There is no url typed on..")
        return ""

    # Check whether it is Youtube or not
    video_id = extract_video_id(url)
    if (video_id == None):
        print("This is not a Youtube video..")
        return ""

    print("start")
    start_time = time.time()

    # Get the constant responses
    constantData = get_title_from_youtube(video_id)
    
    # Get the transcript of video
    transcript = get_transcript_from_youtube(video_id)
    print("Time to get the transcript of Youtube: ", time.time() - start_time)
    # print(transcript)

    if type(constantData) is not list:
        print(constantData)
        return ""
    else:
        return StreamingResponse(stream_media(transcript, constantData, url), media_type='text/event-stream')
    # result = asyncio.run(complete_profile(transcript))
    # #print(result)
    # if 'media' in result:
    #     # result['media'] = sorted(result['media'], key=lambda x: x['Category'])
    #     current_category = "---"
    #     for item in result['media']:
    #         if item["Category"] == current_category:
    #             item["Category"] = ""
    #         else:
    #             current_category = item["Category"]

    

    # result['author'] = author
    # result['title'] = title
    # result['avatar'] = avatar_url
    # result['url'] = url
    # result['share_link'] = f"list02ProductsShare?url={url}"

    # print("Total Time: ", time.time() - start_time)
    # return result
