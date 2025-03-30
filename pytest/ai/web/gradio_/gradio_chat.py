import gradio as gr
import time

def user(message, history):
    return "", history + [[message, None]]


def bot(history):

    user_message = history[-1][0]
    time.sleep(3)
    history[-1][1] = user_message

    return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()