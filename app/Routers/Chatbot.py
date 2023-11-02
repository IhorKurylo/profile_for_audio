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
    # start_time = time.time()
    # video_id = extract_video_id(url)
    # title = get_title_from_youtube(video_id)
    # functions = [get_transcript_from_youtube, extract_data, complete_profile]
    # result = pipeline(video_id, functions)
    # result['title'] = title
    # current_time = time.time()
    # print("Total Time: ", current_time - start_time)
    result = {
        "transcript": "Mental focus follows visual focus..\nWe have an aperture or a window on our focus..\nWhen you are exci",
        "media": [
            {
                "Category": "Book",
                "Title": "Stolen Focus",
                "Title Source": "https://www.amazon.com/Stolen-Focus-Attention-Think-Deeply/dp/0593138511",
                "Author": "Johann Hari",
                "Author Source": "https://johannhari.com/",
                "Description": "Johann Hari's 'Stolen Focus' discusses our diminishing ability to maintain attention due to various factors such as technology, stress, lack of sleep, lack of exercise, reduced connection with nature and people. The book provides insights into why people are finding it harder to focus in the current time and gives a perspective on the problem from a neuroscience angle.",
                "Image": "https://m.media-amazon.com/images/I/71z+2nHWZGL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "Huberman Lab Podcast",
                "Title Source": "https://www.hubermanlab.com/",
                "Author": "Dr. Andrew Huberman",
                "Author Source": "https://www.hubermanlab.com/",
                "Description": "The 'Huberman Lab Podcast,' hosted by Stanford neuroscientist Dr. Andrew Huberman, covers various aspects of neuroscience and related scientific topics. In each episode, Dr. Huberman delivers a self-contained masterclass on a different subject, often inviting guest speakers who are experts in the field. The popular podcast sees millions of listeners worldwide.",
                "Image": "https://assets-global.website-files.com/64416928859cbdd1716d79ce/6441c30ef12f50bc3f2449da_huberman-lab-podcast-cover.webp"
            },
            {
                "Category": "Live Event",
                "Title": "Andrew Huberman's Live Event",
                "Title Source": "https://www.hubermanlab.com/events",
                "Author": "Dr. Andrew Huberman",
                "Author Source": "https://www.hubermanlab.com/",
                "Description": "The live event is being hosted by neuroscientist Dr. Andrew Huberman in Seattle on May 17, followed by another one in Portland on May 18. The details of the event are yet to be disclosed, but they are expected to involve discourses on neuroscience, given Dr. Huberman's expertise. The event highlights are anticipated to be invaluable resources for understanding the workings of the brain.",
                "Image": "https://i.ytimg.com/vi/TO0WUTq5zYI/maxresdefault.jpg"
            },
            {
                "Category": "Television series",
                "Title": "Madmen",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Matthew Weiner",
                "Author Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Description": "Mad Men is an American period drama television series created by Matthew Weiner. The series is set primarily in the 1960s and reflects on the changing moods and social mores of the United States during the era. The 'Mad Men' TV series is mentioned as a take on the concept of an individual drastically changing their personality and life.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "The Rich Roll Podcast",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Rich Roll",
                "Author Source": "https://www.richroll.com/",
                "Description": "The context of this analysis is taken from the conversation between the host, Rich Roll, and the guest, Dr. Andrew Huberman, on The Rich Roll Podcast. While the specific episode is not mentioned, they discuss a wide range of topics including neuroscience, self-perception, trauma, the power of actions to change one's perspective and personality, and the therapeutic applications of hallucinogenic substances.",
                "Image": "https://i.ytimg.com/vi/ugTGB6PE4vw/maxresdefault.jpg"
            }
        ],
        "title": "The Neuroscience of Optimal Performance: Dr. Andrew Huberman | Rich Roll Podcast"
    }
    return result
