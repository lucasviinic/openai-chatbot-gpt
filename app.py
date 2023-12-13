from time import sleep
from helpers import *
from flask import Flask
import os
import openai
import dotenv


app = Flask(__name__)
app.secret_key = 'j82$!@%OLL0-QWE3J4sk3%k-02ksU7kK3iks'

from views import *
    
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
ecommerce_data = load('ecommerce_data.txt')

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

if __name__ == "__main__":
    app.run(debug = True)