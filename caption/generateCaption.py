from dotenv import load_dotenv,dotenv_values
from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown


def generateCaption(script) :
    prompt = f'''
        This is my script :

        {script}

        I want you to generate a caption for my reel. Your response should be such that I can copy your entire response and paste the caption.
    '''
    caption = to_markdown(AskGemini(prompt))
    print(caption)
