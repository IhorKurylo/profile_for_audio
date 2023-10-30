from fastapi import APIRouter, Form
from app.Utils.transcript import extract_video_id, get_transcript_from_youtube
from app.Utils.extract_keywords import extract_data, complete_profile
import time
import asyncio

router = APIRouter()


def pipeline(value, functions):
    result = value
    for func in functions:
        result = func(result)
    return result


# @router.post("/extract_mentioned_data")
# def extract_mentioned_data(url: str = Form(...)):
#     start_time = time.time()
#     functions = [extract_video_id, get_transcript_from_youtube, extract_data]
#     pipeline(url, functions)
#     # print("here")
#     # extract_data(result)
#     # # asyncio.run(extract_data(result))
#     # result = complete_profile(context)
#     current_time = time.time()
#     print("Total Time: ", current_time - start_time)
#     # return result


@router.post("/extract_mentioned_data")
def extract_mentioned_data(url: str = Form(...)):
    start_time = time.time()
    # functions = [extract_video_id, get_transcript_from_youtube, extract_data, complete_profile]
    # result = pipeline(url, functions)
    context = """
        context:  Category: Book
Title: Stolen Focus
Author: Johann Hari
Description: This book is written by Johann Hari and it's all about the modern society's declining ability to sustain attention. Hari investigates a variety of causes from digital technology distractions to the influence of stress, sleep, physical exercise, and our disconnection from nature and other people in shaping our attention capacities.

Category: Podcasts
Title: Huberman Lab Podcast
Author: Dr. Andrew Huberman
Description: The Huberman Lab Podcast is hosted by Dr. Andrew Huberman, a neuroscientist and professor at Stanford University. The podcast is a series of detailed discussions on different aspects of neuroscience ranging from mechanisms of sleep, how we focus and the science behind neuroplasticity. It's known for explaining complex scientific topics in a comprehensible and engaging way.

Category: Podcasts
Title: The Rich Roll Podcast
Author: Rich Roll 
Description: This is a podcast hosted by Rich Roll where he engages his guests in deep, thought-provoking conversations about all things wellness, personal growth, plant-based nutrition, fitness, and more. In the mentioned episode, Rich Roll was having his second round of conversation with Stanford neuroscientist, Dr. Andrew Huberman.
I'm sorry but I couldn't find any specific mention of a book, movie, podcast, or article in the provided text.
Category: Podcast
Title: Unknown
Author: Andrew Huberman
Description: In this context, Andrew Huberman discusses his podcast where he refers to interviewing various guests and studying different forms of therapy such as ketamine therapies, hypnosis, and psychedelic therapies. 

Category: Book
Title: Unknown
Author: Rich Roll
Description: The author mentions Rich Roll's book which inspired him to make several important changes in his life. The title of the book is not specified in the context but it plays a significant role in his journey of self-improvement and personal growth.

Category: TV Series
Title: Mad Men
Creator: Matthew Weiner
Description: Mad Men is an American period drama television series created by Matthew Weiner. The lead character embarks on a journey of completely shifting his life, personality, and identity. The series depicts this transformation by showing how behaviors can change circuits in the nervous system over time.

Category: Podcast
Title: Unknown
Author: Unknown
Description: The author refers to an individual named Chad Wright who has been featured on an unspecified podcast. Through his content, Chad Wright has become an influential figure, inspiring individuals to push their boundaries and act outside of their comfort zones.

Category: Podcast
Title: Unknown
Author: David Speigel and Anna Lamche
Description: David Spiegel and Anna Lamche are experts in psychiatry who have worked extensively in trauma therapies. Their podcasts explore a variety of therapeutic modalities and their impact on trauma recovery, like accessing states of high autonomic arousal and desensitizing oneself to traumatic experiences.

Sorry, but there are no books, movies, articles, and podcasts specifically mentioned by their title in the provided contextual story.
                        I'm sorry but I'm unable to assist as the context provided does not mention or discuss any specific books, movies, articles, or podcasts.
Category: Podcast
Title: Unknown
Author: Unknown
Description:
This podcast was indirectly mentioned in the conversation. One of the participants descried their activities of hosting solo episodes and inviting guests to discuss varied topics. The exact name or theme of the podcast was not disclosed in the context.

Category: Book
Title: Unknown
Author: Unknown
Description:
There was a book mentioned in the conversation, however, the title, theme, or author of the book was not disclosed. The mention hinted that the author of the book and the person having the conversation are same, suggesting that the book might cover a topic that the speaker is knowledgeable in. It is also mentioned the next book by this author is being worked on.

Category: Event (Not strictly a media, but mentioned as planned activities)
Title: Live events in Seattle, Portland, and other cities.
Author/Organizer: Unknown
Description:
The speaker has mentioned their plans to host some live events in several cities including Seattle and Portland around May 17th and 18th. Details about the type or purpose of these live events were not provided. Toward the end of the year, in the fall and winter season, they plan to hold similar events in other cities.
 
    
    """
    complete_profile(context)
    print("here")
    current_time = time.time()
    print("Total Time: ", current_time - start_time)
