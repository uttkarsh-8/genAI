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

system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
For example, if the customer says 'I'm looking to buy a hat', \
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales evemt.'\
Encourage the customer to buy hats if they are unsure what to get."

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
        

system_message += "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, \
but remind the customer to look at hats!"

gr.ChatInterface(fn=chat, type="messages").launch()