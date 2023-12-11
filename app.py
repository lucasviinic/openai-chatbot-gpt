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
            ## Dados do ecommerce:
            {ecommerce_data}   
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

def load(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def salva(file_name: str, content):
    try:
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

ecommerce_data = load('dados_ecommerce.txt')


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    prompt = request.json['msg']
    return Response(handle_response(prompt), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug = True)