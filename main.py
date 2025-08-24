# main.py

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QDialog, QLineEdit, QFormLayout,
                             QDialogButtonBox, QMessageBox)

from database import (buscar_todos_produtos, criar_tabela, adicionar_produto, 
                      buscar_produto_por_id, atualizar_produto, excluir_produto)

class JanelaEdicao(QDialog):
    def __init__(self, produto_id=None, parent=None):
        super().__init__(parent)

        self.produto_id = produto_id
        if self.produto_id is None:
            self.setWindowTitle("Adicionar Novo Produto")
        else:
            self.setWindowTitle("Editar Produto")

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

        if self.produto_id is not None:
            self.carregar_dados_produto()
    
    def carregar_dados_produto(self):
        produto = buscar_produto_por_id(self.produto_id)
        if produto:
            # id, codigo, nome, categoria, fornecedor, p_custo, p_venda, qtd
            self.codigo_input.setText(produto[1])
            self.nome_input.setText(produto[2])
            self.categoria_input.setText(produto[3] if produto[3] else "")
            self.fornecedor_input.setText(produto[4] if produto[4] else "")
            self.preco_custo_input.setText(str(produto[5]))
            self.preco_venda_input.setText(str(produto[6]))
            self.quantidade_input.setText(str(produto[7]))

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
        self.setGeometry(100, 100, 900, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.criar_botoes()
        self.criar_tabela_produtos()
        self.carregar_produtos()

    def criar_botoes(self):
        botoes_layout = QHBoxLayout()
        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.clicked.connect(self.adicionar_produto)
        self.btn_editar = QPushButton("Editar")
        self.btn_editar.clicked.connect(self.editar_produto)
        self.btn_excluir = QPushButton("Excluir")
        self.btn_excluir.clicked.connect(self.excluir_produto)
        botoes_layout.addWidget(self.btn_adicionar)
        botoes_layout.addWidget(self.btn_editar)
        botoes_layout.addWidget(self.btn_excluir)
        self.layout.addLayout(botoes_layout)

    def criar_tabela_produtos(self):
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Código', 'Nome', 'Categoria', 'Fornecedor', 'P. Custo', 'P. Venda', 'Qtd'])
        self.layout.addWidget(self.table)

    def carregar_produtos(self):
        produtos = buscar_todos_produtos()
        self.table.setRowCount(len(produtos))
        for linha, produto in enumerate(produtos):
            for coluna, dado in enumerate(produto):
                self.table.setItem(linha, coluna, QTableWidgetItem(str(dado)))

    def _obter_id_selecionado(self):
        linha_selecionada = self.table.currentRow()
        if linha_selecionada == -1:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione um produto na tabela.")
            return None
        produto_id = int(self.table.item(linha_selecionada, 0).text())
        return produto_id

    def adicionar_produto(self):
        dialog = JanelaEdicao(parent=self)
        if dialog.exec():
            try:
                codigo, nome, cat, forn, p_custo, p_venda, qtd = dialog.get_dados()
                if not all([codigo, nome, p_custo, p_venda, qtd]):
                    QMessageBox.warning(self, "Atenção", "Campos obrigatórios não preenchidos.")
                    return
                adicionar_produto(codigo, nome, cat, forn, float(p_custo), float(p_venda), int(qtd))
                self.carregar_produtos()
                QMessageBox.information(self, "Sucesso", "Produto adicionado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

    def editar_produto(self):
        produto_id = self._obter_id_selecionado()
        if produto_id is None:
            return
        
        dialog = JanelaEdicao(produto_id=produto_id, parent=self)
        if dialog.exec():
            try:
                codigo, nome, cat, forn, p_custo, p_venda, qtd = dialog.get_dados()
                if not all([codigo, nome, p_custo, p_venda, qtd]):
                    QMessageBox.warning(self, "Atenção", "Campos obrigatórios não preenchidos.")
                    return
                atualizar_produto(produto_id, codigo, nome, cat, forn, float(p_custo), float(p_venda), int(qtd))
                self.carregar_produtos()
                QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

    def excluir_produto(self):
        produto_id = self._obter_id_selecionado()
        if produto_id is None:
            return

        confirmacao = QMessageBox.question(self, "Confirmação", 
                                            "Tem certeza que deseja excluir este produto?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirmacao == QMessageBox.StandardButton.Yes:
            try:
                excluir_produto(produto_id)
                self.carregar_produtos()
                QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao excluir: {e}")

if __name__ == '__main__':
    criar_tabela()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())