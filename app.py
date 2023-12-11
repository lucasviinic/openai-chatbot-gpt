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

import tiktoken


app = Flask(__name__)
app.secret_key = 'j82$!@%OLL0-QWE3J4sk3%k-02ksU7kK3iks'
    
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def bot(prompt: str, history: str):
    maxima_repeticao = 1
    repeticao = 0
    while True:
        try:
            model='gpt-3.5-turbo'
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce.
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            ## Dados do ecommerce:
            {ecommerce_data}  
            ## Histórico
            {history}
            """

            expected_output_size = 2000
            total_token_model = 4000
            if token_counter(prompt_do_sistema) >= total_token_model - expected_output_size:
                model = "gpt-3.5-turbo-16k"

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

def handle_response(prompt: str, history: str, file_name: str):
    partial_response = ''
    for response in bot(prompt, history):
        response_piece = response.choices[0].delta.get('content', '')
        if len(response_piece):
            partial_response += response_piece
            yield response_piece

    content = f"""
    Usuário: {prompt}
    IA: {partial_response}
    """

    save(file_name, content)

def load(file_name: str):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def save(file_name: str, content: str):
    try:
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def token_counter(prompt: str) -> int:
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_list = encoder.encode(prompt)
    count = len(token_list)
    return count

ecommerce_data = load('ecommerce_data.txt')
print(token_counter(ecommerce_data))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    prompt = request.json['msg']
    file_name = 'ecomart_history.txt'
    history = ''
    if os.path.exists(file_name):
        history = load(file_name)
    return Response(handle_response(prompt, history, file_name), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug = True)