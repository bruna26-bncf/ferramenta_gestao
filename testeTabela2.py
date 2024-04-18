import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QRegExp
from PyQt5.QtGui import QStandardItemModel
from PyQt5.uic import loadUi


class MyTableFilter(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(MyTableFilter, self).__init__(parent)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if not self.filterRegExp().isEmpty():
            # Lógica de filtragem aqui. Por exemplo, vamos filtrar com base no conteúdo da primeira coluna.
            index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
            text = self.sourceModel().data(index0)
            # Filtra apenas as linhas que contêm a string digitada
            if self.filterRegExp().pattern() in text:
                return True
            return False
        return True



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.listaUBS = uic.loadUi("formulario_lista_operacoes_teste.ui")  # Carrega o arquivo .ui

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Exemplo de Filtro de Tabela")
        self.setGeometry(100, 100, 600, 400)

        # Encontrar a QTableWidget pelo nome definido no Qt Designer
        self.listaUBS.tabelaLista = self.findChild(QTableWidget, "tableWidget")

        # Criando alguns dados de exemplo
        data = [['Alice', 'Smith'],
                ['Bob', 'Johnson'],
                ['Charlie', 'Brown'],
                ['David', 'Miller'],
                ['Emily', 'Davis'],
                ['Frank', 'Wilson'],
                ['Grace', 'Lee']]

        self.model = MyTableModel(data, header=["Nome", "Sobrenome"])
        self.listaUBS.tabelaLista.setModel(self.model)

        # Configurar cabeçalho da tabela
        header = self.listaUBS.tabelaLista.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Criando um QLineEdit para inserir o texto do filtro
        self.filterLineEdit = self.findChild(self.listaUBS.lineEdit, "filterLineEdit")
        self.filterLineEdit.textChanged.connect(self.filterChanged)

    def filterChanged(self, text):
        # Atualizar o filtro com base no texto inserido
        regex = QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)
        self.model.setFilterRegExp(regex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())