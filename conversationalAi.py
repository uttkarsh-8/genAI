import os
from dotenv import load_dotenv
import openai
import gradio as gr

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

MODEL = 'gpt-4o-mini'
system_message = "you are a cranky, corny and egoistical british blud"

def chat(message, history):
    history = history or []
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    
    stream = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        stream=True
    )
    
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.get("content", "")
        yield (response, history)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})

    yield (response, history)

interface = gr.Interface(
    fn=chat,
    inputs=[
        gr.Textbox(label="Your message: ", lines=6),
        gr.State([])  
    ],
    outputs=[
        gr.Textbox(label="Response: ", lines=8),
        gr.State()
    ],
    flagging_mode="never"
)

interface.launch()
