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
    print(url)
    # start_time = time.time()
    # video_id = extract_video_id(url)
    # title = get_title_from_youtube(video_id)
    # functions = [get_transcript_from_youtube, extract_data, complete_profile]
    # result = pipeline(video_id, functions)
    # result['title'] = title
    # current_time = time.time()
    # print("Total Time: ", current_time - start_time)
    result = {
        "transcript": "so does that mean that like the vast majority of your real wealth creation has been in like the 10 l",
        "media": [
            {
                "Category": "Podcast",
                "Title": "My First Million (MFM)",
                "Title Source": "https://www.mfmpod.com/",
                "Author": "Sam Parr, Shaan Puri",
                "Author Source": "https://www.mfmpod.com/",
                "Description": "In the podcast, My First Million, the hosts Sam Parr and Shaan Puri, often brainstorm business ideas or discuss business strategies based on trends in the market. They also frequently bring guests onto the show to share their interesting business or personal journeys, providing audience with different perspectives on entrepreneurship.",
                "Image": "https://images.podpage.com/https%3A%2F%2Fs3.us-west-1.amazonaws.com%2Fredwood-labs%2Fshowpage%2Fuploads%2Fimages%2F77a8c506e195400bb335a17755c9c218.jpeg?auto=format&fill=blur&fit=fill&h=628&w=1200&s=36b2cd7da7b433eec3b7839af9247e8b"
            },
            {
                "Category": "Podcast",
                "Title": "Podcast episode with Rob Dyrdek",
                "Title Source": "https://www.youtube.com/playlist?list=PLMl_CINepkAnzxHDNulfPg_0gK6IbuF_f",
                "Author": "Sam Parr, Shaan Puri",
                "Author Source": "https://www.mfmpod.com/",
                "Description": "This podcast episode is part of 'My First Million' series and Rob Dyrdek is brought in as a guest to speak about his various entrepreneurial endeavors, his time management techniques and details about companies he's built. The episode is said to be humorous, inspirational, tactical and entertaining.",
                "Image": "https://i.ytimg.com/vi/zbDJRnQkfTw/maxresdefault.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "Billed with Rob",
                "Title Source": "https://www.justice.gov/usao-de/pr/tax-and-firearm-charges-filed-against-robert-hunter-biden",
                "Author": "Rob Dyrdek",
                "Author Source": "https://www.instagram.com/robdyrdek/?hl=en",
                "Description": "Rob Dyrdek, a professional skateboarder and entrepreneur, shares his philosophy and experiences on 'Billed with Rob'. He strives to enlighten his audience on how they can cultivate a harmonious and high-quality existence through self-awareness, discipline, and optimization of their time and health.",
                "Image": "https://m.media-amazon.com/images/I/91niq+rYdFL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "My First Million",
                "Title Source": "https://www.mfmpod.com/",
                "Author": "Sam Parr and Shaan Puri",
                "Author Source": "https://www.mfmpod.com/",
                "Description": "In the podcast 'My First Million,' Sam Parr and Shaan Puri discuss trends, business ideas, and insights drawn from the experiences of successful entrepreneurs and innovators.",
                "Image": "https://yt3.googleusercontent.com/knXAGosF84sygp1GtQsA_ihQlg5eyB_ZIvpv3a3DApa-6_mFT1q29H-D12Ui1tie1v4nfYN8Cw=s900-c-k-c0x00ffffff-no-rj"
            },
            {
                "Category": "Podcast",
                "Title": "Most Unrelatable Podcast Part 1 and Part 2",
                "Title Source": "https://www.youtube.com/playlist?list=PLMl_CINepkAnzxHDNulfPg_0gK6IbuF_f",
                "Author": "Rob Dyrdek",
                "Author Source": "https://www.instagram.com/robdyrdek/?hl=en",
                "Description": "In these special podcast editions, Rob Dyrdek delves into the specifics of how he operates on an everyday basis. He shares his insights and what he has learned on his journey to high-level functioning.",
                "Image": "https://i.ytimg.com/vi/7HDpEqYCxaA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAwBcsOD6U4FfZgJR7cgGdL5oog2w"
            },
            {
                "Category": "Podcast",
                "Title": "Brian Johnson's podcast",
                "Title Source": "https://podcasts.apple.com/us/podcast/heroic-with-brian-johnson-activate-your-best-every-day/id1033620094",
                "Author": "Brian Johnson",
                "Author Source": "https://en.wikipedia.org/wiki/Brian_Johnson",
                "Description": "Brian Johnson's podcast is not specifically named in the context, and therefore, precise details about it cannot be ascertained. However, Rob Dyrdek mentions Brian Johnson as an emblematic figure in the health and wellness industry, known for his futuristic and transformational approach to self-optimization and growth.",
                "Image": "https://images.squarespace-cdn.com/content/v1/5884e9861b10e356f538b6ce/1486233848358-QNQYI36YWSWNJWIRF29K/bethanyo.com_0062.jpg"
            }
        ],
        "title": "How Rob Dyrdek Went From $15M to $350M in 5 Years (#465)"
    }
    return result
