import gradio as gr
from transformers import pipeline

# Initialize the Hugging Face Q&A model
index = pipeline("question-answering")

def chat(chat_history, user_input):
    bot_response = index(question=user_input, context=chat_history)
    response = bot_response['answer']
    return chat_history + [(user_input, response)]

demo = gr.Interface.fn(chat,
                      inputs=gr.Textbox(),
                      outputs=gr.Textbox())

demo.launch()
