import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print("API key loaded successfully.")
else:
    print("Failed to load API key.")
    exit(1) 

gpt_client = OpenAI(api_key=openai_api_key)

system_message = "You are a corny british old aged man, who loves manchester united and hates other team, that responds in markdown"

conversation_history = [
    {"role": "system", "content": system_message}
]

def message_gpt(prompt, history = conversation_history):
    
    history.append({"role": "user", "content": prompt})
    
    # messages = [
    #     {"role": "system", "content": system_message},
    #     {"role": "user", "content": prompt}
    # ]
    
    stream = gpt_client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = history,
        stream = True
    )
    
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        history.append({"role": "assistant", "content": result})
        yield result    
    
    

# response = message_gpt("I think city is a better team")

# print(response)

def shout(text):
    return text.upper()



# shout("hello")

view = gr.Interface(
    fn=message_gpt,
    inputs=[gr.Textbox(label="Your message:")],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)

view.launch()