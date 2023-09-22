import os
import openai
import gradio as gr

openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response.choices[0].text

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

block = gr.Blocks()

with block:
    gr.HTML("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .chat-box {
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .user-message, .ai-message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #cce6ff;
            color: #0066cc;
        }
        .ai-message {
            background-color: #f0f0f0;
            color: #333;
        }
        .custom-input-box {
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
        }
        .custom-output-box {
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
            background-color: #f7f7f7;
        }
    </style>
    <div class="container">
        <h1>Build Your Own ChatGPT with OpenAI API & Gradio</h1>
        <div class="chat-box">
            <div class="user-message custom-output-box">Hello, who are you?</div>
            <div class="ai-message custom-output-box">I am an AI created by OpenAI. How can I help you today?</div>
        </div>
    </div>
    """)

    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Type your message here...", style="width: 100%;", class_name="custom-input-box")
    state = gr.State()
    submit = gr.Button("SEND")
    
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug=True, share=True)
