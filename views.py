from app import app, bot
from helpers import *
from flask import flash, redirect, render_template, request, Response, session, url_for
from models import *
from token_counter import *
from summarizer import criando_resumo
import os


def handle_response(prompt: str, history: str, file_name: str):
    partial_response = ''
    summary_history = criando_resumo(history)
    for response in bot(prompt, summary_history):
        response_piece = response.choices[0].delta.get('content', '')
        if len(response_piece):
            partial_response += response_piece
            yield response_piece

    content = f"""
    Histórico: {summary_history}
    Usuário: {prompt}
    IA: {partial_response}
    """

    save(file_name, content)

@app.route("/")
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    prompt = request.json['msg']
    file_name = session['usuario_logado']
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

@app.route('/login')
def login():
    return render_template('login.html', proxima='/')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            return redirect(request.form['proxima'])
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))
