from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown
import json
import random

def worldfacts() :
    with open('assets/json/political_facts.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    randomIndex = random.randint(0,len(data) - 1)
    quote = data[randomIndex]

    print(quote)
    prompt = f'''
    I am running a PoliticalFacts channel in instagram.
    
    I want you to make a script for a reel that I will post on my page. In this context, give me 45 secs script for the following event.

    This is the quote - {quote['statement']}. 

    Write the script in first person for this particular part and just give me script nothing else. In starting directly start with topic without any introduction. During outro say - "For more Political Facts content follow my page". Remember just the text that I have to read. 
'''  
    script = to_markdown(AskGemini(prompt))
    print(script)
    print('-'*80)
    return script