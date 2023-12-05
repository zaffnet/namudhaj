#!/bin/python3

import gradio as gr
import logging
import os
import requests

MODEL_URL = os.getenv("MODEL_URL")


def classify(text):
    try:
        response = requests.post(
            f'{MODEL_URL}/model/predict',
            data={'text': [text]}
        )
        resp = response.json()
        print(resp)
        preds = resp["predictions"][0][0]
        return preds
    except Exception as exc:
        logging.error('Error in predicting, resp = %s', resp)



with gr.Blocks() as demo:
    text = gr.Textbox(label="input", placeholder="Enter your text here...")
    model_output = gr.Label(label="Sentiment model", num_top_classes=2)

    pred_btn = gr.Button("Predict label")
    pred_btn.click(
        fn=classify,
        inputs=text,
        outputs=[model_output],
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