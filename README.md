### YT-IG-Project

This is a project to automate Instagram and youtube. Till now I have only done instagram. The automation has 5 steps.

## Scripting

- Method 1 - Given a subreddit, the code will scrape desirable content from the subreddit using PRAW.

- Method 2 - Fetching data from NewYork Times API.

- Method 3 - Fetching data from Gemini API for motivational and similar content.

Than the content is given to Gemini and it will make a script.

## Voiceover

- Method 1 - AWS Polly API

- Method 2 -ElevelLabs API

## Background

I have downloaded some no copyright videos. My code will randomly cut a 1 min segment. Same for the background song. This was done by moviepy.

## Making Video

Using stable_whisper textclips were generated and using FFmpeg , the textclips and video were combined.

## Uploading to Instagram

Using instagram-private-api I made a Express server with various APIs to upload my reels.
