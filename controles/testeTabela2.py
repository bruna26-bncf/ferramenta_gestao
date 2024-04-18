from PyQt5 import uic, QtWidgets, QtGui, QtCore, Qt
import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton


class ListaOperacoes():


    lista_old = [('2024123', 'Pitagoras', '1234567899', 'CRA', 10000.00, 'originacao'),
             ('2024456', 'Biluca', '1234567888', 'CRI', 11000.00, 'mandatada'),
             ('2024654', 'Frida', '1234567877', 'Debenture', 12000.00, 'liquidada'),
             ('2024987', 'Bianca', '1234567866', 'FIDC', 13000.00, 'aprovada')]

    def __init__(self):
        self.listaUBS = uic.loadUi("formulario_lista_operacoes.ui")
        #self.listaUBS.tabelaLista.cellDoubleClicked.connect(self.cell_was_clicked)
        self.listaUBS.tabelaLista.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listaUBS.tabelaLista.setHorizontalHeaderLabels(['ID', 'Nome', 'CNPJ', 'Tipo', 'Valor',
                                                             'Status', 'Consultar'])
        self.header = self.listaUBS.tabelaLista.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

        self.listaUBS.lineEdit.textChanged.connect(self.filter_table)
        self.carregar_lista()

    def filter_table(self):
        text = self.listaUBS.lineEdit.text().lower()
        print(text)
        for row in range(self.listaUBS.tabelaLista.rowCount()):
            row_hidden = True
            for col in range(self.listaUBS.tabelaLista.columnCount()):
                item = self.listaUBS.tabelaLista.item(row, col)
                if item and text in item.text().lower():
                    row_hidden = False
                    break
            self.listaUBS.tabelaLista.setRowHidden(row, row_hidden)

    def carregar_lista(self):
        self.lista = self.lista_old
        print(self.lista)
        self.listar_operacoes()

    def listar_operacoes(self):
        try:
            print(self.lista)
            self.listaUBS.tabelaLista.clear()
            self.listaUBS.tabelaLista.setHorizontalHeaderLabels(['ID', 'Nome', 'CNPJ', 'Tipo', 'Valor',
                                                                  'Status', 'Consultar'])

            linhas = len(self.lista)
            self.listaUBS.tabelaLista.setRowCount(linhas)

            for linha in range(linhas):
                self.listaUBS.tabelaLista.setItem(linha, 0, QTableWidgetItem(str(self.lista[linha][0])))
                self.listaUBS.tabelaLista.setItem(linha, 1, QTableWidgetItem(str(self.lista[linha][1])))

                if (self.lista[linha][2]) is not None:
                    print(self.lista[linha][2])
                    if len(str(self.lista[linha][2])) < 14:
                        cnpj = (str(self.lista[linha][2])).zfill(14)
                        print(cnpj)
                    else:
                        cnpj = str(self.lista[linha][2])
                        print(cnpj)
                    cnpj_formatado = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:15])

                    self.listaUBS.tabelaLista.setItem(linha, 2, QTableWidgetItem(str(cnpj_formatado)))

                self.listaUBS.tabelaLista.setItem(linha, 3, QTableWidgetItem(str(self.lista[linha][3])))
                if (self.lista[linha][4]) is not None:
                    self.listaUBS.tabelaLista.setItem(linha, 4, QTableWidgetItem(str("{:,.2f}".format(self.lista[linha][4]).replace(",", "X").replace(".", ",").replace("X", "."))))
                else:
                    self.listaUBS.tabelaLista.setItem(linha, 4, QTableWidgetItem(str("0,00")))

                self.listaUBS.tabelaLista.setItem(linha, 5, QTableWidgetItem(str(self.lista[linha][5])))
                self.button = QPushButton("☺")
                # setting geometry of button
                self.button.setGeometry(200, 150, 100, 40)
                # changing font and size of text
                self.button.setFont(QFont('Calibri', 20))
                self.button.setStyleSheet("font-weight: bold")
                self.button.clicked.connect(lambda checked, row=linha: self.button_clicked(row))
                self.listaUBS.tabelaLista.setCellWidget(linha, 6, self.button)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            #ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - preencher_tabela_series", 0)

    def button_clicked(self, row):
        print("cliquei aqui")
        id = self.listaUBS.tabelaLista.item(row, 0).text()
        nome = self.listaUBS.tabelaLista.item(row, 1).text()
        print("ID da linha:", id, "Nome da linha", nome)
        #self.abrir_formulario(id, nome)

    """
    def cell_was_clicked(self):
        print("celula clicada")
        self.row = self.listaUBS.tabelaLista.currentRow()
        print("Linha " + str(self.row))
        self.value = self.listaUBS.tabelaLista.item(self.row, 0).text()
        print(self.value)
        self.abrir_formulario(self.value) """

    # def abrir_formulario(self, id, nome):
    #     print(self.value)
    #     self.p = PreencherPlanilha()
    #     self.p.dadosUBS.show()
    #     self.p.funcao_buscar(id, nome)


if __name__ == "__main__":
    import sys

    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QtWidgets.QApplication(sys.argv)
    l = ListaOperacoes()
    l.listaUBS.show()
    sys.exit(app.exec_())



