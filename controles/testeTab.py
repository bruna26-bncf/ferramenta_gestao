from PyQt5 import uic, QtWidgets
import os

from PyQt5.QtWidgets import QSpinBox, QApplication, QWidget


class TesteTab:

    def __init__(self):
        self.serieEstruturacao = uic.loadUi("formulario_estruturacao_series.ui")
        self.serieEstruturacao.tabWidget.setTabVisible(0, True)
        self.serieEstruturacao.tabWidget.setTabVisible(1, False)
        self.serieEstruturacao.tabWidget.setTabVisible(2, False)
        self.serieEstruturacao.tabWidget.setTabVisible(3, False)
        self.serieEstruturacao.tabWidget.setTabVisible(4, False)
        self.serieEstruturacao.botaoIncluir.clicked.connect(self.funcao_inserir_tab)
        self.serieEstruturacao.botaoTeste.clicked.connect(self.capturar_dados)

    def funcao_inserir_tab(self):
        self.serieEstruturacao.tabWidget.setTabVisible(0, True)
        self.serieEstruturacao.tabWidget.setTabVisible(1, False)
        self.serieEstruturacao.tabWidget.setTabVisible(2, False)
        self.serieEstruturacao.tabWidget.setTabVisible(3, False)
        self.serieEstruturacao.tabWidget.setTabVisible(4, False)
        self.nr_tabs = self.serieEstruturacao.spinBox_series.value()
        for i in range (self.nr_tabs):
            self.serieEstruturacao.tabWidget.setTabVisible(i, True)

    def capturar_dados(self):
        print(self.nr_tabs)
        for i in range (self.nr_tabs):
            spinBox_serie = self.serieEstruturacao.tabWidget.findChild(QSpinBox, "spinBox_serie_" + str(i))
            print(spinBox_serie)

            if spinBox_serie:
                value = spinBox_serie.value()
                print(value)







if __name__ == "__main__":
    import sys

    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QtWidgets.QApplication(sys.argv)
    l = TesteTab()
    l.serieEstruturacao.show()
    sys.exit(app.exec_())