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

def limits_history(history: str, max_token_limit: int) -> str:
    total_tokens = 0
    partial_history = ''
    for line in reversed(history.split('\n')):
        line_tokens = token_counter(line)
        total_tokens += line_tokens
        if total_tokens > max_token_limit:
            break
        partial_history = line + partial_history
    return partial_history

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
    max_token_limit = 2000
    partial_history = limits_history(history, max_token_limit)
    for response in bot(prompt, partial_history):
        response_piece = response.choices[0].delta.get('content', '')
        if len(response_piece):
            partial_response += response_piece
            yield response_piece

    content = f"""
    Histórico: {partial_history}
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
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def token_counter(prompt: str) -> int:
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_list = encoder.encode(prompt)
    count = len(token_list)
    return count

ecommerce_data = load('ecommerce_data.txt')

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

@app.route("/clean-history", methods=['POST'])
def clean_history():
    file_name = 'ecomart_history.txt'
    if os.path.exists(file_name):
        os.remove(file_name)
        print("Arquivo removido")
    else:
        print("Não foi possível remover esse arquivo.")
    return {}

if __name__ == "__main__":
    app.run(debug = True)