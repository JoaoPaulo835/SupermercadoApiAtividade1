import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

conn = sqlite3.connect('supermercado.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS setores (
        id INTEGER PRIMARY KEY,
        nome TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY,
        nome TEXT
    )
''')
conn.commit()
conn.close()

def db_connection():
   conn = None
   try:
      conn = sqlite3.connect("supermercado.db")
   except sqlite3.Error as e:
      print(e)

   return conn

def adicionar_item(tabela, nome):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO {tabela} (nome)
        VALUES (?)
    ''', (nome,))
    conn.commit()
    rowid = cursor.lastrowid
    conn.close()
    return rowid

def obter_itens(tabela):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT * FROM {tabela}
    ''')
    columns = [column[0] for column in cursor.description]
    
    response = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return response

@app.route('/<tabela>', methods=['POST'])
def adicionar_item_api(tabela):
    data = request.get_json()
    if 'nome' not in data:
        return jsonify({'error': 'Nome não fornecido'}), 400
    item_id = adicionar_item(tabela, data['nome'])
    return jsonify({'id': item_id, 'nome': data['nome']}), 201

@app.route('/<tabela>', methods=['GET'])
def obter_itens_api(tabela):
    return jsonify(obter_itens(tabela))

if __name__ == '__main__':
    app.run()