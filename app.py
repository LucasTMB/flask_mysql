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
    
# Visualizar todos os produtos
@app.route('/produtos', methods=['GET'])
def obter_produtos():
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = "SELECT * FROM produtos"
        cursor.execute(query)
        produtos = []
        for (idVendas, nome_produto, valor) in cursor:
            produtos.append({
                'idVendas': idVendas,
                'nome_produto': nome_produto,
                'valor': valor
            })
        conn.close()
        return jsonify(produtos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Visualizar um produto por ID
@app.route('/produto/<int:id>', methods=['GET'])
def obter_produto_por_id(id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        query = "SELECT * FROM produtos WHERE idVendas = %s"
        cursor.execute(query, (id,))
        produto = cursor.fetchone()
        conn.close()
        if produto:
            return jsonify({
                'idVendas': produto[0],
                'nome_produto': produto[1],
                'valor': produto[2]
            })
        else:
            return jsonify({'message': 'Produto não encontrado!'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Atualizar um produto por ID
@app.route('/produto/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        data = request.get_json()
        conn = conectar_db()
        cursor = conn.cursor()
        query = "UPDATE produtos SET nome_produto = %s, valor = %s WHERE idVendas = %s"
        cursor.execute(query, (data['nome_produto'], data['valor'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Produto atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.run(port=5000, host='localhost', debug=True)