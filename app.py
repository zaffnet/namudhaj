#!/bin/python3

import gradio as gr
import logging
import backoff
import os
import openai
import requests
from openai import OpenAI

MODEL_URL = os.getenv("MODEL_URL")
API_KEY = os.environ["OPENAI_API_KEY"]
ORG_ID = os.environ["OPENAI_ORG_ID"]

SYSTEM_PROMPT = """You are helpful AI assistant. Answer the following question.\n"""





client = OpenAI(organization=ORG_ID, api_key=API_KEY)

def classify(text):
    try:
        response = requests.post(
            f'{MODEL_URL}/model/predict',
            json={'text': [text]}
        )
        resp = response.json()
        print(resp)
        preds = resp["predictions"][0]
        return preds
    except Exception as exc:
        logging.error('Error in predicting, resp = %s', resp, exc_info=exc)



@backoff.on_exception(backoff.expo, openai.RateLimitError)
def get_gpt4_explanation(text):
    try:
        model_label = classify(text)
        sentiment = 'positive' if model_label['positive'] > model_label['negative'] else 'negative'
        response = client.with_options(
            timeout=30, max_retries=2
            ).chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": f'Why does the following text has {sentiment} sentiment:\n Text:{text}',
                    },
                ],
                temperature=1.0,
                max_tokens=64,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        return response.choices[0].message.content
    except Exception as exc:
         logging.error('Error in predicting, resp = %s', response, exc_info=exc)

    

with gr.Blocks() as demo:
    text = gr.Textbox(label="Input", placeholder="Enter your text here...")
    model_output = gr.Label(label="Label from BERT model", num_top_classes=2)
    gpt4_explanation = gr.Textbox(value="", label="GPT-4 Explanation")

    def collate(text):
        return classify(text), get_gpt4_explanation(text)


    pred_btn = gr.Button("Predict sentiment")
    pred_btn.click(
        fn=collate,
        inputs=text,
        outputs=[model_output, gpt4_explanation],
        api_name="model_pred",
    )

demo.queue().launch(
    server_name="0.0.0.0", 
    server_port=7860, 
    share=False
)


# FOR TGI LLM
# import gradio as gr
# import os
# from huggingface_hub import InferenceClient

# model = os.getenv("MODEL", "falcon-40b")
# url = os.getenv("MODEL_URL")
# max_tokens = os.getenv("MAX_TOKENS", 50)

# client = InferenceClient(model=url)

# def inference(message, history):
#     partial_message = ""
#     for token in client.text_generation(message, max_new_tokens=max_tokens, stream=True):
#         partial_message += token
#         yield partial_message

# gr.ChatInterface(
#     inference,
#     chatbot=gr.Chatbot(height=300),
#     textbox=gr.Textbox(placeholder="Chat with me!", container=False, scale=7),
#     description=f'Text generation interface with {model} model.',
#     title="Namudhaj",
#     examples=["What is Cloud Computing?"],
#     retry_btn="Retry",
#     undo_btn="Undo",
#     clear_btn="Clear",
# ).queue().launch(server_name="0.0.0.0", server_port=7860, share=False)