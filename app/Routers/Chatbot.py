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
    #     start_time = time.time()
    #     video_id = extract_video_id(url)
    #     title = get_title_from_youtube(video_id)
    #     functions = [get_transcript_from_youtube, extract_data, complete_profile]
    #     result = pipeline(video_id, functions)
    #     result['title'] = title
    #     current_time = time.time()
    #     print("Total Time: ", current_time - start_time)
    result = {
        "transcript": "so does that mean that like the vast majority of your real wealth creation has been in like the 10 l",
        "media": [
            {
                "Category": "Podcast",
                "Title": "My First Million",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Sam Parr & Shaan Puri",
                "Author Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Description": "\"My First Million\" is a podcast hosted by Sam Parr and Shaan Puri. They discuss various ways they have generated wealth, from start-ups to angel investing to real estate - and much more. In this context, they're speaking with Rob Dyrdek, a professional skateboarder, actor, producer, entrepreneur, and reality TV star, discussing their methods of wealth creation, the ups and downs of their careers, and Rob’s journey in starting various ventures.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            },
            {
                "Category": "Movie",
                "Title": "Deadpool",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Tim Miller (director)",
                "Author Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Description": "\"Deadpool\" is a 2016 American superhero film based on the Marvel Comics character of the same name. It was directed by Tim Miller. In this context, the movie is mentioned to indicate a point in Rob Dyrdek's life when his net worth was about 15 million to 20 million dollars.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "Dr. Andrew Huberman's Podcast",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Dr. Andrew Huberman",
                "Author Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Description": "Dr. Andrew Huberman's podcast covers the straightforward science behind new medical breakthroughs, how listeners can affect their state of mind and body, improve sleep, learn at a faster pace, and achieve more in their lives. Rob Dyrdek discusses an instance from this podcast where Dr. Huberman promotes Momentous protein, a brand co-founded by Rob.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "The most unrelatable podcast part one and part two",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Rob Dyrdek",
                "Author Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Description": "These podcast episodes are Rob Dyrdek's detailed accounting of the depth of his operation and what he's learned along the way to achieve his current level of success and personal development. He discusses how this unattainable discipline and lifestyle led him to a consistent state of joy and fulfillment.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "My First Million",
                "Title Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Author": "Sam Parr, Shaan Puri",
                "Author Source": "https://stackoverflow.com/questions/27920928/google-api-request-limit-exceeded",
                "Description": "This conversation is featured on the podcast hosted by Sam Parr and Shaan Puri. They often have guests from various industries and walks of life to discuss successful enterprises, unique business models, and innovative ideas. In this particular episode, they are hosting Rob Dyrdek to discuss his approach to harmony, success, and wellness.",
                "Image": "https://www.lifespanpodcast.com/content/images/2022/01/Welcome-Message-Title-Card-2.jpg"
            }
        ],
        "title": "How Rob Dyrdek Went From $15M to $350M in 5 Years (#465)"
    }
    return result
