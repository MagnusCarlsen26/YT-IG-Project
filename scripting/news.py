from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown
import requests
import datetime
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()

def fetch_news(query,top_n=3):
    today = datetime.date.today()
    three_days_ago = today - datetime.timedelta(days=3)
    from_date = three_days_ago.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'sortBy': 'popularity',
        'apiKey': os.getenv('NEWS_API'),
    }

    try:
        response = requests.get('https://newsapi.org/v2/everything', params=params)
        response.raise_for_status() 
        data = response.json()

        if data['status'] == 'ok':
            articles = data['articles'][:top_n]
            news_data = []  
            for article in articles:
                news_item = {
                    'title': article['title'],
                    'url': article['url']
                }
                news_data.append(news_item) 

            return news_data 

        else:
            print(f"Error: {data['message']}")  
            return None 

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None 

def makeNews(newsType):

    news_list = fetch_news(newsType) 
    news = ""
    news_data = []
    for i in news_list:
        news += f"Title - {i['title']} \n URL - {i['url']} \n\n"
        news_data.append(i['title'])

    print(news)
    print('-'*80)

    prompt = f''' 
    I have a {newsType} page on instagram where I upload daily {newsType}. I want you to make a script for
    a reel that I will post on my page. In this context, give me 45 secs script for the following event.
    '''
    condition = f'''
    Write the script in first person for this particular part and just give me script nothing else. In starting directly start with topic without any introduction. During outro say - "For more {newsType} content follow my page". Remember just the text that I have to read. 
    '''

    query = prompt + news + condition
    script = to_markdown(AskGemini(prompt + news + condition ))

    print(script)
    
    return script
