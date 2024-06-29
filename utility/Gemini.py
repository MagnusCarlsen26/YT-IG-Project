import google.generativeai as genai

genai.configure(api_key='AIzaSyDvlm3GYZzlc-q2Us5rO0Yzbc3Wk8VbLJE')
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat()

def AskGemini(prompt : str) -> str :
    response = model.generate_content(prompt)
    return response.text