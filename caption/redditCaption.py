from dotenv import load_dotenv,dotenv_values
from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown


def generateCaption(title,channelName) :
    return f'''
{title}
#reddit #redditposts #reels #fyp #redditreadings
Like and follow @reddit.{channelName} for more !

'''
