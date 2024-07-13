import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API"))
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat()

def AskGemini(prompt : str) -> str :
    response = model.generate_content(prompt)
    return response.text