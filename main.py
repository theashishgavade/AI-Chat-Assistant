import openai
import gradio as gr
import logging

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your OpenAI API key for authentication
openai.api_key = "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"  # Replace with your key

# Define an initial message to start the conversation with the AI Chat Assistant
messages = [{"role": "system", "content": "AI Chat Assistant for all your need"}]

def AI_Chat_Assistant(message, history):
    try:
        history_openai_format = []
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})
        history_openai_format.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages= history_openai_format,
            temperature=1.0,
            stream=True
        )

        partial_message = ""
        for chunk in response:
            if len(chunk['choices'][0]['delta']) != 0:
                partial_message = partial_message + chunk['choices'][0]['delta']['content']
                yield partial_message

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        yield "An error occurred. Please try again later."
        # You can also log the error to a log file for further analysis.

# Create a Gradio interface for the AI_Chat_Assistant function with a title and description
chatbot_interface = gr.ChatInterface(fn=AI_Chat_Assistant, title="AI Chat Assistant",
                                      description="AI Chat Assistant for all your needs").queue()

# Launch the Gradio interface with a public link and error handling
try:
    chatbot_interface.launch(share=True)
except Exception as e:
    logging.critical(f"Failed to launch the interface: {str(e)}")
    print(f"Failed to launch the interface: {str(e)}")
