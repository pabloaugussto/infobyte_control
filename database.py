# database.py

import sqlite3
import os

# Pega o caminho absoluto do diretório onde o script está
# Isso garante que o banco de dados será criado na pasta do projeto, não importa de onde você execute o script
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIRETORIO_ATUAL, 'infobyte.db')

def conectar():
    """Conecta ao banco de dados SQLite e retorna a conexão e o cursor."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
    """Cria a tabela 'produtos' no banco de dados, se ela não existir."""
    try:
        conn, cursor = conectar()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            categoria TEXT,
            fornecedor TEXT,
            preco_custo REAL NOT NULL,
            preco_venda REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        if conn:
            conn.close()

def adicionar_produto(codigo, nome, categoria, fornecedor, preco_custo, preco_venda, quantidade):
    """Adiciona um novo produto ao banco de dados."""
    try:
        conn, cursor = conectar()
        cursor.execute("""
        INSERT INTO produtos (codigo, nome, categoria, fornecedor, preco_custo, preco_venda, quantidade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo, nome, categoria, fornecedor, preco_custo, preco_venda, quantidade))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar produto: {e}")
    finally:
        if conn:
            conn.close()

def buscar_todos_produtos():
    """Busca e retorna todos os produtos da tabela."""
    produtos = []
    try:
        conn, cursor = conectar()
        cursor.execute("SELECT * FROM produtos ORDER BY nome")
        produtos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar produtos: {e}")
    finally:
        if conn:
            conn.close()
    return produtos


if __name__ == '__main__':
    print("Iniciando configuração do banco de dados...")
    criar_tabela()
    print("Banco de dados e tabela 'produtos' verificados/criados com sucesso!")
   
                   