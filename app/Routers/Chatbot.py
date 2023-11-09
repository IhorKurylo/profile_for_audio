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
    result = {
        "transcript": "one of the best quotes from this book summarizes it completely it's only after you've lost everything that you're free to do anything i'm ryan holiday these are some of my absolute favorite books i think sometimes people read books and then you're like what was that book about again and they have no",
        "media": [
            {
                "Category": "Book",
                "Title": "Blue Ocean Strategy",
                "Title Source": "https://www.blueoceanstrategy.com/what-is-blue-ocean-strategy/",
                "Author": "W. Chan Kim and Renée Mauborgne",
                "Author Source": "https://www.blueoceanstrategy.com/authors/",
                "Description": "This book focuses on how businesses can find market spaces that are free of competition (blue oceans) rather than competing in crowded markets (red oceans). By venturing into these uncharted market territories, companies can innovate and make the competition irrelevant, which can lead to greater success and profitability.",
                "Image": "https://m.media-amazon.com/images/I/91YCWH4jFdL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Book",
                "Title": "The Enchiridion",
                "Title Source": "https://classics.mit.edu/Epictetus/epicench.html",
                "Author": "Epictetus",
                "Author Source": "https://en.wikipedia.org/wiki/Epictetus",
                "Description": "Epictetus outlines Stoic philosophy in The Enchiridion (Greek for \"the handbook\"), emphasizing the segregation between what is in our control and what is not in our control. He encourages individuals to focus solely on what they can control.",
                "Image": "https://upload.wikimedia.org/wikipedia/en/2/25/Adventure_Time_The_Enchiridion%21_Title_Card.png"
            },
            {
                "Category": "Book",
                "Title": "Steel Like an Artist",
                "Title Source": "https://www.amazon.com/Steal-Like-Artist-Things-Creative/dp/0761169253",
                "Author": "Austin Kleon",
                "Author Source": "https://austinkleon.com/",
                "Description": "Austin Kleon's book discusses the concept that nothing is truly original. It promotes the idea of embracing influences, combining them to create new ideas, and turning them into one's own original work.",
                "Image": "http://www.austinkleon.com/wp-content/uploads/2011/09/poster-0.gif"
            },
            {
                "Category": "Book",
                "Title": "Fight Club",
                "Title Source": "https://www.imdb.com/title/tt0137523/",
                "Author": "Chuck Palahniuk",
                "Author Source": "https://www.chuckpalahniuk.net/",
                "Description": "This novel tells the story of the unnamed protagonist's struggle with consumerism and a creeping sense of emasculation in modern society. It leads to the creation of Fight Club with Tyler Durden as a radical form of psychotherapy.",
                "Image": "https://m.media-amazon.com/images/M/MV5BODQ0OWJiMzktYjNlYi00MzcwLThlZWMtMzRkYTY4ZDgxNzgxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg"
            },
            {
                "Category": "Book",
                "Title": "How to Fight Anti-Semitism",
                "Title Source": "https://www.amazon.com/How-Fight-Anti-Semitism-Bari-Weiss/dp/0593136055",
                "Author": "Bari Weiss",
                "Author Source": "https://twitter.com/bariweiss?lang=en",
                "Description": "Bari Weiss explores the persistence of anti-Semitism through history and its present resurgence. She co-relates the treatment of Jewish people as an indicator of the societal values and the health of a society, almost like a 'canary in the coal mine.'",
                "Image": "https://images1.penguinrandomhouse.com/cover/9780593136263"
            },
            {
                "Category": "Book",
                "Title": "The 48 Laws of Power",
                "Title Source": "https://www.amazon.com/48-Laws-Power-Robert-Greene/dp/0140280197",
                "Author": "Robert Greene",
                "Author Source": "https://powerseductionandwar.com/",
                "Description": "This book is essentially a manual on the uses and power of manipulation in various areas including, but not limited to, politics, business, and day-to-day life. Greene compiles historical strategies of powerful figures to illustrate a set of Laws intended to guide readers on the acquisition, maintenance, and defense of power.",
                "Image": "https://m.media-amazon.com/images/I/51Kq3KxnzIL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Book",
                "Title": "Hold Me Tight",
                "Title Source": "https://www.amazon.com/Hold-Me-Tight-Conversations-Lifetime/dp/031611300X",
                "Author": "Sue Johnson",
                "Author Source": "https://drsuejohnson.com/",
                "Description": "Authored by Dr. Sue Johnson, this book delves into the patterns of conflict within romantic relationships, providing insight into the emotional underpinnings of couples' interactions and offering guidance for developing stronger, more fulfilling connections.",
                "Image": "https://m.media-amazon.com/images/I/91u7wOrjs2L._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Book",
                "Title": "The Apprenticeship of Duddy Kravitz",
                "Title Source": "https://en.wikipedia.org/wiki/The_Apprenticeship_of_Duddy_Kravitz_(film)",
                "Author": "Mordecai Richler",
                "Author Source": "https://en.wikipedia.org/wiki/Mordecai_Richler",
                "Description": "This novel is the story of a young Jewish man from Montreal who ascends from his modest upbringing to becoming a wealthy landowner. It explores themes of ambition, success, and morality, and raises the question: at what cost does one achieve their dreams?",
                "Image": "https://upload.wikimedia.org/wikipedia/en/b/b4/TheApprenticeshipOfDuddyKravitz.jpg"
            },
            {
                "Category": "Book",
                "Title": "Essentialism",
                "Title Source": "https://www.amazon.com/Essentialism-Disciplined-Pursuit-Greg-McKeown/dp/0804137382",
                "Author": "Greg McKeown",
                "Author Source": "https://gregmckeown.com/",
                "Description": "Essentialism is about identifying what is truly essential in your life and eliminating the rest. McKeown argues that by focusing on fewer things, we can achieve better results, find more time, and lead a more meaningful life.",
                "Image": "https://verbaltovisual.com/wp-content/uploads/2023/01/Essentialism_15_Focus.png"
            },
            {
                "Category": "Book",
                "Title": "The War of Art",
                "Title Source": "https://www.amazon.com/War-Art-Through-Creative-Battles/dp/1936891026",
                "Author": "Steven Pressfield",
                "Author Source": "https://stevenpressfield.com/",
                "Description": "Pressfield's book approaches the challenges of creating art, focusing on the concept of Resistance as an internal force that hinders creativity. He discusses strategies for overcoming blocks and persistently pursuing one's passion in the realm of creative work.",
                "Image": "https://m.media-amazon.com/images/I/61v-bmIFmhL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Book",
                "Title": "On the Shortness of Life",
                "Title Source": "https://www.amazon.com/Shortness-Life-Penguin-Great-Ideas/dp/0143036327",
                "Author": "Seneca",
                "Author Source": "https://senecafoa.org/",
                "Description": "Seneca, the Stoic philosopher, writes a moral essay advising that one's life is long enough if lived properly. By not squandering time on pointless activities, one can live a rich and fulfilling life, focusing on impactful and meaningful actions.",
                "Image": "https://m.media-amazon.com/images/I/71b1fwolK4L._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "Category": "Podcast",
                "Title": "The Daily Stoic",
                "Title Source": "https://dailystoic.com/",
                "Author": "Ryan Holiday",
                "Author Source": "https://ryanholiday.net/",
                "Description": "Ryan Holiday's podcast, 'The Daily Stoic,' involves discussions about stoicism and interviews with various individuals. It aims to provide wisdom and insights following Stoic philosophy to improve daily life.",
                "Image": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1462161080l/29093292.jpg"
            },
            {
                "Category": "Book",
                "Title": "Meditations",
                "Title Source": "https://www.amazon.com/Meditations-Marcus-Aurelius/dp/1503280462",
                "Author": "Marcus Aurelius",
                "Author Source": "https://en.wikipedia.org/wiki/Marcus_Aurelius",
                "Description": "This book is a series of personal writings by Marcus Aurelius, the Roman Emperor, recording his private notes to himself and ideas on Stoic philosophy. It is considered one of the greatest works of philosophy and is still relevant for guidance on virtuous living today.",
                "Image": "https://m.media-amazon.com/images/I/71FCbiv0tTL._AC_UF1000,1000_QL80_.jpg"
            }
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
