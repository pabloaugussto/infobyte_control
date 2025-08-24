# main.py

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QWidget, 
                             QPushButton, QDialog, QLineEdit, QFormLayout,
                             QDialogButtonBox, QMessageBox)

# Agora importamos também a função 'adicionar_produto'
from database import buscar_todos_produtos, criar_tabela, adicionar_produto


class JanelaAdicionarProduto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Adicionar Novo Produto")
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.codigo_input = QLineEdit()
        self.nome_input = QLineEdit()
        self.categoria_input = QLineEdit()
        self.fornecedor_input = QLineEdit()
        self.preco_custo_input = QLineEdit()
        self.preco_venda_input = QLineEdit()
        self.quantidade_input = QLineEdit()

        self.form_layout.addRow("Código:", self.codigo_input)
        self.form_layout.addRow("Nome:", self.nome_input)
        self.form_layout.addRow("Categoria:", self.categoria_input)
        self.form_layout.addRow("Fornecedor:", self.fornecedor_input)
        self.form_layout.addRow("Preço de Custo:", self.preco_custo_input)
        self.form_layout.addRow("Preço de Venda:", self.preco_venda_input)
        self.form_layout.addRow("Quantidade:", self.quantidade_input)
        
        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.layout.addWidget(self.button_box)

    def get_dados(self):
        return (
            self.codigo_input.text(),
            self.nome_input.text(),
            self.categoria_input.text(),
            self.fornecedor_input.text(),
            self.preco_custo_input.text(),
            self.preco_venda_input.text(),
            self.quantidade_input.text()
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("InfoByte Control - Controle de Estoque")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.btn_adicionar = QPushButton("Adicionar Novo Produto")
        self.btn_adicionar.clicked.connect(self.abrir_janela_adicionar)
        self.layout.addWidget(self.btn_adicionar)

        self.criar_tabela_produtos()
        self.carregar_produtos()

    def criar_tabela_produtos(self):
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Código', 'Nome do Produto', 'Categoria', 
            'Fornecedor', 'Preço Custo', 'Preço Venda', 'Qtd'
        ])
        
        self.layout.addWidget(self.table)

    def carregar_produtos(self):
        produtos = buscar_todos_produtos()
        self.table.setRowCount(len(produtos))

        for linha, produto in enumerate(produtos):
            for coluna, dado in enumerate(produto):
                self.table.setItem(linha, coluna, QTableWidgetItem(str(dado)))

    def abrir_janela_adicionar(self):
        dialog = JanelaAdicionarProduto(self)
        
        if dialog.exec():
            try:
                codigo, nome, categoria, fornecedor, p_custo, p_venda, qtd = dialog.get_dados()

                if not all([codigo, nome, p_custo, p_venda, qtd]):
                    QMessageBox.warning(self, "Atenção", "Os campos Código, Nome, Preços e Quantidade são obrigatórios.")
                    return

                adicionar_produto(codigo, nome, categoria, fornecedor, float(p_custo), float(p_venda), int(qtd))
                
                self.carregar_produtos()
                QMessageBox.information(self, "Sucesso", "Produto adicionado com sucesso!")
            
            except ValueError:
                QMessageBox.critical(self, "Erro", "Verifique os valores de Preço e Quantidade. Eles devem ser números.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao adicionar o produto: {e}")


if __name__ == '__main__':
    criar_tabela()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())