from app import app, bot
from helpers import *
from flask import render_template, request, Response
from token_counter import *
import os


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