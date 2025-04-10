import gradio as gr

def echo(text, request: gr.Request):
    if request:
        print("IP address:", request.client.host)  # 打印客户端的IP地址
    return text

io = gr.Interface(echo, "textbox", "textbox").launch()