import os

from PyQt5 import uic, QtWidgets
from objetos.usuario import Usuario
from objetos.api_token import ApiToken
import ctypes
from objetos.versao import Versao
from querys.dao_generic import Generic_DAO
from querys.dao import Dao
from apis.api import Api
from apis.generic_api import Generic_Api
import getpass
from datetime import datetime
from controles.importacao_dados_excel import ImportarExcel
from controles.preencher_planilha_ubs import PreencherPlanilha
from controles.planilha_lista_operacoes import ListaOperacoes
from controles.caminhos import Caminho


class Principal:
    chave = getpass.getuser()
    senha = ""
    autenticador = ""
    logado = False

    gapi = Generic_Api()
    api = Api()
    gedao = Generic_DAO()
    dao = Dao()

    def __init__(self):
        #self.caminho = Caminho.caminho_ui()
        self.formulario_principal = uic.loadUi("formulario_principal.ui")
        self.verifica_versao()
        self.formulario_principal.textoMatricula.setText(self.chave)
        self.formulario_principal.logarButton.clicked.connect(self.logar)
        self.formulario_principal.textoSenha.returnPressed.connect(self.logar)
        self.formulario_principal.actionArquivo_UBS.triggered.connect(self.chamar_importar_ubs)
        self.formulario_principal.actionPreencher_Planilha.triggered.connect(self.chamar_inserir_dados)
        self.formulario_principal.actionLista_Operacoes.triggered.connect(self.chamar_listar_dados)
        self.formulario_principal.label_versao.setText("Versão: " + str(self.versao.versao))

    def verifica_versao(self):
        self.versao = Versao()
        if self.versao.versao != self.dao.verifica_versao():
            ctypes.windll.user32.MessageBoxW(0, "Versão do Programa Desatualizada. \n"
                                                "Instale nova versão disponível na rede",
                                                "Atenção", 0)
            sys.exit(0)

    def logar(self):
        api = Api()

        if self.formulario_principal.textoMatricula.text() != "" and self.formulario_principal.textoSenha.text() != "":

            self.chave = self.formulario_principal.textoMatricula.text()
            self.senha = self.formulario_principal.textoSenha.text()
            self.autenticador = self.formulario_principal.textoAutenticador.text()

            Usuario.chave = self.chave
            Usuario.senha = self.senha
            Usuario.autenticador = self.autenticador


            ApiToken.token = self.gapi.gera_token(Usuario.chave, Usuario.senha, Usuario.autenticador)
            ApiToken.hora_inicio = datetime.now().time().minute + (datetime.now().time().hour * 60)
            print(datetime.now().time().minute)
            print(datetime.now().time().hour * 60)
            print(ApiToken.token)
            print(ApiToken.hora_inicio)

            matricula = self.chave[1:8]
            print(matricula)

            api.dados_funci(matricula)

            if ApiToken.token is not False:

                self.logado = True

                if '2' in Usuario.sexo:
                    self.formulario_principal.bemVindoLabel.setText("Bem-Vinda " + Usuario.nome)
                else:
                    self.formulario_principal.bemVindoLabel.setText("Bem-Vindo " + Usuario.nome)

            else:
                ctypes.windll.user32.MessageBoxW(0, "Matricula ou Senha incorreta", "Atenção", 0)

        else:
            ctypes.windll.user32.MessageBoxW(0, "Você não digitou suas credencias", "Atenção", 0)

    def chamar_importar_ubs(self):
        if self.logado:
            self.e = ImportarExcel()
            #self.e.importar_excel_ubs()

        else:
            ctypes.windll.user32.MessageBoxW(0, "Usuário não logado. Entre com suas credenciais", "Atenção", 0)

    def chamar_inserir_dados(self):

        if self.logado:
            self.p = PreencherPlanilha()
            self.p.dadosUBS.show()
        else:
            ctypes.windll.user32.MessageBoxW(0, "Usuário não logado. Entre com suas credenciais", "Atenção", 0)

    def chamar_listar_dados(self):
        if self.logado:
            self.l = ListaOperacoes()
            self.l.listaUBS.show()
        else:
            ctypes.windll.user32.MessageBoxW(0, "Usuário não logado. Entre com suas credenciais", "Atenção", 0)


if __name__ == "__main__":
    import sys

    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    p = Principal()
    p.formulario_principal.showMaximized()
    sys.exit(app.exec_())
