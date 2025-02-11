import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from typing import List
import gradio as gr 
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


system_message = "You are an assistant that analyzes the contents of a company website landing page \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown."

def message_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

# response = message_gpt(prompt)
# print(response)

def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

# shout("hello")

# view = gr.Interface(
#     fn=message_gpt,
#     inputs=[gr.Textbox(label="Your message: ", lines=6)],
#     outputs=[gr.Textbox(label="Response: ", lines=8)],
#     flagging_mode="never"
# )

# view.launch()


class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    
def stream_brochure(company_name, url, model):
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += Website(url).get_contents()
    if model=="GPT":
        result = message_gpt(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result
    
    
view = gr.Interface(
    fn=stream_brochure,
    inputs=[
        gr.Textbox(label="Company name:"),
        gr.Textbox(label="Landing page URL including http:// or https://"),
        gr.Dropdown(["GPT", "Claude"], label="Select model")],
    outputs=[gr.Markdown(label="Brochure:")],
    flagging_mode="never"
)
view.launch()