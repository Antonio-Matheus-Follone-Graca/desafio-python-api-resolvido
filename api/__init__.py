from flask import Flask, Blueprint, g
from api.rotas import *
import sqlite3
import os
def create_app():
    api = Blueprint('api', __name__)
    app = Flask(__name__)
    
    
    def obter_conexao_com_banco():
        conexao = getattr(g, 'conexao_com_banco', None)
        if conexao is None:
            # pegando a ordem dos diretórios
            ROOT_DIR = os.getcwd()
            # acessando a pasta do banco
            DB_URL = os.path.join(ROOT_DIR,'data','database.db')
            # conexao com o banco
            conexao =  sqlite3.connect(DB_URL)
            cursor = conexao.cursor()
        return conexao

    # Lógica a ser executada antes de cada requisição
    @app.before_request
    def before_request():
        # conexão com o banco de dados e cursor
        g.conexao_com_banco = obter_conexao_com_banco()
        g.cursor = g.conexao_com_banco.cursor()

    # Função a ser executada após o processamento de cada requisição
    @app.teardown_request
    def teardown_request(exception=None):
        cursor = getattr(g, 'cursor', None)
        if cursor is not None:
            cursor.close()

        conexao = getattr(g, 'conexao_com_banco', None)
        if conexao is not None:
            conexao.close()
       
    # definindo rotas: endereço, nome, nome da função e método http
    api.add_url_rule('/status', 'health', view_func=health, methods=['GET'])
    api.add_url_rule('/despesas', 'listagem_despesas', view_func=listagem_despesas, methods=['GET'])
    api.add_url_rule('/despesas', 'cadastro', view_func=cadastro_despesas, methods=['POST'])
    # prefixo, exemplo para acessar status, devo acessar antes /api. ficando assim /api/status
    app.register_blueprint(api, url_prefix='/api')
    
   
        
    return app