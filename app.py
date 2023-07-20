import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

db_config = {
    'host': f'{os.getenv("DB_HOST")}',
    'user': f'{os.getenv("DB_USER")}',
    'password': f'{os.getenv("DB_PASS")}',
    'database': f'{os.getenv("DB_NAME")}',
}

# Função para conectar o banco de dados
def conectar_db():
    return mysql.connector.connect(**db_config)

# Criar novo produto
@app.route('/produto', methods=['POST'])
def criar_produto():
    try:
        data = request.get_json()
        conn = conectar_db()
        cursor = conn.cursor()
        query = "INSERT INTO produtos (nome_produto, valor) VALUES (%s, %s)"
        cursor.execute(query, (data['nome_produto'], data['valor']))
        conn.commit()
        conn.close()
        return(jsonify({'message': 'Produto criado com sucesso!'})), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.run(port=5000, host='localhost', debug=True)