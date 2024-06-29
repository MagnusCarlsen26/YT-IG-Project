import datetime
import requests
import pyperclip
import time
from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown
from dotenv import load_dotenv,dotenv_values

load_dotenv()

def find(index : int,data,prompt,condition) -> int:
    for i in range(index,len(data)):
        event = data[i]['text']
        print('Event :')
        print(event)
        print('Score :',AskGemini(prompt+event+condition)[:-2])
        print('-'*80)
        response = AskGemini(prompt+event+condition)
        if  len(response) == 3 and int(response[:-2]) >= 5:
            return event,i
        time.sleep(8)

def scripting() :

    date = datetime.datetime.now().strftime('%m/%d') 

    url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{date}'
    try :
        response = requests.get(url)
        response.raise_for_status() 
    except Exception as e:
        print("Error occured while scripting()",e)
        return scripting() 
    data = response.json()

    prompt = ''' On a scale of 1 to 10 how interesting the following event be to Americans. '''
    condition = ''' Just give me integer between 1 to 10 nothing else '''

    data = data['selected'] + data['births'] + data['deaths'] + data['events']

    events = []

    index = -1
    for i in range(3):
        event,index = find(index+1,data,prompt,condition)
        events.append(event)

    for i in events:
        print(i)
        print()
    print('-'*80)
    prompt = f'''
        I have a onThisDayInHistory page on instagram where I upload daily content. I want you to make a script for
    a reel that I will post on my page. In this context, give me 45 secs script for the following event.

    {''.join(events)}

    Write the script in first person for this particular part and just give me script nothing else. In starting directly start with topic without any introduction. During outro say - "For more  content follow my page". Remember just the text that I have to read. 
    '''

    script = to_markdown(AskGemini( prompt ))
    print(script)
    print('-'*80)
    return script