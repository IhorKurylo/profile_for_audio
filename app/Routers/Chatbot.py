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
    if url == "https://www.youtube.com/watch?v=_WNL6dUFRiA&list=PLDBZgkgeoMJhpMxQ0sqpdhHYv4lZOf0J8&index=7":
        return {}
    print("start")
    start_time = time.time()
    video_id = extract_video_id(url)
    print("video_id: ", video_id)
    title = get_title_from_youtube(video_id)
    functions = [get_transcript_from_youtube, extract_data, complete_profile]
    result = pipeline(video_id, functions)
    result['title'] = title
    # result = {
    #     "transcript": "- Welcome to the Lifespan podcast, where we discuss the science of aging and how to be healthier\nat ",
    #     "media": [
    #         {
    #             "Category": "Podcast",
    #             "Title": "Lifespan podcast",
    #             "Title Source": "https://www.lifespanpodcast.com/",
    #             "Author": "David Sinclair, Matthew LaPlante",
    #             "Author Source": "https://chass.usu.edu/journalism/news/articles/laplantebestseller2019",
    #             "Description": "The Lifespan podcast is hosted by David Sinclair, a professor at Harvard Medical School and co-director of the Paul F. Glenn Center for Aging Research, along with his cohost, Matthew LaPlante. In the podcast, they discuss the science of aging and ways to promote better health at any stage in life. They endeavor to address the most pressing questions about lifestyle changes and supplements that can slow, stop, and reverse the aging process. A specific episode focuses on the use of supplements and the medical benefits of certain molecules.",
    #             "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
    #         },
    #         {
    #             "Category": "Podcast",
    #             "Title": "Lifespan Podcast",
    #             "Title Source": "https://www.lifespanpodcast.com/",
    #             "Author": "David Sinclair",
    #             "Author Source": "https://sinclair.hms.harvard.edu/people/david-sinclair",
    #             "Description": "The Lifespan podcast is hosted by David Sinclair, a scientist, entrepreneur, and author known for his research on aging and lifespan extension. In this episode, he discusses various drugs and supplements that can potentially contribute to anti-aging benefits, with topics ranging from resveratrol to glucose sensitivity, insulin, longevity, and more. As always, he emphasizes the importance of consulting with a physician before trying any new treatment or intervention.",
    #             "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
    #         }
    #     ],
    #     "title": "YouTube Video",
    # }
    current_time = time.time()
    print("Total Time: ", current_time - start_time)
    return result
