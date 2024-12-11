from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask("Minha API")
CORS(app) 
@app.route("/")
def index():
    return "Hello World!"

@app.route("/consulta", methods=["GET"])
def consulta_cadastro():
    documento = request.args.get("doc")
    registro = dados(documento)
    
    if registro.get("nome") == "não encontrado":
        return jsonify({"mensagem": "CPF não encontrado"}), 404  
    
    return jsonify(registro)  

@app.route("/cadastro", methods=["POST"])
def cadastrar():
    payload = request.json
    cpf = payload.get("cpf")
    valores = payload.get("dados")

    
    dados_pessoas = carregar_arquivo()
    if cpf in dados_pessoas:
        return jsonify({"mensagem": "CPF já cadastrado"}), 400  
    
    salvar_dados(cpf, valores)
    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}), 201  

def carregar_arquivo():
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    try:
        with open(caminho_arquivo, "r") as arq:
            dados = json.load(arq)

        
        dados_ordenados = dict(sorted(dados.items(), key=lambda item: item[1]['nome'].lower()))
        return dados_ordenados
    except Exception as e:
        return f"Falha ao carregar o arquivo: {e}"
    
def gravar_arquivo(dados):
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "dados.json")
    try:
        
        dados_ordenados = dict(sorted(dados.items(), key=lambda item: item[1]['nome'].lower()))

        
        with open(caminho_arquivo, "w") as arq:
            json.dump(dados_ordenados, arq, indent=4)
        return "dados armazenados"
    except Exception as e:
        return f"Falha ao carregar o arquivo: {e}"

def salvar_dados(cpf, registro):
    dados_pessoas = carregar_arquivo()
    dados_pessoas[cpf] = registro
    gravar_arquivo(dados_pessoas)

def dados(cpf):
    dados_pessoas = carregar_arquivo()
    vazio = {
        "nome": "não encontrado",
        "data_nascimento": "não encontrado",
        "email": "não econtrado",
    }
    cliente = dados_pessoas.get(cpf, vazio)
    return cliente


if __name__ == "__main__":
     app.run()

     