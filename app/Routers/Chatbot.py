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
    result = {
        "transcript": "one of the best quotes from this book summarizes it completely it's only after you've lost everything that you're free to do anything i'm ryan holiday these are some of my absolute favorite books i think sometimes people read books and then you're like what was that book about again and they have no",
        "media": [
            {
                "Category": "Book",
                "Title": "Blue Ocean Strategy",
                "Title_Source": "https://www.blueoceanstrategy.com/what-is-blue-ocean-strategy/",
                "Author": "W. Chan Kim and Renée Mauborgne",
                "Author_Source": "https://www.blueoceanstrategy.com/authors/",
                "Description": "This book focuses on how businesses can find market spaces that are free of competition (blue oceans) rather than competing in crowded markets (red oceans). By venturing into these uncharted market territories, companies can innovate and make the competition irrelevant, which can lead to greater success and profitability.",
                "Image": "https://m.media-amazon.com/images/I/91YCWH4jFdL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Book",
                "Title": "The Enchiridion",
                "Title_Source": "https://classics.mit.edu/Epictetus/epicench.html",
                "Author": "Epictetus",
                "Author_Source": "https://en.wikipedia.org/wiki/Epictetus",
                "Description": "Epictetus outlines Stoic philosophy in The Enchiridion (Greek for \"the handbook\"), emphasizing the segregation between what is in our control and what is not in our control. He encourages individuals to focus solely on what they can control.",
                "Image": "https://upload.wikimedia.org/wikipedia/en/2/25/Adventure_Time_The_Enchiridion%21_Title_Card.png"
            },
            {
                "Category": "Book",
                "Title": "Steel Like an Artist",
                "Title_Source": "https://www.amazon.com/Steal-Like-Artist-Things-Creative/dp/0761169253",
                "Author": "Austin Kleon",
                "Author_Source": "https://austinkleon.com/",
                "Description": "Austin Kleon's book discusses the concept that nothing is truly original. It promotes the idea of embracing influences, combining them to create new ideas, and turning them into one's own original work.",
                "Image": "http://www.austinkleon.com/wp-content/uploads/2011/09/poster-0.gif"
            },

        ],
        "title": "Ryan Holiday's Favorite Books Summarized in One Sentence"
    }
    # if url == "":
    #     return {}
    # print("start")
    # start_time = time.time()
    # video_id = extract_video_id(url)
    # if (video_id == None):
    #     return {}
    # # print("video_id: ", video_id)
    # title = get_title_from_youtube(video_id)
    # functions = [get_transcript_from_youtube, extract_data, complete_profile]
    # result = pipeline(video_id, functions)
    # result['title'] = title
    # current_time = time.time()
    # print("Total Time: ", current_time - start_time)
    return result
