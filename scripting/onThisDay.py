import datetime
import requests
import pyperclip  # Library for clipboard interaction
import time
from Gemini import AskGemini
from toMarkdown import to_markdown

date = datetime.datetime.now().strftime('%m/%d')  # Format as MM/DD

url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/{date}'

response = requests.get(url)
response.raise_for_status()  
data = response.json()

prompt = ''' On a scale of 1 to 10 how well known and interesting  the following event be to Americans. '''
condition = ''' Just give me integer between 1 to 10 nothing else '''

data = data['selected'] + data['births'] + data['deaths'] + data['events']

def find(index : int) -> int:
    for i in range(index,len(data)):
        event = data[i]['text']
        print('Event :')
        print(event)
        print('Score :',AskGemini(prompt+event+condition)[:-2])
        print('-'*80)
        if int(AskGemini(prompt+event+condition)[:-2]) >= 8:
            return event,i
        time.sleep(8)

events = []

index = -1
for i in range(3):
    event,index = find(index+1)
    events.append(event)

for i in events:
    print(events)
    print()

prompt = '''
I'm making an instagram reel. My page makes daily reels about 'This day in history'.
With the following information that happened today in history, I want you to make a script for my reel. In this context, give me 45 secs script for the following event.
'''

Format = '''
Write the script in first person for this particular part and just give me script nothing else. In starting directly start with topic without any introduction. During outro say - "For more history content follow my channel".
'''

script = to_markdown(AskGemini(prompt + ''.join(events)+Format))

