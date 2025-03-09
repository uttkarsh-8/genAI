import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"key exists ans starts with {openai_api_key[:8]}")
else:
    print("Openai api key does not exist")
    
openai = OpenAI()
MODEL = 'gpt-4o-mini'

system_message = "You are a helpful AI assitant who hates everything"

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    
    print("History is:")
    print(history)
    print("and message is: ")
    print(messages)
    
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
    
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response
        

gr.ChatInterface(fn=chat, type="messages").launch()