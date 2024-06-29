import praw
import logging

# logging.basicConfig(level=logging.DEBUG)
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from praw.models import MoreComments
import re
import random

def sanitize_text(text: str) -> str:
    r"""Sanitizes the text for tts.
        What gets removed:
     - following characters`^_~@!&;#:-%“”‘"%*/{}[]()\|<>?=+`
     - any http or https links

    Args:
        text (str): Text to be sanitized

    Returns:
        str: Sanitized text
    """

    # remove any urls from the text
    regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

    result = re.sub(regex_urls, " ", text)

    # note: not removing apostrophes
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@!&;#:\-%—“”‘\"%\*/{}\[\]\(\)\\|<>=+]"
    result = re.sub(regex_expr, " ", result)
    result = result.replace("+", "plus").replace("&", "and")

    # emoji removal if the setting is enabled
   

    # remove extra whitespace
    return " ".join(result.split())
# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )

import json
from os.path import exists

def get_subreddit_undone(submissions: list, subreddit, times_checked=0, similarity_scores=None):
    """_summary_

    Args:
        submissions (list): List of posts that are going to potentially be generated into a video
        subreddit (praw.Reddit.SubredditHelper): Chosen subreddit

    Returns:
        Any: The submission that has not been done
    """

    # for i, submission in enumerate(submissions):
    #     # if submission.over_18:
    #     #     try:
    #     #         if not settings.config["settings"]["allow_nsfw"]:
    #     #             print("NSFW Post Detected. Skipping...")
    #     #             continue
    #     #     except AttributeError:
    #     #         print("NSFW settings not defined. Skipping NSFW post...")
    #     if True: #storymode
    #         if not submission.selftext:
    #             print("You are trying to use story mode on post with no post text")
    #             continue
    #         else:
    #             # Check for the length of the post text
    #             if len(submission.selftext) > 2000 :
    #                 print(
    #                     f"Post is too long ({len(submission.selftext)}), try with a different post. ({settings.config['settings']['storymode_max_length']} character limit)"
    #                 )
    #                 continue
    #             elif len(submission.selftext) < 30:
    #                 continue
    #     if True and not submission.is_self:
    #         continue
    #     if similarity_scores is not None:
    #         print('retruned')
    #         return submission, similarity_scores[i].item()
    #     print('retruned')
        
    #     return submission
    print("all submissions have been done going by top submission order")
    VALID_TIME_FILTERS = [
        "day",
        "hour",
        "month",
        "week",
        "year",
        "all",
    ]  # set doesn't have __getitem__
    index = times_checked + 1
    if index == len(VALID_TIME_FILTERS):
        print("All submissions have been done.")

    return get_subreddit_undone(
        subreddit.top(
            limit=(50 if int(index) == 0 else index + 1 * 50),
        ),
        subreddit,
        times_checked=index,
    )  # all the videos in hot have already been done

# This function sort the given threads based on their total similarity with the given keywords
def sort_by_similarity(thread_objects, keywords):
    # Initialize tokenizer + model.
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Transform the generator to a list of Submission Objects, so we can sort later based on context similarity to
    # keywords
    thread_objects = list(thread_objects)

    threads_sentences = []
    for i, thread in enumerate(thread_objects):
        threads_sentences.append(" ".join([thread.title, thread.selftext]))

    # Threads inference
    encoded_threads = tokenizer(
        threads_sentences, padding=True, truncation=True, return_tensors="pt"
    )
    with torch.no_grad():
        threads_embeddings = model(**encoded_threads)
    threads_embeddings = mean_pooling(threads_embeddings, encoded_threads["attention_mask"])

    # Keywords inference
    encoded_keywords = tokenizer(keywords, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        keywords_embeddings = model(**encoded_keywords)
    keywords_embeddings = mean_pooling(keywords_embeddings, encoded_keywords["attention_mask"])

    # Compare every keyword w/ every thread embedding
    threads_embeddings_tensor = torch.tensor(threads_embeddings)
    total_scores = torch.zeros(threads_embeddings_tensor.shape[0])
    cosine_similarity = torch.nn.CosineSimilarity()
    for keyword_embedding in keywords_embeddings:
        keyword_embedding = torch.tensor(keyword_embedding).repeat(
            threads_embeddings_tensor.shape[0], 1
        )
        similarity = cosine_similarity(keyword_embedding, threads_embeddings_tensor)
        total_scores += similarity

    similarity_scores, indices = torch.sort(total_scores, descending=True)

    threads_sentences = np.array(threads_sentences)[indices.numpy()]

    thread_objects = np.array(thread_objects)[indices.numpy()].tolist()

    # print('Similarity Thread Ranking')
    # for i, thread in enumerate(thread_objects):
    #    print(f'{i}) {threads_sentences[i]} score {similarity_scores[i]}')

    return thread_objects, similarity_scores
def script(threads) :
    randomThread = random.randint(0,len(threads) - 1)
    thread = threads[randomThread]  

    for i in range(len(thread['comments'])) :

        if 120 >len(thread['thread_title'].split()) + len(thread['comments'][i]['comment_body'].split()) > 50 :
            print (thread['thread_title'] + '\n' + '\n' + thread['comments'][i]['comment_body'] + 'For more content follow my channel')
            print('-'*80)
            return thread['thread_title'] + '\n' + '\n' + thread['comments'][i]['comment_body']  + 'For more content follow my channel'
    else :
        return script(threads)

def get_subreddit_threads(sub):
    """
    Returns a list of threads from the AskReddit subreddit.
    """
    content = {}
    try:
        reddit = praw.Reddit(
            client_id='8rFWTam2fpS3gXe6loXLlg',
            client_secret='4Bg8Ufxglg_aCsydpuEJzRr_Z8Ejaw',
            user_agent="Accessing Reddit threads",
            # username=username,
            # passkey=passkey,
            # check_for_async=False,
            # https= True,
        )
        print('Logged in')

    except Exception as e:
        print(e)
        if e.response.status_code == 401:
            print("Invalid credentials - please check them in config.toml")
    except:
        print("Something went wrong...")

    print("Getting subreddit threads...")
    similarity_score = 0

    print(f"Using subreddit: r/{sub}.")
    subreddit = reddit.subreddit(sub)

    threads = subreddit.hot(limit=25)

    all_thread_data = []  # List to store data for all threads

    for submission in threads:
        thread_data = {
            "thread_url": f"https://new.reddit.com/{submission.permalink}",
            "thread_title": submission.title,
            "thread_id": submission.id,
            "is_nsfw": submission.over_18,
            "comments": [],
        }

        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            if top_level_comment.body in ["[removed]", "[deleted]"]:
                continue
            if not top_level_comment.stickied:
                sanitised = sanitize_text(top_level_comment.body)
                if not sanitised or sanitised == " ":
                    continue
                if 75 <= len(top_level_comment.body.split()) <= 150:
                    if (
                        top_level_comment.author is not None
                        and sanitize_text(top_level_comment.body) is not None
                    ):
                        thread_data["comments"].append(
                            {
                                "comment_body": top_level_comment.body,
                                "comment_url": top_level_comment.permalink,"comment_id": top_level_comment.id,
                            }
                        )

        all_thread_data.append(thread_data)  # Add thread data to the list
    
    
    return script(all_thread_data)