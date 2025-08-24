# database.py

import sqlite3
import os

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIRETORIO_ATUAL, 'infobyte.db')

def conectar():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
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

# --- NOVAS FUNÇÕES ABAIXO ---

def buscar_produto_por_id(id):
    """Busca um único produto pelo seu ID."""
    produto = None
    try:
        conn, cursor = conectar()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        produto = cursor.fetchone() # fetchone() pega apenas um resultado
    except sqlite3.Error as e:
        print(f"Erro ao buscar produto por ID: {e}")
    finally:
        if conn:
            conn.close()
    return produto

def atualizar_produto(id, codigo, nome, categoria, fornecedor, preco_custo, preco_venda, quantidade):
    """Atualiza um produto existente no banco de dados."""
    try:
        conn, cursor = conectar()
        cursor.execute("""
        UPDATE produtos 
        SET codigo = ?, nome = ?, categoria = ?, fornecedor = ?, preco_custo = ?, preco_venda = ?, quantidade = ?
        WHERE id = ?
        """, (codigo, nome, categoria, fornecedor, preco_custo, preco_venda, quantidade, id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        if conn:
            conn.close()

def excluir_produto(id):
    """Exclui um produto do banco de dados pelo seu ID."""
    try:
        conn, cursor = conectar()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao excluir produto: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    criar_tabela()