from utility.Gemini import AskGemini
from utility.toMarkdown import to_markdown
import requests
import datetime

NEWS_API = '29a27f5edab541728d3ac5dd63c146a3' 
BASE_URL = 'https://newsapi.org/v2/everything'

def fetch_hollywood_news(top_n=3):
    today = datetime.date.today()
    three_days_ago = today - datetime.timedelta(days=3)
    from_date = three_days_ago.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    params = {
        'q': 'Hollywood',
        'from': from_date,
        'to': to_date,
        'sortBy': 'popularity',
        'apiKey': NEWS_API,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() 
        data = response.json()

        if data['status'] == 'ok':
            articles = data['articles'][:top_n]
            news_data = []  # List to store news data

            for article in articles:
                news_item = {
                    'title': article['title'],
                    'url': article['url']
                }
                news_data.append(news_item) 

            return news_data  # Return the list of news items

        else:
            print(f"Error: {data['message']}")  
            return None  # Return None in case of an error

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None 


if __name__ == '__main__':
    news_list = fetch_hollywood_news() 
    if news_list:
        news = ""
        for i in news_list:
            news += f"Title - {i['title']} \n URL - {i['url']} \n\n"

    prompt = ''' I have a Hollywood news page on instagram where I upload daily hollywood news. I want you to make a script for
    a reel that I will post on my page. In this context, give me 45 secs script for the following event.
    '''
    condition = '''
    Write the script in first person for this particular part and just give me script nothing else. In starting directly start with topic without any introduction. During outro say - "For more hollywood news content follow my channel.
    '''

    query = prompt + news + condition
    script = to_markdown(AskGemini(prompt + news + condition ))

    print(script)
    