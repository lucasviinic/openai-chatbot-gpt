from flask import (
    Flask, 
    render_template,
    request, 
    Response
)
import os
import openai
import dotenv
from time import sleep


app = Flask(__name__)
app.secret_key = 'j82$!@%OLL0-QWE3J4sk3%k-02ksU7kK3iks'
    
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def bot(prompt):
    maxima_repeticao = 1
    repeticao = 0
    while True:
        try:
            model='gpt-3.5-turbo'
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce.
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            """
            response = openai.ChatCompletion.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_do_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=model
            )
            return response
        except Exception as erro:
            repeticao += 1
            if repeticao >= maxima_repeticao:
                return "Erro no GPT3: %s" % erro
            print('Erro de comunicação com OpenAI:', erro)
            sleep(1)

def handle_response(prompt: str):
    partial_response = ''
    for response in bot(prompt):
        response_piece = response.choices[0].delta.get('content', '')
        if len(response_piece):
            partial_response += response_piece
            yield response_piece

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    prompt = request.json['msg']
    return Response(handle_response(prompt), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug = True)