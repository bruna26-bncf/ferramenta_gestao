from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QSpinBox
from PyQt5 import uic, QtWidgets, QtCore
from querys.dao import Dao
import ctypes
from PyQt5.QtGui import QDoubleValidator, QIntValidator


class PreencherPlanilha:
    dao = Dao()
    novos_dados = {}
    novos_dados_status = {}
    novos_dados_lastro = {}
    novos_dados_serie = {}
    novos_dados_estudo = {}
    novos_dados_aprovacao = {}
    novos_dados_estruturacao = {}
    novos_dados_liquidacao = {}
    ativarBusca = False
    ativarEdicaoUBS = False
    ativarEdicaoStatus = False
    ativarEdicaoEstudo = False
    ativarEdicaoAprovacao = False
    ativarEdicaoEstruturacao = False
    ativarEdicaoLiquidacao = False
    desativarEdicaoUBS = False
    desativarEdicaoEstudo = False
    desativarAprovacao = False
    desativarEdicaoEstruturacao = False
    desativarEdicaoLiquidacao = False
    versionamento = 0

    resultadogeral = 0
    resultadolastro = 0
    resultadoseries = 0
    qtddoseries = 0


    lista_ID = dao.ids_existentes()
    lista_funci = dao.funcis_bbbi()
    listaSeries = []
    serie = 0

    def __init__(self):
        #self.caminho = Caminho.caminho_ui()
        self.dadosUBS = uic.loadUi("formulario_dados.ui")
        self.dadosUBS.le_qtd_valores_mob_adquirido.returnPressed.connect(self.campos_alterados_liquidacao)
        self.dadosUBS.cb_ativo.currentTextChanged.connect(self.tipo_ativo)
        self.dadosUBS.cb_lastro.currentTextChanged.connect(self.tipo_lastro)
        self.dadosUBS.comboBox_ID.addItems(self.lista_ID)
        self.atualizacao_combo_box_id()
        self.atualizacao_combo_box_funci()
        self.dadosUBS.botaoBuscar.clicked.connect(self.funcao_buscar)
        self.dadosUBS.botaoAlterar_ubs.clicked.connect(self.funcao_habilitar_edicao_ubs)
        self.dadosUBS.botaoAlterarStatus.clicked.connect(self.funcao_habilitar_edicao_status)
        self.dadosUBS.botaoAlterar_estudo.clicked.connect(self.funcao_habilitar_edicao_estudo)
        self.dadosUBS.botaoAlterar_aprovacao.clicked.connect(self.funcao_habilitar_edicao_aprovacao)
        self.dadosUBS.botaoAlterar_estruturacao.clicked.connect(self.funcao_habilitar_edicao_estruturacao)
        self.dadosUBS.botaoAlterar_liquidacao.clicked.connect(self.funcao_habilitar_edicao_liquidacao)
        self.dadosUBS.botaoSalvar_ubs.clicked.connect(self.funcao_salvar_ubs)
        self.dadosUBS.botaoSalvarStatus.clicked.connect(self.funcao_salvar_status)
        self.dadosUBS.botaoSalvar_estudo.clicked.connect(self.funcao_salvar_estudo)
        self.dadosUBS.botaoSalvar_aprovacao.clicked.connect(self.funcao_salvar_aprovacao)
        self.dadosUBS.botaoSalvar_estruturacao.clicked.connect(self.funcao_salvar_estruturacao)
        self.dadosUBS.botaoSalvar_liquidacao.clicked.connect(self.funcao_salvar_liquidacao)
        self.dadosUBS.de_previsaoLiquidacao.setCalendarPopup(True)
        self.dadosUBS.de_dtLimiteEnvioProp.setCalendarPopup(True)
        self.dadosUBS.de_consulta_viab_tvm.setCalendarPopup(True)
        self.dadosUBS.de_consulta_upb.setCalendarPopup(True)
        self.dadosUBS.de_proposta_negocios.setCalendarPopup(True)
        self.dadosUBS.de_aprovacao_estudo_tecnico.setCalendarPopup(True)
        #self.dadosUBS.de_data_emissao.setCalendarPopup(True)
        #self.dadosUBS.de_data_vencimento_emissao.setCalendarPopup(True)
        #self.dadosUBS.de_data_inicial_juros.setCalendarPopup(True)
        #self.dadosUBS.de_data_final_juros.setCalendarPopup(True)
        #self.dadosUBS.de_data_inicial_amortizacao.setCalendarPopup(True)
        #self.dadosUBS.de_data_final_amortizacao.setCalendarPopup(True)
        self.dadosUBS.de_data_bookbuilding.setCalendarPopup(True)
        self.dadosUBS.de_data_liquidacao.setCalendarPopup(True)
        self.dadosUBS.de_previsaoLiquidacao.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_dtLimiteEnvioProp.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_consulta_viab_tvm.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_consulta_upb.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_proposta_negocios.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_aprovacao_estudo_tecnico.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_emissao.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_vencimento_emissao.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_inicial_juros.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_final_juros.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_inicial_amortizacao.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_final_amortizacao.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_data_bookbuilding.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_data_liquidacao.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.botaoIncluirFila.clicked.connect(self.incluir_nova_serie)
        self.funcao_desabilitar_edicao_ubs()
        self.funcao_desabilitar_edicao_status()
        self.funcao_desabilitar_edicao_estudo()
        self.funcao_desabilitar_edicao_aprovacao()
        self.funcao_desabilitar_edicao_estruturacao()
        self.funcao_desabilitar_edicao_liquidacao()
        self.header = self.dadosUBS.tabelaSeries.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
        #UBS Geral
        self.dadosUBS.le_valorEmissao.setValidator(QDoubleValidator())
        self.dadosUBS.le_partGarantiaFirme.setValidator(QDoubleValidator())
        self.dadosUBS.le_loteAdicionalMax.setValidator(QDoubleValidator())
        self.dadosUBS.le_premioResgAntBFF.setValidator(QDoubleValidator())
        self.dadosUBS.le_feeTotal.setValidator(QDoubleValidator())
        self.dadosUBS.le_feeCanal.setValidator(QDoubleValidator())
        #Lastro
        self.dadosUBS.le_lastroVolMedio.setValidator(QDoubleValidator())
        self.dadosUBS.le_lastroTicketMedio.setValidator(QDoubleValidator())
        self.dadosUBS.le_lastroVolTotalCarteira.setValidator(QDoubleValidator())
        self.dadosUBS.le_lastroVolDispCessao.setValidator(QDoubleValidator())
        self.dadosUBS.le_lastroInadMedia.setValidator(QDoubleValidator())
        #serie
        self.dadosUBS.le_prazo_total.setValidator(QDoubleValidator())
        self.dadosUBS.le_carencia_principal.setValidator(QDoubleValidator())
        self.dadosUBS.le_carencia_juros.setValidator(QDoubleValidator())
        self.dadosUBS.le_inicio_pagamento_principal.setValidator(QDoubleValidator())
        self.dadosUBS.le_taxa.setValidator(QDoubleValidator())
        #estudo
        self.dadosUBS.le_prazo_venda_upb.setValidator(QDoubleValidator())
        self.dadosUBS.le_limite_global_rc.setValidator(QDoubleValidator())
        self.dadosUBS.le_limite_especifico_rc.setValidator(QDoubleValidator())
        #Aprovacao
        self.dadosUBS.le_valor_gf_estudo_tecnico.setValidator(QDoubleValidator())
        #Estruturação
        self.dadosUBS.le_numero_emissao.setValidator(QIntValidator())
        self.dadosUBS.le_classe.setValidator(QIntValidator())
        self.dadosUBS.le_series_estruturacao.setValidator(QIntValidator())
        # self.dadosUBS.le_taxa_operacao.setValidator(QDoubleValidator())
        # self.dadosUBS.le_pu_emissao.setValidator(QDoubleValidator())
        self.dadosUBS.le_fee_estrturacao.setValidator(QDoubleValidator())
        self.dadosUBS.le_fee_sucesso.setValidator(QDoubleValidator())
        self.dadosUBS.le_fee_garantia_firme.setValidator(QDoubleValidator())
        self.dadosUBS.le_outras_fees.setValidator(QDoubleValidator())
        #Liquidacao
        self.dadosUBS.le_pu_liquidacao.setValidator(QDoubleValidator())
        self.dadosUBS.le_volume_adquirido.setValidator(QDoubleValidator())
        self.dadosUBS.le_alocacao_upb_mercado_primario.setValidator(QDoubleValidator())
        self.dadosUBS.le_demanda_upb_merc_primario.setValidator(QDoubleValidator())
        self.dadosUBS.le_fee_upb_mercado_primario.setValidator(QDoubleValidator())
        self.dadosUBS.le_fee_retirada_dist_mercado_secundario.setValidator(QDoubleValidator())
        self.dadosUBS.le_fee_recebida_BBBI.setValidator(QDoubleValidator())
        self.dadosUBS.le_qtd_valores_mob_adquirido.setValidator(QDoubleValidator())

        self.dadosUBS.tabWidget.setTabVisible(0, True)
        self.dadosUBS.tabWidget.setTabVisible(1, False)
        self.dadosUBS.tabWidget.setTabVisible(2, False)
        self.dadosUBS.tabWidget.setTabVisible(3, False)
        self.dadosUBS.tabWidget.setTabVisible(4, False)
        self.dadosUBS.botaoIncluir.clicked.connect(self.funcao_inserir_tab)
        self.dadosUBS.botaoTeste.clicked.connect(self.capturar_dados)


    def tipo_ativo(self):
        try:
            print(self.dadosUBS.cb_ativo.currentText())
            if self.dadosUBS.cb_ativo.currentText() in ['CRI', 'CRA', 'FIDC', 'Debêntures Securitizadas'] and self.ativarEdicaoUBS:
                self.dadosUBS.cb_lastro.setEnabled(True)
                print(self.dadosUBS.cb_lastro.currentText())
                self.tipo_lastro()
            else:
                self.dadosUBS.cb_lastro.setEnabled(False)
                self.dadosUBS.cb_lastro.setCurrentText('')
                self.limpar_lastros()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - tipo_ativo", 0)

    def tipo_lastro(self):
        try:
            print(self.dadosUBS.cb_lastro.currentText())
            if self.dadosUBS.cb_lastro.currentText() == 'Direitos Creditórios':
                self.dadosUBS.simResolvencia.setEnabled(True)
                self.dadosUBS.naoResolvencia.setEnabled(True)
                self.dadosUBS.simSubordinacao.setEnabled(True)
                self.dadosUBS.naoSubordinacao.setEnabled(True)
                self.dadosUBS.simSeguro.setEnabled(True)
                self.dadosUBS.naoSeguro.setEnabled(True)
                self.dadosUBS.le_lastroVolMedio.setReadOnly(False)
                self.dadosUBS.le_lastroTicketMedio.setReadOnly(False)
                self.dadosUBS.le_lastroVolTotalCarteira.setReadOnly(False)
                self.dadosUBS.le_lastroVolDispCessao.setReadOnly(False)
                self.dadosUBS.le_lastroInadMedia.setReadOnly(False)
                self.dadosUBS.te_lastroConcCarteira.setReadOnly(False)
                self.dadosUBS.te_lastroIndiceMedioPagAtraso.setReadOnly(False)
                self.dadosUBS.te_lastro10MaioresDeve.setReadOnly(False)
                self.dadosUBS.te_lastroPrazoMedioPagAtraso.setReadOnly(False)
                self.dadosUBS.te_astroPrazoMedioCarteira.setReadOnly(False)
                self.dadosUBS.te_IndiceMedioDistratoDevol.setReadOnly(False)
            else:
                self.limpar_lastros()
                self.dadosUBS.simResolvencia.setEnabled(False)
                self.dadosUBS.naoResolvencia.setEnabled(False)
                self.dadosUBS.simSubordinacao.setEnabled(False)
                self.dadosUBS.naoSubordinacao.setEnabled(False)
                self.dadosUBS.simSeguro.setEnabled(False)
                self.dadosUBS.naoSeguro.setEnabled(False)
                self.dadosUBS.le_lastroVolMedio.setReadOnly(True)
                self.dadosUBS.le_lastroTicketMedio.setReadOnly(True)
                self.dadosUBS.le_lastroVolTotalCarteira.setReadOnly(True)
                self.dadosUBS.le_lastroVolDispCessao.setReadOnly(True)
                self.dadosUBS.le_lastroInadMedia.setReadOnly(True)
                self.dadosUBS.te_lastroConcCarteira.setReadOnly(True)
                self.dadosUBS.te_lastroIndiceMedioPagAtraso.setReadOnly(True)
                self.dadosUBS.te_lastro10MaioresDeve.setReadOnly(True)
                self.dadosUBS.te_lastroPrazoMedioPagAtraso.setReadOnly(True)
                self.dadosUBS.te_astroPrazoMedioCarteira.setReadOnly(True)
                self.dadosUBS.te_IndiceMedioDistratoDevol.setReadOnly(True)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - tipo_lastro", 0)

    def atualizacao_combo_box_id(self):
        try:
            self.dadosUBS.comboBox_ID.clear()
            self.lista_ID = self.dao.ids_existentes()
            self.dadosUBS.comboBox_ID.addItems(self.lista_ID)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - atualizacao_combo_box_id", 0)

    def atualizacao_combo_box_funci(self):
        try:
            self.dadosUBS.cb_assessorBBBI.clear()
            self.lista_funci = self.dao.funcis_bbbi()
            self.dadosUBS.cb_assessorBBBI.addItems(self.lista_funci)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - atualizacao_combo_box_funci", 0)

    def limparVariaveis(self):
        try:
            self.ativarBusca = False
            self.ativarEdicaoUBS = False
            self.desativarEdicaoUBS = False
            self.ativarEdicaoEstudo = False
            self.desativarEdicaoEstudo = False
            self.ativarEdicaoAprovacao = False
            self.desativarEdicaoAprovacao = False
            self.novos_dados = {}
            self.novos_dados_lastro = {}
            self.novos_dados_serie = {}
            self.novos_dados_estudo = {}
            self.novos_dados_aprovacao = {}
            self.novos_dados_liquidacao = {}
            self.listaSeries = []
            self.serie = 0
            self.dadosUBS.seriesFila.setText(str(0))
            self.versionamento = 0
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - limparVariaveis", 0)

    def funcao_buscar(self, id='', nome=''):
        try:
            print(id)
            print(nome)
            self.limparVariaveis()
            self.limpar_formulario()
            self.ativarBusca = True

            if self.dadosUBS.comboBox_ID.currentText() != '':
                self.id = str(self.dadosUBS.comboBox_ID.currentText())[0:13]
            else:
                self.id = id
                self.dadosUBS.comboBox_ID.setCurrentText(id + " - " + nome)
                print()


            print(self.id)
            if self.insere_dados_gerais_ubs():
                self.insere_dados_status()
                self.insere_dados_cliente()
                self.insere_dados_series()
                self.insere_dados_lastro()
                self.insere_dados_estudo()
                self.insere_dados_aprovacao()
                self.insere_dados_estruturacao()
                self.insere_dados_liquidacao()
                self.campos_alterados_estudo()
                self.funcao_desabilitar_edicao_ubs()
                self.funcao_desabilitar_edicao_estudo()
                self.funcao_desabilitar_edicao_aprovacao()
                self.funcao_desabilitar_edicao_estruturacao()
                self.funcao_desabilitar_edicao_estruturacao()
                self.funcao_desabilitar_edicao_estruturacao()
                self.funcao_desabilitar_edicao_liquidacao()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_buscar", 0)

    def insere_dados_gerais_ubs(self):
        try:
            print("Cheguei aqui dados Gerais UBS")
            self.retorno_dados = self.dao.informacoes_id(self.id)

            if self.retorno_dados != []:
                print(self.retorno_dados)
                self.carregarCamposFormularioUBS(self.retorno_dados)
                return True
            else:
                ctypes.windll.user32.MessageBoxW(0, "Dados da UBS inexistentes para esse ID", "UBS", 0)
                return False
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_gerais_ubs", 0)

    def insere_dados_status(self):
        try:
            print("Cheguei aqui Status")

            self.retorno_dados_status = self.dao.informacoes_status(self.id)

            if self.retorno_dados_status != []:
                print(self.retorno_dados_status)
                self.carregarCamposFormularioStatus(self.retorno_dados_status)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Status inexistentes para esse cliente. Atualize.", "Status", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_status", 0)

    def insere_dados_cliente(self):
        try:
            print("Cheguei aqui Clientes Geper")
            cnpj = (self.dadosUBS.cnpj_emissor.text()).replace('/','').replace('.', '').replace('-', '')
            print(cnpj)
            self.retorno_dados_cliente = self.dao.informacoes_cliente(cnpj)

            if self.retorno_dados_cliente != []:
                print(self.retorno_dados_cliente)
                self.carregarCamposFormularioCliente(self.retorno_dados_cliente)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Dados do Cliente inexistentes para esse ID", "Cliente", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_cliente", 0)

    def insere_dados_lastro(self):
        try:
            print("Cheguei aqui Lastros")
            self.retorno_dados_lastro = self.dao.informacoes_lastro(self.id)

            if self.retorno_dados_lastro != []:
                print(self.retorno_dados_lastro)
                self.carregarCamposFormularioLastros(self.retorno_dados_lastro)
            else:
                pass
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_lastro", 0)

    def insere_dados_series(self):
        try:
            print("Cheguei aqui series")
            self.retorno_dados_series = self.dao.informacoes_series(self.id)

            if self.retorno_dados_series != []:
                print(self.retorno_dados_series)
                self.preencher_tabela_series(self.retorno_dados_series)
            else:
                pass
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_series", 0)

    def insere_dados_estudo(self):
        try:
            print("Cheguei aqui series")
            self.retorno_dados_estudo = self.dao.informacoes_estudo(self.id)

            if self.retorno_dados_estudo != []:
                print(self.retorno_dados_estudo)
                self.carregarCamposFormularioEstudo(self.retorno_dados_estudo)
            else:
                pass
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_estudo", 0)

    def insere_dados_aprovacao(self):
        try:
            print("Cheguei aqui series")
            self.retorno_dados_aprovacao = self.dao.informacoes_aprovacao(self.id)

            if self.retorno_dados_aprovacao != []:
                print(self.retorno_dados_aprovacao)
                self.carregarCamposFormularioAprovacao(self.retorno_dados_aprovacao)
            else:
                pass
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_aprovacao", 0)

    def insere_dados_estruturacao(self):
        try:
            print("Cheguei aqui series")
            self.retorno_dados_estruturacao = self.dao.informacoes_estruturacao(self.id)

            if self.retorno_dados_estruturacao != []:
                print(self.retorno_dados_estruturacao)
                self.carregarCamposFormularioEstruturacao(self.retorno_dados_estruturacao)
            else:
                pass
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_estruturacao", 0)

    def insere_dados_liquidacao(self):
        try:
            print("Cheguei aqui series")
            self.setar_dados_padronizados()
            self.retorno_dados_liquidacao = self.dao.informacoes_liquidacao(self.id)

            if self.retorno_dados_liquidacao != []:
                print(self.retorno_dados_liquidacao)
                self.carregarCamposFormularioLiquidacao(self.retorno_dados_liquidacao)
            else:
                pass
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - insere_dados_liquidacao", 0)

    def setar_dados_padronizados(self):
        try:
            self.dadosUBS.le_carteira_rm.setText(str("Negociação"))
            self.dadosUBS.le_grupo_rm.setText(str("Grupo Mercado de Capitais"))
            self.dadosUBS.le_livro_rm.setText(str("333 Underwriting"))
            self.dadosUBS.le_categoria_contabil.setText(str("1"))
            self.dadosUBS.le_camara_registro.setText(str("CETIP"))
            self.dadosUBS.le_codigo_grupo.setText(str("22"))
            self.dadosUBS.le_grupo.setText(str("MERCADO DE CAPITAIS"))
            self.dadosUBS.le_codigo_livro.setText(str("150"))
            self.dadosUBS.le_livro.setText(str("UNDERWRITING"))
            self.dadosUBS.le_codigo_sub_livro.setText(str("37"))
            self.dadosUBS.le_sub_livro.setText(str("MOEDA NACIONAL"))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - setar_dados_padronizados", 0)

    def carregarCamposFormularioStatus(self, dados):
        try:
            self.dadosUBS.comboBox_status.setCurrentText(str(dados[0][0]))
            self.dadosUBS.te_motivo_status.setText(str(dados[0][1]))

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioStatus", 0)

    def carregarCamposFormularioCliente(self, dados):
        try:
            print("cheguei aqui nos dados da GEPER")
            self.dadosUBS.le_mci.setText(str(dados[0][0]))
            self.dadosUBS.le_grupo_economico.setText(str(dados[0][2]))
            self.dadosUBS.le_nome_grupo_economico.setText(str(dados[0][3]))
            self.dadosUBS.le_uor.setText(str(dados[0][4]))

            print(dados[0][5])
            if dados[0][5] is not None:
                self.dadosUBS.le_cep.setText(str(dados[0][5][0]))
                self.dadosUBS.le_cep.setText(str(dados[0][5][0]))
            else:
                self.dadosUBS.le_cep.setText(str("0"))
                self.dadosUBS.le_cep.setText(str("0"))

            self.dadosUBS.le_prefixo.setText(str(dados[0][6]))
            self.dadosUBS.le_carteira.setText(str(dados[0][7]))

            print(dados[0][8])
            if dados[0][8] is not None:
                self.dadosUBS.le_agencia.setText(str(dados[0][8][0]["prefixo"]))
                self.dadosUBS.le_conta.setText(str(dados[0][8][0]["conta"]))
            else:
                self.dadosUBS.le_agencia.setText(str("0"))
                self.dadosUBS.le_conta.setText(str("0"))

            self.dadosUBS.le_uor_diretoria.setText(str(dados[0][9]))
            self.dadosUBS.le_prefixo_diretoria.setText(str(dados[0][10]))
            self.dadosUBS.le_nome_diretoria.setText(str(dados[0][11]))

            self.dadosUBS.le_uor_regional.setText(str(dados[0][12]))
            self.dadosUBS.le_prefixo_regional.setText(str(dados[0][13]))
            self.dadosUBS.le_nome_regional.setText(str(dados[0][14]))

            self.dadosUBS.le_uor_super.setText(str(dados[0][15]))
            self.dadosUBS.le_prefixo_super.setText(str(dados[0][16]))
            self.dadosUBS.le_nome_super.setText(str(dados[0][17]))

            self.dadosUBS.le_matricula_gerente_geral.setText(str(dados[0][18]))
            self.dadosUBS.le_nome_gerente_geral.setText(str(dados[0][19]))

            self.dadosUBS.le_matricula_gerente_negocios.setText(str(dados[0][20]))
            self.dadosUBS.le_nome_gerente_negocios.setText(str(dados[0][21]))

            self.dadosUBS.le_matricula_gerente_relacionamento.setText(str(dados[0][22]))
            self.dadosUBS.le_nome_gerente_relacionamento.setText(str(dados[0][23]))

            if dados[0][24] is not None:
                self.dadosUBS.le_limite_aprovado.setText(str("{:,.2f}".format(dados[0][24]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_aprovado.setText(str("0,00"))

            if dados[0][25] is not None:
                self.dadosUBS.le_limite_disponivel.setText(str("{:,.2f}".format(dados[0][25]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_disponivel.setText(str("0,00"))

            if dados[0][26] is not None:
                self.dadosUBS.le_limite_aprovado_tvm.setText(str("{:,.2f}".format(dados[0][26]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_aprovado_tvm.setText(str("0,00"))

            if dados[0][27] is not None:
                self.dadosUBS.le_limite_disponivel_tvm.setText(str("{:,.2f}".format(dados[0][27]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_disponivel_tvm.setText(str("0,00"))

            if dados[0][28] is not None:
                self.dadosUBS.le_limite_aprovado_distribuicao.setText(str("{:,.2f}".format(dados[0][28]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_aprovado_distribuicao.setText(str("0,00"))

            if dados[0][29] is not None:
                self.dadosUBS.le_limite_disponivel_distribuicao.setText(str("{:,.2f}".format(dados[0][29]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_disponivel_distribuicao.setText(str("0,00"))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioCliente", 0)

    def carregarCamposFormularioEstudo(self, dados):
        try:
            self.dadosUBS.cb_assessorBBBI.setCurrentText(str(dados[0][2]))
            self.dadosUBS.cb_estrategia_distribuicao.setCurrentText(str(dados[0][3]))

            if dados[0][4] == 1:
                self.dadosUBS.simTVM.setChecked(True)
            else:
                self.dadosUBS.naoTVM.setChecked(True)

            if dados[0][5] == 1:
                self.dadosUBS.simUPB.setChecked(True)
            else:
                self.dadosUBS.naoUPB.setChecked(True)

            if dados[0][6] is not None:
                self.dadosUBS.le_prazo_venda_upb.setText(str("{:,.2f}".format(dados[0][6]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_prazo_venda_upb.setText(str("0,00"))

            if dados[0][7] is not None:
                self.dadosUBS.le_impactoxprobabilidade.setText(str("{:,.2f}".format(dados[0][7]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_impactoxprobabilidade.setText(str("0,00"))

            if dados[0][8] is not None:
                self.dadosUBS.le_limite_global_rc.setText(str("{:,.2f}".format(dados[0][8]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_global_rc.setText(str("0,00"))

            if dados[0][9] is not None:
                self.dadosUBS.le_limite_especifico_rc.setText(str("{:,.2f}".format(dados[0][9]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_limite_especifico_rc.setText(str("0,00"))

            self.dadosUBS.de_consulta_viab_tvm.setDateTime(datetime((dados[0][10]).year, (dados[0][10]).month, (dados[0][10]).day))
            self.dadosUBS.de_consulta_upb.setDateTime(datetime((dados[0][11]).year, (dados[0][11]).month, (dados[0][11]).day))
            self.dadosUBS.de_proposta_negocios.setDateTime(datetime((dados[0][12]).year, (dados[0][12]).month, (dados[0][12]).day))

            self.dadosUBS.te_retorno_consulta_viabilidade_tvm.setText(str(dados[0][13]))
            self.dadosUBS.te_retorno_consulta_upb.setText(str(dados[0][14]))
            self.dadosUBS.te_resultado_proposta_negocios.setText(str(dados[0][15]))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioEstudo", 0)

    def carregarCamposFormularioAprovacao(self, dados):
        try:
            self.dadosUBS.le_numero_estudo_tecnico.setText(str(dados[0][2]))
            self.dadosUBS.de_aprovacao_estudo_tecnico.setDateTime(datetime((dados[0][3]).year, (dados[0][3]).month, (dados[0][3]).day))
            self.dadosUBS.le_valor_gf_estudo_tecnico.setText(str("{:,.2f}".format(dados[0][4]).replace(",", "X").replace(".", ",").replace("X", ".")))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioEstudo", 0)

    def carregarCamposFormularioEstruturacao(self, dados):
        try:
            self.dadosUBS.le_nomeSecuritizadoraAdm.setText(str(dados[0][2]))
            self.dadosUBS.le_cnpjSecuritizadoraAdm.setText((str(dados[0][3])).zfill(14))
            self.dadosUBS.le_nomeAgendeFiduciario.setText(str(dados[0][4]))
            self.dadosUBS.le_cnpjAgendeFiduciario.setText((str(dados[0][5])).zfill(14))

            if dados[0][6] == 1:
                self.dadosUBS.cb_especie.setCurrentText('Quirografária')
            elif dados[0][6] == 2:
                self.dadosUBS.cb_especie.setCurrentText('Subordinada')
            elif dados[0][6] == 3:
                self.dadosUBS.cb_especie.setCurrentText('Garantia real')
            elif dados[0][6] == 4:
                self.dadosUBS.cb_especie.setCurrentText('Flutuante')

            if dados[0][7] == 1:
                self.dadosUBS.cb_especie.setCurrentText('CDI')
            elif dados[0][7] == 4:
                self.dadosUBS.cb_especie.setCurrentText('IPCA')

            if dados[0][8] == 1:
                self.dadosUBS.cb_indexador_operacao.setCurrentText('%')
            elif dados[0][8] == 2:
                self.dadosUBS.cb_indexador_operacao.setCurrentText('Spread')

            self.dadosUBS.le_numero_emissao.setText(str(dados[0][9]))
            self.dadosUBS.le_classe.setText(str(dados[0][10]))
            self.dadosUBS.le_series_estruturacao.setText(str(dados[0][11]))

            #self.dadosUBS.le_taxa_operacao.setText(str("{:,.2f}".format(dados[0][12]).replace(",", "X").replace(".", ",").replace("X", ".")))
            #self.dadosUBS.le_pu_emissao.setText(str("{:,.2f}".format(dados[0][13]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_fee_estrturacao.setText(str("{:,.2f}".format(dados[0][14]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_fee_sucesso.setText(str("{:,.2f}".format(dados[0][15]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_fee_garantia_firme.setText(str("{:,.2f}".format(dados[0][16]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_outras_fees.setText(str("{:,.2f}".format(dados[0][17]).replace(",", "X").replace(".", ",").replace("X", ".")))

            self.dadosUBS.le_fee_distribuicao_canal.setText(str(dados[0][18]))

            #self.dadosUBS.de_data_emissao.setDateTime(datetime((dados[0][19]).year, (dados[0][19]).month, (dados[0][19]).day))
            #self.dadosUBS.de_data_vencimento_emissao.setDateTime(datetime((dados[0][20]).year, (dados[0][20]).month, (dados[0][20]).day))
            #self.dadosUBS.de_data_inicial_juros.setDateTime(datetime((dados[0][21]).year, (dados[0][21]).month, (dados[0][21]).day))
            #self.dadosUBS.de_data_final_juros.setDateTime(datetime((dados[0][22]).year, (dados[0][22]).month, (dados[0][22]).day))
            #self.dadosUBS.de_data_inicial_amortizacao.setDateTime(datetime((dados[0][23]).year, (dados[0][23]).month, (dados[0][23]).day))
            #self.dadosUBS.de_data_final_amortizacao.setDateTime(datetime((dados[0][24]).year, (dados[0][24]).month, (dados[0][24]).day))
            self.dadosUBS.de_data_bookbuilding.setDateTime(datetime((dados[0][25]).year, (dados[0][25]).month, (dados[0][25]).day))
            self.dadosUBS.de_data_liquidacao.setDateTime(datetime((dados[0][26]).year, (dados[0][26]).month, (dados[0][26]).day))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioEstruturacao", 0)

    def carregarCamposFormularioLiquidacao(self, dados):
        try:
            print("cheguei aqui nos dados gerais da Liquidação")
            self.dadosUBS.le_codigo_ativo.setText(str(dados[0][2]))
            self.dadosUBS.le_insi.setText(str(dados[0][3]))

            self.dadosUBS.le_pu_liquidacao.setText(str("{:,.2f}".format(dados[0][4]).replace(",", "X").replace(".", ",").replace("X", ".")))

            if dados[0][5] == 1:
                self.dadosUBS.simGFSE.setChecked(True)
            else:
                self.dadosUBS.naoGFSE.setChecked(True)

            self.dadosUBS.le_volume_adquirido.setText(str("{:,.2f}".format(dados[0][6]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_qtd_valores_mob_adquirido.setText(str("{:,.2f}".format(dados[0][7]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_porcent_sobras.setText(str("{:,.2f}".format(dados[0][8]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_prob_colocacao_realizada.setText(str(dados[0][9]))
            self.dadosUBS.le_demanda_upb_merc_primario.setText(str("{:,.2f}".format(dados[0][10]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_alocacao_upb_mercado_primario.setText(str("{:,.2f}".format(dados[0][11]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_fee_upb_mercado_primario.setText(str("{:,.2f}".format(dados[0][12]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_fee_retirada_dist_mercado_secundario.setText(str("{:,.2f}".format(dados[0][13]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_fee_recebida_BBBI.setText(str("{:,.2f}".format(dados[0][14]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_carteira_rm.setText(str(dados[0][15]))
            self.dadosUBS.le_grupo_rm.setText(str(dados[0][16]))
            self.dadosUBS.le_livro_rm.setText(str(dados[0][17]))
            self.dadosUBS.le_categoria_contabil.setText(str(dados[0][18]))
            self.dadosUBS.le_camara_registro.setText(str(dados[0][19]))
            self.dadosUBS.le_codigo_grupo.setText(str(dados[0][20]))
            self.dadosUBS.le_grupo.setText(str(dados[0][21]))
            self.dadosUBS.le_codigo_livro.setText(str(dados[0][22]))
            self.dadosUBS.le_livro.setText(str(dados[0][23]))
            self.dadosUBS.le_codigo_sub_livro.setText(str(dados[0][24]))
            self.dadosUBS.le_sub_livro.setText(str(dados[0][25]))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro -carregarCamposFormularioLiquidacao", 0)

    def carregarCamposFormularioUBS(self, dados):
        try:
            print("cheguei aqui nos dados gerais da UBS")

            self.dadosUBS.cb_ativo.setCurrentText(str(dados[0][0]))
            self.dadosUBS.nome_emissor.setText(str(dados[0][1]))
            self.dadosUBS.cnpj_emissor.setText((str(dados[0][2])).zfill(14))

            if dados[0][4] == 24933830000130:
                self.dadosUBS.cb_cnpjCoordenador.setCurrentText('24.933.830/0001-30')
            elif dados[0][4] == 2819125000173:
                self.dadosUBS.cb_cnpjCoordenador.setCurrentText('02.819.125/0001-73')

            self.dadosUBS.coordenador_lider.setText(str(dados[0][5]))
            self.dadosUBS.demais_coordenadores.setText(str(dados[0][6]))

            if dados[0][7] == 1:
                self.dadosUBS.simLei.setChecked(True)
            else:
                self.dadosUBS.naoLei.setChecked(True)

            if dados[0][8] == 1:
                self.dadosUBS.simConversiveisAcao.setChecked(True)
            else:
                self.dadosUBS.naoConversiveisAcao.setChecked(True)

            if dados[0][9] == 1:
                self.dadosUBS.simLoteAdicional.setChecked(True)
            else:
                self.dadosUBS.naoLoteAdicional.setChecked(True)

            if dados[0][10] == 1:
                self.dadosUBS.simHaveraEsforcos.setChecked(True)
            else:
                self.dadosUBS.naoHaveraEsforcos.setChecked(True)

            if dados[0][11] == 1:
                self.dadosUBS.simTeraGarantia.setChecked(True)
            else:
                self.dadosUBS.naoTeraGarantia.setChecked(True)

            if dados[0][12] == 1:
                self.dadosUBS.simPermiteResgate.setChecked(True)
            else:
                self.dadosUBS.naoPermiteResgate.setChecked(True)

            if dados[0][13] == 1:
                self.dadosUBS.simMarketMac.setChecked(True)
            else:
                self.dadosUBS.naoMarketMac.setChecked(True)

            if dados[0][14] == 1:
                self.dadosUBS.simBalancoAuditado.setChecked(True)
            else:
                self.dadosUBS.naoBalancoAuditado.setChecked(True)

            if dados[0][15] == 1:
                self.dadosUBS.simBalancoDivulgado.setChecked(True)
            else:
                self.dadosUBS.naoBalancoDivulgado.setChecked(True)

            if dados[0][16] == 1:
                self.dadosUBS.simRFP.setChecked(True)
            else:
                self.dadosUBS.naoRFP.setChecked(True)

            if dados[0][42] == 1:
                self.dadosUBS.simESG.setChecked(True)
            else:
                self.dadosUBS.naoESG.setChecked(True)

            self.dadosUBS.cb_nomeCoordenador.setCurrentText(str(dados[0][3]))
            self.dadosUBS.cb_legislacaoCVM.setCurrentText(str(dados[0][17]))
            self.dadosUBS.cb_ritoRegistro.setCurrentText(str(dados[0][18]))

            print(str(dados[0][18]), str(dados[0][17]), str(dados[0][19]))

            self.dadosUBS.cb_documentoOferta.setCurrentText(str(dados[0][19]))
            self.dadosUBS.cb_regimeColocacao.setCurrentText(str(dados[0][20]))
            self.dadosUBS.cb_ratingEmissora.setCurrentText(str(dados[0][21]))
            self.dadosUBS.cb_ratingOferta.setCurrentText(str(dados[0][22]))
            self.dadosUBS.cb_probabilidadeColocacao.setCurrentText(str(dados[0][23]))
            self.dadosUBS.cb_tipoEmissor.setCurrentText(str(dados[0][24]))
            self.dadosUBS.cb_fee_forma_calculo.setCurrentText(str(dados[0][43]))

            if dados[0][25] is not None:
                self.dadosUBS.le_valorEmissao.setText(str("{:,.2f}".format(dados[0][25]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_valorEmissao.setText(str("0,00"))

            self.dadosUBS.te_destinacaoRecursos.setText(str(dados[0][26]))

            if dados[0][27] is not None:
                self.dadosUBS.le_partGarantiaFirme.setText(str("{:,.2f}".format(dados[0][27]).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_partGarantiaFirme.setText(str("0,00"))

            if dados[0][28] is not None:
                self.dadosUBS.le_loteAdicionalMax.setText(str("{:,.2f}".format((dados[0][28])*100).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_loteAdicionalMax.setText(str("0,00"))

            if dados[0][29] is not None:
                self.dadosUBS.le_premioResgAntBFF.setText(str("{:,.2f}".format((dados[0][29])*100).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_premioResgAntBFF.setText(str("0,00"))

            self.dadosUBS.te_garantia.setText(str(dados[0][30]))

            if dados[0][31] is not None:
                self.dadosUBS.le_feeTotal.setText(str("{:,.2f}".format((dados[0][31])*100).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_feeTotal.setText(str("0,00"))

            if dados[0][32] is not None:
                self.dadosUBS.le_feeCanal.setText(str("{:,.2f}".format((dados[0][32])*100).replace(",", "X").replace(".", ",").replace("X", ".")))
            else:
                self.dadosUBS.le_feeCanal.setText(str("0,00"))

            if dados[0][33] is not None:
                if (dados[0][33]).isnumeric():
                    self.dadosUBS.le_outrasFees.setText(str("{:,.2f}".format((float(dados[0][33]))*100).replace(",", "X").replace(".", ",").replace("X", ".")))
                else:
                    self.dadosUBS.le_outrasFees.setText(str("0,00"))
            else:
                self.dadosUBS.le_outrasFees.setText(str("0,00"))

            self.dadosUBS.spinBox_series.setValue(int(dados[0][34]))
            self.dadosUBS.de_previsaoLiquidacao.setDateTime(datetime((dados[0][35]).year, (dados[0][35]).month, (dados[0][35]).day))
            self.dadosUBS.de_dtLimiteEnvioProp.setDateTime(datetime((dados[0][36]).year, (dados[0][36]).month, (dados[0][36]).day))
            self.dadosUBS.le_empresaAudit.setText(str(dados[0][37]))
            self.dadosUBS.te_justificativa.setText(str(dados[0][38]))
            self.dadosUBS.te_covenants.setText(str(dados[0][39]))
            self.dadosUBS.te_observacoes.setText(str(dados[0][40]))
            self.dadosUBS.versao.setText(str(dados[0][41]))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioUBS", 0)

    def carregarCamposFormularioLastros(self, dadoslastro):
        try:
            print("cheguei aqui nos dados lastro")

            if dadoslastro[0][2] == 1:
                self.dadosUBS.simResolvencia.setChecked(True)
            else:
                self.dadosUBS.naoResolvencia.setChecked(True)

            if dadoslastro[0][3] == 1:
                self.dadosUBS.simSubordinacao.setChecked(True)
            else:
                self.dadosUBS.naoSubordinacao.setChecked(True)

            if dadoslastro[0][4] == 1:
                self.dadosUBS.simSeguro.setChecked(True)
            else:
                self.dadosUBS.naoSeguro.setChecked(True)

            if dadoslastro[0][5] == 1:
                self.dadosUBS.cb_lastro.setCurrentText(str('Direitos Creditórios'))
            elif dadoslastro[0][5] == 2:
                self.dadosUBS.cb_lastro.setCurrentText(str('Título de Dívida'))

            self.dadosUBS.le_lastroVolMedio.setText(str("{:,.2f}".format(dadoslastro[0][6]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_lastroTicketMedio.setText(str("{:,.2f}".format(dadoslastro[0][7]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_lastroVolTotalCarteira.setText(str("{:,.2f}".format(dadoslastro[0][10]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_lastroVolDispCessao.setText(str("{:,.2f}".format(dadoslastro[0][12]).replace(",", "X").replace(".", ",").replace("X", ".")))
            self.dadosUBS.le_lastroInadMedia.setText(str("{:,.2f}".format(dadoslastro[0][13]).replace(",", "X").replace(".", ",").replace("X", ".")))

            self.dadosUBS.te_lastroConcCarteira.setText(str(dadoslastro[0][8]))
            self.dadosUBS.te_lastro10MaioresDeve.setText(str(dadoslastro[0][9]))
            self.dadosUBS.te_astroPrazoMedioCarteira.setText(str(dadoslastro[0][11]))
            self.dadosUBS.te_lastroIndiceMedioPagAtraso.setText(str(dadoslastro[0][14]))
            self.dadosUBS.te_lastroPrazoMedioPagAtraso.setText(str(dadoslastro[0][15]))
            self.dadosUBS.te_IndiceMedioDistratoDevol.setText(str(dadoslastro[0][16]))

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - carregarCamposFormularioLastros", 0)

    def preencher_tabela_series(self, lista):
        try:
            self.dadosUBS.tabelaSeries.clear()
            self.dadosUBS.tabelaSeries.setHorizontalHeaderLabels(['Tipo', 'Prazo total (meses)', 'Carência Principal (meses)',
                                                                  'Pagamento Principal', 'Inicio Pgto Principal (meses)',
                                                                  'Carência Juros (meses),',
                                                                  'Pagamento Juros', 'Indexador', 'Informar referência da NTN-B',
                                                                  'Taxa', 'Público Alvo Mercado Primário',
                                                                  'Público Alvo Mercado Secundário'])

            print(lista)

            linhas = len(lista)
            self.dadosUBS.tabelaSeries.setRowCount(linhas)

            for linha in range(linhas):
                self.dadosUBS.tabelaSeries.setItem(linha, 0, QTableWidgetItem(str(lista[linha][0])))

                if (lista[linha][1]) is not None:
                    self.dadosUBS.tabelaSeries.setItem(linha, 1, QTableWidgetItem(str("{:,.2f}".format(lista[linha][1]).replace(",", "X").replace(".", ",").replace("X", "."))))
                else:
                    self.dadosUBS.tabelaSeries.setItem(linha, 1, QTableWidgetItem(str("0,00")))

                if (lista[linha][2]) is not None:
                    self.dadosUBS.tabelaSeries.setItem(linha, 2, QTableWidgetItem(str("{:,.2f}".format(lista[linha][2]).replace(",", "X").replace(".", ",").replace("X", "."))))
                else:
                    self.dadosUBS.tabelaSeries.setItem(linha, 2, QTableWidgetItem(str("0,00")))

                self.dadosUBS.tabelaSeries.setItem(linha, 3, QTableWidgetItem(str(lista[linha][3])))

                if (lista[linha][4]) is not None:
                    self.dadosUBS.tabelaSeries.setItem(linha, 4, QTableWidgetItem(str("{:,.2f}".format(lista[linha][4]).replace(",", "X").replace(".", ",").replace("X", "."))))
                else:
                    self.dadosUBS.tabelaSeries.setItem(linha, 4, QTableWidgetItem(str("0,00")))

                if (lista[linha][5]) is not None:
                    self.dadosUBS.tabelaSeries.setItem(linha, 5, QTableWidgetItem(str("{:,.2f}".format(lista[linha][5]).replace(",", "X").replace(".", ",").replace("X", "."))))
                else:
                    self.dadosUBS.tabelaSeries.setItem(linha, 5, QTableWidgetItem(str("0,00")))

                self.dadosUBS.tabelaSeries.setItem(linha, 6, QTableWidgetItem(str(lista[linha][6])))

                self.dadosUBS.tabelaSeries.setItem(linha, 7, QTableWidgetItem(str(lista[linha][7])))

                if (lista[linha][8]) != 'nan':
                    self.dadosUBS.tabelaSeries.setItem(linha, 8, QTableWidgetItem(str(lista[linha][8])))
                else:
                    self.dadosUBS.tabelaSeries.setItem(linha, 8, QTableWidgetItem(str("")))

                if (lista[linha][9]) is not None:
                    self.dadosUBS.tabelaSeries.setItem(linha, 9, QTableWidgetItem(str("{:,.2f}".format(lista[linha][9]).replace(",", "X").replace(".", ",").replace("X", "."))))
                else:
                    self.dadosUBS.tabelaSeries.setItem(linha, 9, QTableWidgetItem(str("0,00")))

                self.dadosUBS.tabelaSeries.setItem(linha, 10, QTableWidgetItem(str(lista[linha][10])))
                self.dadosUBS.tabelaSeries.setItem(linha, 11, QTableWidgetItem(str(lista[linha][10])))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - preencher_tabela_series", 0)

    def funcao_desabilitar_edicao_status(self):
        try:
            self.dadosUBS.comboBox_status.setEnabled(False)
            self.dadosUBS.te_motivo_status.setReadOnly(True)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_status", 0)

    def funcao_habilitar_edicao_status(self):
        try:
            if self.ativarBusca:
                self.ativarEdicaoStatus = True
                ctypes.windll.user32.MessageBoxW(0, "Edição habilitada para Status",
                                                 "Atenção", 0)
                self.dadosUBS.comboBox_status.setEnabled(True)
                self.dadosUBS.te_motivo_status.setReadOnly(False)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_habilitar_edicao_status", 0)

    def funcao_desabilitar_edicao_ubs(self):
        try:
            print("desabilitar")
            self.dadosUBS.cb_ativo.setEnabled(False)
            self.dadosUBS.nome_emissor.setReadOnly(True)
            self.dadosUBS.cnpj_emissor.setReadOnly(True)
            self.dadosUBS.coordenador_lider.setReadOnly(True)
            self.dadosUBS.demais_coordenadores.setReadOnly(True)

            self.dadosUBS.simLei.setEnabled(False)
            self.dadosUBS.simConversiveisAcao.setEnabled(False)
            self.dadosUBS.simLoteAdicional.setEnabled(False)
            self.dadosUBS.simHaveraEsforcos.setEnabled(False)
            self.dadosUBS.simTeraGarantia.setEnabled(False)
            self.dadosUBS.simPermiteResgate.setEnabled(False)
            self.dadosUBS.simMarketMac.setEnabled(False)
            self.dadosUBS.simBalancoAuditado.setEnabled(False)
            self.dadosUBS.simBalancoDivulgado.setEnabled(False)
            self.dadosUBS.simRFP.setEnabled(False)
            self.dadosUBS.simESG.setEnabled(False)

            self.dadosUBS.naoLei.setEnabled(False)
            self.dadosUBS.naoConversiveisAcao.setEnabled(False)
            self.dadosUBS.naoLoteAdicional.setEnabled(False)
            self.dadosUBS.naoHaveraEsforcos.setEnabled(False)
            self.dadosUBS.naoTeraGarantia.setEnabled(False)
            self.dadosUBS.naoPermiteResgate.setEnabled(False)
            self.dadosUBS.naoMarketMac.setEnabled(False)
            self.dadosUBS.naoBalancoAuditado.setEnabled(False)
            self.dadosUBS.naoBalancoDivulgado.setEnabled(False)
            self.dadosUBS.naoRFP.setEnabled(False)
            self.dadosUBS.naoESG.setEnabled(False)

            self.dadosUBS.cb_nomeCoordenador.setEnabled(False)
            self.dadosUBS.cb_cnpjCoordenador.setEnabled(False)
            self.dadosUBS.cb_legislacaoCVM.setEnabled(False)
            self.dadosUBS.cb_ritoRegistro.setEnabled(False)
            self.dadosUBS.cb_documentoOferta.setEnabled(False)
            self.dadosUBS.cb_regimeColocacao.setEnabled(False)
            self.dadosUBS.cb_ratingEmissora.setEnabled(False)
            self.dadosUBS.cb_ratingOferta.setEnabled(False)
            self.dadosUBS.cb_probabilidadeColocacao.setEnabled(False)
            self.dadosUBS.cb_tipoEmissor.setEnabled(False)
            self.dadosUBS.cb_fee_forma_calculo.setEnabled(False)

            self.dadosUBS.le_valorEmissao.setReadOnly(True)
            self.dadosUBS.te_destinacaoRecursos.setReadOnly(True)
            self.dadosUBS.le_partGarantiaFirme.setReadOnly(True)
            self.dadosUBS.le_loteAdicionalMax.setReadOnly(True)
            self.dadosUBS.le_premioResgAntBFF.setReadOnly(True)
            self.dadosUBS.te_garantia.setReadOnly(True)
            self.dadosUBS.le_feeTotal.setReadOnly(True)
            self.dadosUBS.le_feeCanal.setReadOnly(True)
            self.dadosUBS.le_outrasFees.setReadOnly(True)
            self.dadosUBS.spinBox_series.setReadOnly(True)
            self.dadosUBS.de_previsaoLiquidacao.setReadOnly(True)
            self.dadosUBS.de_dtLimiteEnvioProp.setReadOnly(True)
            self.dadosUBS.le_empresaAudit.setReadOnly(True)
            self.dadosUBS.te_justificativa.setReadOnly(True)
            self.dadosUBS.te_covenants.setReadOnly(True)
            self.dadosUBS.te_observacoes.setReadOnly(True)

            #Lastros
            self.dadosUBS.cb_lastro.setEnabled(False)
            self.dadosUBS.simResolvencia.setEnabled(False)
            self.dadosUBS.naoResolvencia.setEnabled(False)
            self.dadosUBS.simSubordinacao.setEnabled(False)
            self.dadosUBS.naoSubordinacao.setEnabled(False)
            self.dadosUBS.simSeguro.setEnabled(False)
            self.dadosUBS.naoSeguro.setEnabled(False)

            self.dadosUBS.le_lastroVolMedio.setReadOnly(True)
            self.dadosUBS.le_lastroTicketMedio.setReadOnly(True)
            self.dadosUBS.le_lastroVolTotalCarteira.setReadOnly(True)
            self.dadosUBS.le_lastroVolDispCessao.setReadOnly(True)
            self.dadosUBS.le_lastroInadMedia.setReadOnly(True)
            self.dadosUBS.te_lastroConcCarteira.setReadOnly(True)
            self.dadosUBS.te_lastroIndiceMedioPagAtraso.setReadOnly(True)
            self.dadosUBS.te_lastro10MaioresDeve.setReadOnly(True)
            self.dadosUBS.te_lastroPrazoMedioPagAtraso.setReadOnly(True)
            self.dadosUBS.te_astroPrazoMedioCarteira.setReadOnly(True)
            self.dadosUBS.te_IndiceMedioDistratoDevol.setReadOnly(True)

            #SERIES
            self.dadosUBS.cb_tipo.setEnabled(False)
            self.dadosUBS.cb_pagamento_principal.setEnabled(False)
            self.dadosUBS.cb_pagamento_juros.setEnabled(False)
            self.dadosUBS.cb_indexador.setEnabled(False)
            self.dadosUBS.cb_publicoAlvoMercadoPrimario.setEnabled(False)
            self.dadosUBS.cb_publicoAlvoMercadoSecundario.setEnabled(False)

            self.dadosUBS.le_prazo_total.setReadOnly(True)
            self.dadosUBS.le_carencia_principal.setReadOnly(True)
            self.dadosUBS.le_carencia_juros.setReadOnly(True)
            self.dadosUBS.le_inicio_pagamento_principal.setReadOnly(True)
            self.dadosUBS.le_informar_referencia.setReadOnly(True)
            self.dadosUBS.le_taxa.setReadOnly(True)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_ubs", 0)

    def funcao_habilitar_edicao_ubs(self):
        try:
            if self.ativarBusca:
                self.ativarEdicaoUBS = True
                ctypes.windll.user32.MessageBoxW(0, "Edição habilitada",
                                                 "Atenção", 0)
                self.tipo_ativo()
                print("habilitar")
                self.dadosUBS.cb_ativo.setEnabled(True)
                self.dadosUBS.nome_emissor.setReadOnly(False)
                self.dadosUBS.cnpj_emissor.setReadOnly(False)
                self.dadosUBS.coordenador_lider.setReadOnly(False)
                self.dadosUBS.demais_coordenadores.setReadOnly(False)

                self.dadosUBS.simLei.setEnabled(True)
                self.dadosUBS.simConversiveisAcao.setEnabled(True)
                self.dadosUBS.simLoteAdicional.setEnabled(True)
                self.dadosUBS.simHaveraEsforcos.setEnabled(True)
                self.dadosUBS.simTeraGarantia.setEnabled(True)
                self.dadosUBS.simPermiteResgate.setEnabled(True)
                self.dadosUBS.simMarketMac.setEnabled(True)
                self.dadosUBS.simBalancoAuditado.setEnabled(True)
                self.dadosUBS.simBalancoDivulgado.setEnabled(True)
                self.dadosUBS.simRFP.setEnabled(True)
                self.dadosUBS.simESG.setEnabled(True)

                self.dadosUBS.naoLei.setEnabled(True)
                self.dadosUBS.naoConversiveisAcao.setEnabled(True)
                self.dadosUBS.naoLoteAdicional.setEnabled(True)
                self.dadosUBS.naoHaveraEsforcos.setEnabled(True)
                self.dadosUBS.naoTeraGarantia.setEnabled(True)
                self.dadosUBS.naoPermiteResgate.setEnabled(True)
                self.dadosUBS.naoMarketMac.setEnabled(True)
                self.dadosUBS.naoBalancoAuditado.setEnabled(True)
                self.dadosUBS.naoBalancoDivulgado.setEnabled(True)
                self.dadosUBS.naoRFP.setEnabled(True)
                self.dadosUBS.naoESG.setEnabled(True)

                self.dadosUBS.cb_nomeCoordenador.setEnabled(True)
                self.dadosUBS.cb_cnpjCoordenador.setEnabled(True)
                self.dadosUBS.cb_legislacaoCVM.setEnabled(True)
                self.dadosUBS.cb_ritoRegistro.setEnabled(True)
                self.dadosUBS.cb_documentoOferta.setEnabled(True)
                self.dadosUBS.cb_regimeColocacao.setEnabled(True)
                self.dadosUBS.cb_ratingEmissora.setEnabled(True)
                self.dadosUBS.cb_ratingOferta.setEnabled(True)
                self.dadosUBS.cb_probabilidadeColocacao.setEnabled(True)
                self.dadosUBS.cb_tipoEmissor.setEnabled(True)
                self.dadosUBS.cb_fee_forma_calculo.setEnabled(True)

                self.dadosUBS.le_valorEmissao.setReadOnly(False)
                self.dadosUBS.te_destinacaoRecursos.setReadOnly(False)
                self.dadosUBS.le_partGarantiaFirme.setReadOnly(False)
                self.dadosUBS.le_loteAdicionalMax.setReadOnly(False)
                self.dadosUBS.le_premioResgAntBFF.setReadOnly(False)
                self.dadosUBS.te_garantia.setReadOnly(False)
                self.dadosUBS.le_feeTotal.setReadOnly(False)
                self.dadosUBS.le_feeCanal.setReadOnly(False)
                self.dadosUBS.le_outrasFees.setReadOnly(False)
                self.dadosUBS.spinBox_series.setReadOnly(False)
                self.dadosUBS.de_previsaoLiquidacao.setReadOnly(False)
                self.dadosUBS.de_dtLimiteEnvioProp.setReadOnly(False)
                self.dadosUBS.le_empresaAudit.setReadOnly(False)
                self.dadosUBS.te_justificativa.setReadOnly(False)
                self.dadosUBS.te_covenants.setReadOnly(False)
                self.dadosUBS.te_observacoes.setReadOnly(False)

                #Lastros
                if (self.dadosUBS.cb_ativo.currentText() in ['CRI', 'CRA', 'FIDC', 'Debêntures Securitizadas'] and
                        self.dadosUBS.cb_lastro.currentText() == 'Direitos Creditórios'):
                    self.dadosUBS.simResolvencia.setEnabled(True)
                    self.dadosUBS.naoResolvencia.setEnabled(True)
                    self.dadosUBS.simSubordinacao.setEnabled(True)
                    self.dadosUBS.naoSubordinacao.setEnabled(True)
                    self.dadosUBS.simSeguro.setEnabled(True)
                    self.dadosUBS.naoSeguro.setEnabled(True)

                    self.dadosUBS.le_lastroVolMedio.setReadOnly(False)
                    self.dadosUBS.le_lastroTicketMedio.setReadOnly(False)
                    self.dadosUBS.le_lastroVolTotalCarteira.setReadOnly(False)
                    self.dadosUBS.le_lastroVolDispCessao.setReadOnly(False)
                    self.dadosUBS.le_lastroInadMedia.setReadOnly(False)
                    self.dadosUBS.te_lastroConcCarteira.setReadOnly(False)
                    self.dadosUBS.te_lastroIndiceMedioPagAtraso.setReadOnly(False)
                    self.dadosUBS.te_lastro10MaioresDeve.setReadOnly(False)
                    self.dadosUBS.te_lastroPrazoMedioPagAtraso.setReadOnly(False)
                    self.dadosUBS.te_astroPrazoMedioCarteira.setReadOnly(False)
                    self.dadosUBS.te_IndiceMedioDistratoDevol.setReadOnly(False)

                #SERIES
                self.dadosUBS.cb_tipo.setEnabled(True)
                self.dadosUBS.cb_pagamento_principal.setEnabled(True)
                self.dadosUBS.cb_pagamento_juros.setEnabled(True)
                self.dadosUBS.cb_indexador.setEnabled(True)
                self.dadosUBS.cb_publicoAlvoMercadoPrimario.setEnabled(True)
                self.dadosUBS.cb_publicoAlvoMercadoSecundario.setEnabled(True)

                self.dadosUBS.le_prazo_total.setReadOnly(False)
                self.dadosUBS.le_carencia_principal.setReadOnly(False)
                self.dadosUBS.le_carencia_juros.setReadOnly(False)
                self.dadosUBS.le_inicio_pagamento_principal.setReadOnly(False)
                self.dadosUBS.le_informar_referencia.setReadOnly(False)
                self.dadosUBS.le_taxa.setReadOnly(False)

            else:
                ctypes.windll.user32.MessageBoxW(0, "Consultar um ID antes de prosseguir",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_habilitar_edicao_ubs", 0)

    def funcao_desabilitar_edicao_estudo(self):
        try:
            print("desabilitar")
            self.dadosUBS.cb_assessorBBBI.setEnabled(False)
            self.dadosUBS.cb_estrategia_distribuicao.setEnabled(False)

            self.dadosUBS.simTVM.setEnabled(False)
            self.dadosUBS.naoTVM.setEnabled(False)

            self.dadosUBS.simUPB.setEnabled(False)
            self.dadosUBS.naoUPB.setEnabled(False)

            self.dadosUBS.le_prazo_venda_upb.setReadOnly(True)
            self.dadosUBS.le_impactoxprobabilidade.setReadOnly(True)
            self.dadosUBS.le_limite_global_rc.setReadOnly(True)
            self.dadosUBS.le_limite_especifico_rc.setReadOnly(True)
            self.dadosUBS.de_consulta_viab_tvm.setReadOnly(True)
            self.dadosUBS.de_consulta_upb.setReadOnly(True)
            self.dadosUBS.de_proposta_negocios.setReadOnly(True)
            self.dadosUBS.te_retorno_consulta_viabilidade_tvm.setReadOnly(True)
            self.dadosUBS.te_retorno_consulta_upb.setReadOnly(True)
            self.dadosUBS.te_resultado_proposta_negocios.setReadOnly(True)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_estudo", 0)

    def funcao_habilitar_edicao_estudo(self):
        try:
            print("habilitar")
            if self.ativarBusca:
                self.ativarEdicaoEstudo = True
                ctypes.windll.user32.MessageBoxW(0, "Edição habilitada para fase Estudo",
                                                 "Atenção", 0)

                self.dadosUBS.cb_assessorBBBI.setEnabled(True)
                self.dadosUBS.cb_estrategia_distribuicao.setEnabled(True)

                self.dadosUBS.simTVM.setEnabled(True)
                self.dadosUBS.naoTVM.setEnabled(True)

                self.dadosUBS.simUPB.setEnabled(True)
                self.dadosUBS.naoUPB.setEnabled(True)

                self.dadosUBS.le_prazo_venda_upb.setReadOnly(False)
                #self.dadosUBS.le_impactoxprobabilidade.setReadOnly(False)
                self.dadosUBS.le_limite_global_rc.setReadOnly(False)
                self.dadosUBS.le_limite_especifico_rc.setReadOnly(False)
                self.dadosUBS.de_consulta_viab_tvm.setReadOnly(False)
                self.dadosUBS.de_consulta_upb.setReadOnly(False)
                self.dadosUBS.de_proposta_negocios.setReadOnly(False)
                self.dadosUBS.te_retorno_consulta_viabilidade_tvm.setReadOnly(False)
                self.dadosUBS.te_retorno_consulta_upb.setReadOnly(False)
                self.dadosUBS.te_resultado_proposta_negocios.setReadOnly(False)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Consultar um ID antes de prosseguir",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_habilitar_edicao_estudo", 0)

    def funcao_desabilitar_edicao_aprovacao(self):
        try:
            print("desabilitar")
            self.dadosUBS.le_numero_estudo_tecnico.setReadOnly(True)
            self.dadosUBS.de_aprovacao_estudo_tecnico.setReadOnly(True)
            self.dadosUBS.le_valor_gf_estudo_tecnico.setReadOnly(True)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_aprovacao", 0)

    def funcao_habilitar_edicao_aprovacao(self):
        try:
            print("desabilitar")
            if self.ativarBusca:
                self.ativarEdicaoAprovacao = True
                ctypes.windll.user32.MessageBoxW(0, "Edição habilitada para fase Aprovação",
                                                 "Atenção", 0)
                self.dadosUBS.le_numero_estudo_tecnico.setReadOnly(False)
                self.dadosUBS.de_aprovacao_estudo_tecnico.setReadOnly(False)
                self.dadosUBS.le_valor_gf_estudo_tecnico.setReadOnly(False)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Consultar um ID antes de prosseguir",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_habilitar_edicao_aprovacao", 0)

    def funcao_desabilitar_edicao_estruturacao(self):
        try:
            print("desabilitar")
            self.dadosUBS.le_nomeSecuritizadoraAdm.setReadOnly(True)
            self.dadosUBS.le_cnpjSecuritizadoraAdm.setReadOnly(True)
            self.dadosUBS.le_nomeAgendeFiduciario.setReadOnly(True)
            self.dadosUBS.le_cnpjAgendeFiduciario.setReadOnly(True)

            self.dadosUBS.cb_especie.setEnabled(False)
            self.dadosUBS.cb_indexador_operacao.setEnabled(False)
            self.dadosUBS.cb_percentual_spreead_operacao.setEnabled(False)

            self.dadosUBS.le_numero_emissao.setReadOnly(True)
            self.dadosUBS.le_classe.setReadOnly(True)
            self.dadosUBS.le_series_estruturacao.setReadOnly(True)
            #self.dadosUBS.le_taxa_operacao.setReadOnly(True)
            #self.dadosUBS.le_pu_emissao.setReadOnly(True)
            self.dadosUBS.le_fee_estrturacao.setReadOnly(True)
            self.dadosUBS.le_fee_sucesso.setReadOnly(True)
            self.dadosUBS.le_fee_garantia_firme.setReadOnly(True)
            self.dadosUBS.le_outras_fees.setReadOnly(True)
            self.dadosUBS.le_fee_distribuicao_canal.setReadOnly(True)

            # self.dadosUBS.de_data_emissao.setReadOnly(True)
            # self.dadosUBS.de_data_vencimento_emissao.setReadOnly(True)
            # self.dadosUBS.de_data_inicial_juros.setReadOnly(True)
            # self.dadosUBS.de_data_final_juros.setReadOnly(True)
            # self.dadosUBS.de_data_inicial_amortizacao.setReadOnly(True)
            # self.dadosUBS.de_data_final_amortizacao.setReadOnly(True)
            self.dadosUBS.de_data_bookbuilding.setReadOnly(True)
            self.dadosUBS.de_data_liquidacao.setReadOnly(True)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_estruturacao", 0)

    def funcao_habilitar_edicao_estruturacao(self):
        try:
            print("habilitar")
            if self.ativarBusca:
                self.ativarEdicaoEstruturacao = True
                ctypes.windll.user32.MessageBoxW(0, "Edição habilitada para fase Estruturação",
                                                 "Atenção", 0)

                self.dadosUBS.le_nomeSecuritizadoraAdm.setReadOnly(False)
                self.dadosUBS.le_cnpjSecuritizadoraAdm.setReadOnly(False)
                self.dadosUBS.le_nomeAgendeFiduciario.setReadOnly(False)
                self.dadosUBS.le_cnpjAgendeFiduciario.setReadOnly(False)

                self.dadosUBS.cb_especie.setEnabled(True)
                self.dadosUBS.cb_indexador_operacao.setEnabled(True)
                self.dadosUBS.cb_percentual_spreead_operacao.setEnabled(True)

                self.dadosUBS.le_numero_emissao.setReadOnly(False)
                self.dadosUBS.le_classe.setReadOnly(False)
                self.dadosUBS.le_series_estruturacao.setReadOnly(False)
                #self.dadosUBS.le_taxa_operacao.setReadOnly(False)
                #self.dadosUBS.le_pu_emissao.setReadOnly(False)
                self.dadosUBS.le_fee_estrturacao.setReadOnly(False)
                self.dadosUBS.le_fee_sucesso.setReadOnly(False)
                self.dadosUBS.le_fee_garantia_firme.setReadOnly(False)
                self.dadosUBS.le_outras_fees.setReadOnly(False)
                self.dadosUBS.le_fee_distribuicao_canal.setReadOnly(False)

                # self.dadosUBS.de_data_emissao.setReadOnly(False)
                # self.dadosUBS.de_data_vencimento_emissao.setReadOnly(False)
                # self.dadosUBS.de_data_inicial_juros.setReadOnly(False)
                # self.dadosUBS.de_data_final_juros.setReadOnly(False)
                # self.dadosUBS.de_data_inicial_amortizacao.setReadOnly(False)
                # self.dadosUBS.de_data_final_amortizacao.setReadOnly(False)
                self.dadosUBS.de_data_bookbuilding.setReadOnly(False)
                self.dadosUBS.de_data_liquidacao.setReadOnly(False)

            else:
                ctypes.windll.user32.MessageBoxW(0, "Consultar um ID antes de prosseguir",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_habilitar_edicao_estruturacao", 0)

    def funcao_desabilitar_edicao_liquidacao(self):
        try:
            self.dadosUBS.le_codigo_ativo.setReadOnly(True)
            self.dadosUBS.le_insi.setReadOnly(True)
            self.dadosUBS.le_pu_liquidacao.setReadOnly(True)

            self.dadosUBS.simGFSE.setEnabled(False)
            self.dadosUBS.naoGFSE.setEnabled(False)

            self.dadosUBS.le_volume_adquirido.setReadOnly(True)
            self.dadosUBS.le_qtd_valores_mob_adquirido.setReadOnly(True)
            self.dadosUBS.le_porcent_sobras.setReadOnly(True)
            self.dadosUBS.le_prob_colocacao_realizada.setReadOnly(True)

            self.dadosUBS.le_demanda_upb_merc_primario.setReadOnly(True)
            self.dadosUBS.le_alocacao_upb_mercado_primario.setReadOnly(True)
            self.dadosUBS.le_fee_upb_mercado_primario.setReadOnly(True)
            self.dadosUBS.le_fee_retirada_dist_mercado_secundario.setReadOnly(True)
            self.dadosUBS.le_fee_recebida_BBBI.setReadOnly(True)
            self.dadosUBS.le_carteira_rm.setReadOnly(True)
            self.dadosUBS.le_grupo_rm.setReadOnly(True)
            self.dadosUBS.le_livro_rm.setReadOnly(True)
            self.dadosUBS.le_categoria_contabil.setReadOnly(True)
            self.dadosUBS.le_camara_registro.setReadOnly(True)
            self.dadosUBS.le_codigo_grupo.setReadOnly(True)
            self.dadosUBS.le_grupo.setReadOnly(True)
            self.dadosUBS.le_codigo_livro.setReadOnly(True)
            self.dadosUBS.le_livro.setReadOnly(True)
            self.dadosUBS.le_codigo_sub_livro.setReadOnly(True)
            self.dadosUBS.le_sub_livro.setReadOnly(True)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_liquidacao", 0)

    def funcao_habilitar_edicao_liquidacao(self):
        try:
            if self.ativarBusca:
                self.ativarEdicaoLiquidacao = True
                ctypes.windll.user32.MessageBoxW(0, "Edição habilitada para fase Liquidação",
                                                 "Atenção", 0)

                self.dadosUBS.le_codigo_ativo.setReadOnly(False)
                self.dadosUBS.le_insi.setReadOnly(False)
                self.dadosUBS.le_pu_liquidacao.setReadOnly(False)

                self.dadosUBS.simGFSE.setEnabled(True)
                self.dadosUBS.naoGFSE.setEnabled(True)

                self.dadosUBS.le_volume_adquirido.setReadOnly(False)
                self.dadosUBS.le_qtd_valores_mob_adquirido.setReadOnly(False)
                #self.dadosUBS.le_porcent_sobras.setReadOnly(False)
                #self.dadosUBS.le_prob_colocacao_realizada.setReadOnly(False)

                self.dadosUBS.le_demanda_upb_merc_primario.setReadOnly(False)
                self.dadosUBS.le_alocacao_upb_mercado_primario.setReadOnly(False)
                self.dadosUBS.le_fee_upb_mercado_primario.setReadOnly(False)
                self.dadosUBS.le_fee_retirada_dist_mercado_secundario.setReadOnly(False)
                self.dadosUBS.le_fee_recebida_BBBI.setReadOnly(False)
                self.dadosUBS.le_carteira_rm.setReadOnly(False)
                self.dadosUBS.le_grupo_rm.setReadOnly(False)
                self.dadosUBS.le_livro_rm.setReadOnly(False)
                self.dadosUBS.le_categoria_contabil.setReadOnly(False)
                self.dadosUBS.le_camara_registro.setReadOnly(False)
                self.dadosUBS.le_codigo_grupo.setReadOnly(False)
                self.dadosUBS.le_grupo.setReadOnly(False)
                self.dadosUBS.le_codigo_livro.setReadOnly(False)
                self.dadosUBS.le_livro.setReadOnly(False)
                self.dadosUBS.le_codigo_sub_livro.setReadOnly(False)
                self.dadosUBS.le_sub_livro.setReadOnly(False)
            else:
                ctypes.windll.user32.MessageBoxW(0, "Consultar um ID antes de prosseguir",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_desabilitar_edicao_liquidacao", 0)

    def funcao_salvar_ubs(self):
        try:
            print("salvar")
            if self.ativarEdicaoUBS:
                self.funcao_desabilitar_edicao_ubs()
                """Ao clicar em salvar, um novo versionamento deve ser impostado, independente de 
                    onde foi a alteração"""

                self.versionar_novos_dados_ubs()
                self.versionar_novos_dados_lastro()

                self.cnpj_antigo = int(self.dao.verificar_ultimo_cnpj_por_id(self.id))

                # Dados Gerais
                self.resultadogeral = self.dao.inserir_dados_gerais_versionamento(self.novos_dados)
                if self.resultadogeral == 1:
                    self.dadosUBS.versao.setText(str(self.novos_dados["versionamento"]))
                    self.verificar_alteracao_cnpj(self.cnpj_antigo)

                    ctypes.windll.user32.MessageBoxW(0, "Dados Gerais salvos com sucesso",
                                                    "Dados Gerais", 0)

                else:
                    ctypes.windll.user32.MessageBoxW(0, "Dados referente aos dados gerais da UBS não foram salvos \n"
                                                        "Verifique se as informações foram inseridas corretamente!",
                                                     "Atenção", 0)

                #Lastro
                if (self.dadosUBS.cb_ativo.currentText() in ['CRI', 'CRA', 'FIDC', 'Debêntures Securitizadas']
                        and self.dadosUBS.cb_lastro.currentText() == 'Direitos Creditórios'):
                    self.resultadolastro = self.dao.inserir_dados_lastro_versionamento(self.novos_dados_lastro)
                    print(self.resultadolastro)
                    if self.resultadolastro == 1:
                        ctypes.windll.user32.MessageBoxW(0, "Dados referente ao Lastro salvos com sucesso",
                                                    "Lastro", 0)
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Dados referente ao Lastro não foram salvos \n"
                                                            "Verifique se as informações foram inseridas corretamente!",
                                                         "Atenção", 0)

                #Series
                for item in self.listaSeries:
                    self.resultadoseries = self.dao.inserir_dados_series_versionamento(item)
                    if self.resultadoseries == 1:
                        self.qtddoseries = self.qtddoseries + 1

                print(self.qtddoseries)

                if self.qtddoseries >= 1:
                    ctypes.windll.user32.MessageBoxW(0, f"Dados referente a Séries salvos com sucesso \n"
                                                        f"Foram inseridas {self.qtddoseries} séries",
                                                     "Séries", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Não foram inseridas novas séries",
                                                     "Séries", 0)

                self.dadosUBS.seriesFila.setText(str(0))
                self.insere_dados_series()
                self.ativarEdicaoUBS = False
                self.listaSeries = []
                self.qtddoseries = 0
                self.novos_dados = {}
                self.novos_dados_lastro = {}
                self.novos_dados_serie = {}

                self.campos_alterados_estudo()
                self.atualizacao_combo_box_id()

                self.dadosUBS.comboBox_ID.setCurrentText(str(self.id) + " - " + str(self.dadosUBS.nome_emissor.text()))

            else:
                ctypes.windll.user32.MessageBoxW(0, "Só é possivel salvar caso haja alterações",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_salvar_ubs", 0)

    def funcao_salvar_status(self):
        try:
            if self.ativarEdicaoStatus:
                self.funcao_desabilitar_edicao_status()
                self.versionar_dados_status()
                print(self.novos_dados_status)
                resultadoStatus = self.dao.inserir_dados_status(self.novos_dados_status)
                if resultadoStatus == 1:
                    ctypes.windll.user32.MessageBoxW(0, "Dados Salvos com sucesso",
                                                 "Status", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Ocorreu algum erro ao inserir os dados \n"
                                                        "Verifique se os dados foram inseridos corretamente.",
                                                 "Atenção", 0)
                self.ativarEdicaoStatus = False
                self.novos_dados_status = {}

            else:
                ctypes.windll.user32.MessageBoxW(0, "Só é possivel salvar caso haja alterações",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_salvar_estudo", 0)

    def funcao_salvar_estudo(self):
        try:
            if self.ativarEdicaoEstudo:
                self.funcao_desabilitar_edicao_estudo()
                self.versionar_dados_estudo()
                print(self.novos_dados_estudo)
                resultadoestudo = self.dao.inserir_dados_estudo(self.novos_dados_estudo)
                if resultadoestudo == 1:
                    ctypes.windll.user32.MessageBoxW(0, "Dados Salvos com sucesso",
                                                 "Estudo", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Ocorreu algum erro ao inserir os dados \n"
                                                        "Verifique se os dados foram inseridos corretamente.",
                                                 "Atenção", 0)
                self.ativarEdicaoEstudo = False
                self.novos_dados_estudo = {}

            else:
                ctypes.windll.user32.MessageBoxW(0, "Só é possivel salvar caso haja alterações",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_salvar_estudo", 0)

    def funcao_salvar_aprovacao(self):
        try:
            if self.ativarEdicaoAprovacao:
                self.funcao_desabilitar_edicao_aprovacao()
                self.versionar_dados_aprovacao()
                print(self.novos_dados_aprovacao)
                resultadoaprovacao = self.dao.inserir_dados_aprovacao(self.novos_dados_aprovacao)
                if resultadoaprovacao == 1:
                    ctypes.windll.user32.MessageBoxW(0, "Dados Salvos com sucesso",
                                                 "Aprovação", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Ocorreu algum erro ao inserir os dados \n"
                                                        "Verifique se os dados foram inseridos corretamente.",
                                                 "Atenção", 0)
                self.ativarEdicaoAprovacao = False
                self.novos_dados_aprovacao = {}

            else:
                ctypes.windll.user32.MessageBoxW(0, "Só é possivel salvar caso haja alterações",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_salvar_aprovacao", 0)

    def funcao_salvar_estruturacao(self):
        try:
            if self.ativarEdicaoEstruturacao:
                self.funcao_desabilitar_edicao_estruturacao()
                self.versionar_dados_estruturacao()
                print(self.novos_dados_estruturacao)
                resultadoestruturacao = self.dao.inserir_dados_estruturacao(self.novos_dados_estruturacao)
                if resultadoestruturacao == 1:
                    ctypes.windll.user32.MessageBoxW(0, "Dados Salvos com sucesso",
                                                 "Estruturação", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Ocorreu algum erro ao inserir os dados \n"
                                                        "Verifique se os dados foram inseridos corretamente.",
                                                 "Atenção", 0)
                self.ativarEdicaoEstruturacao = False
                self.novos_dados_estruturacao = {}

            else:
                ctypes.windll.user32.MessageBoxW(0, "Só é possivel salvar caso haja alterações",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_salvar_estruturacao", 0)

    def funcao_salvar_liquidacao(self):
        try:
            if self.ativarEdicaoLiquidacao:
                self.funcao_desabilitar_edicao_liquidacao()
                self.versionar_dados_liquidacao()
                print(self.novos_dados_liquidacao)
                resultadoLiquidacao = self.dao.inserir_dados_liquidacao(self.novos_dados_liquidacao)
                if resultadoLiquidacao == 1:
                    ctypes.windll.user32.MessageBoxW(0, "Dados Salvos com sucesso",
                                                 "Liquidação", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Ocorreu algum erro ao inserir os dados \n"
                                                        "Verifique se os dados foram inseridos corretamente.",
                                                 "Atenção", 0)
                self.ativarEdicaoLiquidacao = False
                self.novos_dados_liquidacao = {}

            else:
                ctypes.windll.user32.MessageBoxW(0, "Só é possivel salvar caso haja alterações",
                                                 "Atenção", 0)
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - funcao_salvar_liquidacao", 0)

    def versionar_novos_dados_ubs(self):
        try:
            """Capturar os dados para novo versionamento"""

            if self.dadosUBS.cb_ativo.currentText() == "Debêntures":
                self.novos_dados["tipo_ativo"] = 1
            elif self.dadosUBS.cb_ativo.currentText() == "Notas Comerciais":
                self.novos_dados["tipo_ativo"] = 2
            elif self.dadosUBS.cb_ativo.currentText() == "CRI":
                self.novos_dados["tipo_ativo"] = 3
            elif self.dadosUBS.cb_ativo.currentText() == "CRA":
                self.novos_dados["tipo_ativo"] = 4
            elif self.dadosUBS.cb_ativo.currentText() == "FIDC":
                self.novos_dados["tipo_ativo"] = 5
            elif self.dadosUBS.cb_ativo.currentText() == "Debêntures Securitizadas":
                self.novos_dados["tipo_ativo"] = 6

            self.novos_dados["id"] = self.id
            self.novos_dados["versionamento"] = int(self.dadosUBS.versao.text()) + 1

            if self.dadosUBS.simLei.isChecked():
                self.novos_dados["lei_12431"] = '1'
            elif self.dadosUBS.naoLei.isChecked():
                self.novos_dados["lei_12431"] = '0'

            if self.dadosUBS.simConversiveisAcao.isChecked():
                self.novos_dados["conv_acoes"] = '1'
            elif self.dadosUBS.naoConversiveisAcao.isChecked():
                self.novos_dados["conv_acoes"] = '0'

            if self.dadosUBS.simESG.isChecked():
                self.novos_dados["esg"] = '1'
            elif self.dadosUBS.naoESG.isChecked():
                self.novos_dados["esg"] = '0'

            self.novos_dados["nome_emissor"] = self.dadosUBS.nome_emissor.text()
            self.novos_dados["cnpj_emissor"] = (self.dadosUBS.cnpj_emissor.text()).replace('/','').replace('.', '').replace('-', '')

            if self.dadosUBS.cb_tipoEmissor.currentText() == "EGEM":
                self.novos_dados["tipo_emissor"] = 1
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "EFRF":
                self.novos_dados["tipo_emissor"] = 2
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "Emissor em fase pré-operacional":
                self.novos_dados["tipo_emissor"] = 3
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "SPAC":
                self.novos_dados["tipo_emissor"] = 4
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "SPE":
                self.novos_dados["tipo_emissor"] = 5
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "S.A. capital aberto":
                self.novos_dados["tipo_emissor"] = 6
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "S.A. capital fechado":
                self.novos_dados["tipo_emissor"] = 7
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "S.A. categoria B":
                self.novos_dados["tipo_emissor"] = 8
            elif self.dadosUBS.cb_tipoEmissor.currentText() == "LTDA.":
                self.novos_dados["tipo_emissor"] = 9

            if self.dadosUBS.cb_fee_forma_calculo.currentText() == "Flat":
                self.novos_dados["fee_canal_forma_cal"] = 1
            elif self.dadosUBS.cb_fee_forma_calculo.currentText() == "Ao ano":
                self.novos_dados["fee_canal_forma_cal"] = 2

            if self.dadosUBS.cb_nomeCoordenador.currentText() == "UBS BB":
                self.novos_dados["nome_coordenador"] = 1
            elif self.dadosUBS.cb_nomeCoordenador.currentText() == "BB-BI":
                self.novos_dados["nome_coordenador"] = 2

            if self.dadosUBS.cb_cnpjCoordenador.currentText() == "02.819.125/0001-73":
                self.novos_dados["cnpj_coordenador"] = 2819125000173
            elif self.dadosUBS.cb_cnpjCoordenador.currentText() == "24.933.830/0001-30":
                self.novos_dados["cnpj_coordenador"] = 24933830000130

            self.novos_dados["coordenador_lider"] = self.dadosUBS.coordenador_lider.text()
            self.novos_dados["demais_coordenadores"] = self.dadosUBS.demais_coordenadores.text()

            if self.dadosUBS.cb_legislacaoCVM.currentText() == "RCVM 160":
                self.novos_dados["legislacao_cvm"] = 1
            elif self.dadosUBS.cb_legislacaoCVM.currentText() == "RCVM 60":
                self.novos_dados["legislacao_cvm"] = 2
            elif self.dadosUBS.cb_legislacaoCVM.currentText() == "RCVMs 160 e 60":
                self.novos_dados["legislacao_cvm"] = 3

            if self.dadosUBS.cb_ritoRegistro.currentText() == "Automático":
                self.novos_dados["rito_registro"] = 1
            elif self.dadosUBS.cb_ritoRegistro.currentText() == "Ordinário":
                self.novos_dados["rito_registro"] = 2

            if self.dadosUBS.cb_documentoOferta.currentText() == "Formulário Eletrônico":
                self.novos_dados["documento_oferta"] = 1
            elif self.dadosUBS.cb_documentoOferta.currentText() == "Prospecto":
                self.novos_dados["documento_oferta"] = 2
            elif self.dadosUBS.cb_documentoOferta.currentText() == "Lâmina":
                self.novos_dados["documento_oferta"] = 3
            elif self.dadosUBS.cb_documentoOferta.currentText() == "Prospecto e Lâmina":
                self.novos_dados["documento_oferta"] = 4

            self.novos_dados["valor_emissao"] = self.dadosUBS.le_valorEmissao.text().replace('.', '').replace(',', '.')
            self.novos_dados["destinacao_recursos"] = self.dadosUBS.te_destinacaoRecursos.toPlainText()

            if self.dadosUBS.cb_regimeColocacao.currentText() == "Garantia Firme":
                self.novos_dados["regime_colocacao"] = 1
            elif self.dadosUBS.cb_regimeColocacao.currentText() == "Melhores Esforços":
                self.novos_dados["regime_colocacao"] = 2
            elif self.dadosUBS.cb_regimeColocacao.currentText() == "Garantia Firme e Melhores Esforços":
                self.novos_dados["regime_colocacao"] = 3

            self.novos_dados["part_regime_garantia_firme"] = self.dadosUBS.le_partGarantiaFirme.text().replace('.', '').replace(',', '.')

            if self.dadosUBS.simLoteAdicional.isChecked():
                self.novos_dados["lote_adicional"] = '1'
            elif self.dadosUBS.naoLoteAdicional.isChecked():
                self.novos_dados["lote_adicional"] = '0'

            self.novos_dados["lote_ad_maximo"] = self.dadosUBS.le_loteAdicionalMax.text().replace('.', '').replace(',', '.')

            self.novos_dados["series"] = self.dadosUBS.spinBox_series.value()

            if self.dadosUBS.cb_ratingEmissora.currentText() == "Aaa/AAA/AAA":
                self.novos_dados["rating_emissora"] = 1
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "Aa1/AA+/AA+":
                self.novos_dados["rating_emissora"] = 2
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "Aa2/AA/AA":
                self.novos_dados["rating_emissora"] = 3
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "Aa3/AA-/AA-":
                self.novos_dados["rating_emissora"] = 4
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "A1/A+/A+":
                self.novos_dados["rating_emissora"] = 5
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "A2/A/A":
                self.novos_dados["rating_emissora"] = 6
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "A3/A-/A-":
                self.novos_dados["rating_emissora"] = 7
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "Baa1/BBB+/BBB+":
                self.novos_dados["rating_emissora"] = 8
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "Baa2/BBB/BBB":
                self.novos_dados["rating_emissora"] = 9
            elif self.dadosUBS.cb_ratingEmissora.currentText() == "Baa3/BBB-/BBB-":
                self.novos_dados["rating_emissora"] = 10
            elif self.dadosUBS.cb_ratingEmissora.currentText() in ["Não se aplica", "Não possui"]:
                self.novos_dados["rating_emissora"] = 0
            elif self.dadosUBS.cb_ratingEmissora.currentText() in ["Não haverá"]:
                self.novos_dados["rating_emissora"] = 11

            if self.dadosUBS.cb_ratingOferta.currentText() == "Aaa/AAA/AAA":
                self.novos_dados["rating_min_oferta"] = 1
            elif self.dadosUBS.cb_ratingOferta.currentText() == "Aa1/AA+/AA+":
                self.novos_dados["rating_min_oferta"] = 2
            elif self.dadosUBS.cb_ratingOferta.currentText() == "Aa2/AA/AA":
                self.novos_dados["rating_min_oferta"] = 3
            elif self.dadosUBS.cb_ratingOferta.currentText() == "Aa3/AA-/AA-":
                self.novos_dados["rating_min_oferta"] = 4
            elif self.dadosUBS.cb_ratingOferta.currentText() == "A1/A+/A+":
                self.novos_dados["rating_min_oferta"] = 5
            elif self.dadosUBS.cb_ratingOferta.currentText() == "A2/A/A":
                self.novos_dados["rating_min_oferta"] = 6
            elif self.dadosUBS.cb_ratingOferta.currentText() == "A3/A-/A-":
                self.novos_dados["rating_min_oferta"] = 7
            elif self.dadosUBS.cb_ratingOferta.currentText() == "Baa1/BBB+/BBB+":
                self.novos_dados["rating_min_oferta"] = 8
            elif self.dadosUBS.cb_ratingOferta.currentText() == "Baa2/BBB/BBB":
                self.novos_dados["rating_min_oferta"] = 9
            elif self.dadosUBS.cb_ratingOferta.currentText() == "Baa3/BBB-/BBB-":
                self.novos_dados["rating_min_oferta"] = 10
            elif self.dadosUBS.cb_ratingOferta.currentText() in ["Não se aplica", "Não possui"]:
                self.novos_dados["rating_min_oferta"] = 0
            elif self.dadosUBS.cb_ratingOferta.currentText() in ["Não haverá"]:
                self.novos_dados["rating_min_oferta"] = 11

            if self.dadosUBS.cb_probabilidadeColocacao.currentText() == "Muito Baixa":
                self.novos_dados["prob_colocacao"] = 1
            elif self.dadosUBS.cb_probabilidadeColocacao.currentText() == "Baixa":
                self.novos_dados["prob_colocacao"] = 2
            elif self.dadosUBS.cb_probabilidadeColocacao.currentText() == "Média":
                self.novos_dados["prob_colocacao"] = 3
            elif self.dadosUBS.cb_probabilidadeColocacao.currentText() == "Alta":
                self.novos_dados["prob_colocacao"] = 4
            elif self.dadosUBS.cb_probabilidadeColocacao.currentText() == "Muito Alta":
                self.novos_dados["prob_colocacao"] = 5

            self.novos_dados["justificativa"] = self.dadosUBS.te_justificativa.toPlainText()

            if self.dadosUBS.simHaveraEsforcos.isChecked():
                self.novos_dados["esforcos_distrib"] = '1'
            elif self.dadosUBS.naoHaveraEsforcos.isChecked():
                self.novos_dados["esforcos_distrib"] = '0'

            if self.dadosUBS.simTeraGarantia.isChecked():
                self.novos_dados["ha_garantia"] = '1'
            elif self.dadosUBS.naoTeraGarantia.isChecked():
                self.novos_dados["ha_garantia"] = '0'

            self.novos_dados["garantia"] = self.dadosUBS.te_garantia.toPlainText()
            self.novos_dados["covenants"] = self.dadosUBS.te_covenants.toPlainText()

            if self.dadosUBS.simPermiteResgate.isChecked():
                self.novos_dados["permite_resgate_antecip"] = '1'
            elif self.dadosUBS.naoPermiteResgate.isChecked():
                self.novos_dados["permite_resgate_antecip"] = '0'

            if self.dadosUBS.simMarketMac.isChecked():
                self.novos_dados["market_flex_mac_clause"] = '1'
            elif self.dadosUBS.naoMarketMac.isChecked():
                self.novos_dados["market_flex_mac_clause"] = '0'

            self.novos_dados["premio_resgate_antecip"] = self.dadosUBS.le_premioResgAntBFF.text().replace('.', '').replace(',', '.')

            self.novos_dados["fees_total"] = self.dadosUBS.le_feeTotal.text().replace('.', '').replace(',', '.')
            self.novos_dados["fees_canal"] = self.dadosUBS.le_feeCanal.text().replace('.', '').replace(',', '.')
            self.novos_dados["outras_fees"] = self.dadosUBS.le_outrasFees.text()

            if self.dadosUBS.cb_fee_forma_calculo.currentText() == "Flat":
                self.novos_dados["fee_canal_forma_cal"] = 1
            elif self.dadosUBS.cb_fee_forma_calculo.currentText() == "Ao ano":
                self.novos_dados["fee_canal_forma_cal"] = 2

            if self.dadosUBS.simBalancoAuditado.isChecked():
                self.novos_dados["balanco_auditado"] = '1'
            elif self.dadosUBS.naoBalancoAuditado.isChecked():
                self.novos_dados["balanco_auditado"] = '0'

            self.novos_dados["empresa_auditoria"] = self.dadosUBS.le_empresaAudit.text()

            if self.dadosUBS.simBalancoDivulgado.isChecked():
                self.novos_dados["balanco_divulgado"] = '1'
            elif self.dadosUBS.naoBalancoDivulgado.isChecked():
                self.novos_dados["balanco_divulgado"] = '0'

            if self.dadosUBS.simRFP.isChecked():
                self.novos_dados["rfp"] = '1'
            elif self.dadosUBS.naoRFP.isChecked():
                self.novos_dados["rfp"] = '0'

            self.novos_dados["previsao_liquidacao"] = datetime.strptime(self.dadosUBS.de_previsaoLiquidacao.text(), '%d/%m/%Y').date()
            self.novos_dados["data_limite_prop"] = datetime.strptime(self.dadosUBS.de_dtLimiteEnvioProp.text(), '%d/%m/%Y').date()
            self.novos_dados["observacoes"] = self.dadosUBS.te_observacoes.toPlainText()

            print(self.novos_dados)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_novos_dados_ubs", 0)

    def versionar_novos_dados_lastro(self):
        try:
            print("inserir novos dados lastro")

            self.novos_dados_lastro["id"] = self.id
            self.novos_dados_lastro["versionamento"] = int(self.dadosUBS.versao.text()) + 1

            if self.dadosUBS.cb_lastro.currentText() == 'Direitos Creditórios':
                self.novos_dados_lastro["lastro"] = 1
            elif self.dadosUBS.cb_lastro.currentText() == 'Título de Dívida':
                self.novos_dados_lastro["lastro"] = 2

            if self.dadosUBS.simResolvencia.isChecked():
                self.novos_dados_lastro["resolvencia"] = '1'
            elif self.dadosUBS.naoResolvencia.isChecked():
                self.novos_dados_lastro["resolvencia"] = '0'

            if self.dadosUBS.simSubordinacao.isChecked():
                self.novos_dados_lastro["subordinacao"] = '1'
            elif self.dadosUBS.naoSubordinacao.isChecked():
                self.novos_dados_lastro["subordinacao"] = '0'

            if self.dadosUBS.simSeguro.isChecked():
                self.novos_dados_lastro["seguro"] = '1'
            elif self.dadosUBS.naoSeguro.isChecked():
                self.novos_dados_lastro["seguro"] = '0'

            self.novos_dados_lastro["lastro_vol_medio"] = self.dadosUBS.le_lastroVolMedio.text().replace('.', '').replace(',', '.')
            self.novos_dados_lastro["lastro_tic_medio"] = self.dadosUBS.le_lastroTicketMedio.text().replace('.', '').replace(',', '.')
            self.novos_dados_lastro["lastro_vol_total_carteira"] = self.dadosUBS.le_lastroVolTotalCarteira.text().replace('.', '').replace(',', '.')
            self.novos_dados_lastro["lastro_vol_disp_cessao"] = self.dadosUBS.le_lastroVolDispCessao.text().replace('.', '').replace(',', '.')
            self.novos_dados_lastro["lastro_inad_media"] = self.dadosUBS.le_lastroVolDispCessao.text().replace('.', '').replace(',', '.')

            self.novos_dados_lastro["lastro_conc_carteira"] = self.dadosUBS.te_lastroConcCarteira.toPlainText()
            self.novos_dados_lastro["lastro_10_maiores_dev"] = self.dadosUBS.te_lastro10MaioresDeve.toPlainText()
            self.novos_dados_lastro["lastro_prz_medio_carteira"] = self.dadosUBS.te_astroPrazoMedioCarteira.toPlainText()
            self.novos_dados_lastro["lastro_idc_media_pag_atraso"] = self.dadosUBS.te_lastroIndiceMedioPagAtraso.toPlainText()
            self.novos_dados_lastro["lastro_prz_medio_pag_atraso"] = self.dadosUBS.te_lastroPrazoMedioPagAtraso.toPlainText()
            self.novos_dados_lastro["lastro_idc_distrato_devol"] = self.dadosUBS.te_IndiceMedioDistratoDevol.toPlainText()
            print(self.novos_dados_lastro)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_novos_dados_lastro", 0)

    def incluir_nova_serie(self):
        try:
            if self.ativarEdicaoUBS:
                if (self.dadosUBS.le_prazo_total.text() != "" and self.dadosUBS.le_carencia_principal.text() != "" and
                    self.dadosUBS.le_carencia_juros.text() != "" and self.dadosUBS.le_inicio_pagamento_principal.text() !=
                        "" and self.dadosUBS.le_taxa.text() != ""):
                    print("Incluir nova série")
                    self.novos_dados_serie = {}
                    print(self.id)

                    self.novos_dados_serie["id"] = self.id
                    self.novos_dados_serie["versionamento"] = int(self.dadosUBS.versao.text()) + 1
                    self.novos_dados_serie["serie"] = self.serie + 1

                    if self.dadosUBS.cb_tipo.currentText() == "Debênture Convencional":
                        self.novos_dados_serie["tipo"] = 7
                    elif self.dadosUBS.cb_tipo.currentText() == "Debênture Infraestrutura":
                        self.novos_dados_serie["tipo"] = 8
                    elif self.dadosUBS.cb_tipo.currentText() == "Não se aplica":
                        self.novos_dados_serie["tipo"] = 9

                    self.novos_dados_serie["prazo"] = self.dadosUBS.le_prazo_total.text().replace('.', '').replace(',', '.')
                    self.novos_dados_serie["carencia"] = self.dadosUBS.le_carencia_principal.text().replace('.', '').replace(',', '.')

                    if self.dadosUBS.cb_pagamento_principal.currentText() == "Mensal":
                        self.novos_dados_serie["pag_principal"] = 1
                    elif self.dadosUBS.cb_pagamento_principal.currentText() == "Trimestral":
                        self.novos_dados_serie["pag_principal"] = 2
                    elif self.dadosUBS.cb_pagamento_principal.currentText() == "Semestral":
                        self.novos_dados_serie["pag_principal"] = 3
                    elif self.dadosUBS.cb_pagamento_principal.currentText() == "Anual":
                        self.novos_dados_serie["pag_principal"] = 4

                    self.novos_dados_serie["ini_pag_principal"] = self.dadosUBS.le_inicio_pagamento_principal.text().replace('.', '').replace(',', '.')

                    self.novos_dados_serie["carencia_juros"] = self.dadosUBS.le_carencia_juros.text().replace('.', '').replace(',', '.')

                    if self.dadosUBS.cb_pagamento_juros.currentText() == "Mensal":
                        self.novos_dados_serie["pag_juros"] = 1
                    elif self.dadosUBS.cb_pagamento_juros.currentText() == "Trimestral":
                        self.novos_dados_serie["pag_juros"] = 2
                    elif self.dadosUBS.cb_pagamento_juros.currentText() == "Semestral":
                        self.novos_dados_serie["pag_juros"] = 3
                    elif self.dadosUBS.cb_pagamento_juros.currentText() == "Anual":
                        self.novos_dados_serie["pag_juros"] = 4

                    if self.dadosUBS.cb_indexador.currentText() == "%CDI":
                        self.novos_dados_serie["indexador"] = 1
                    elif self.dadosUBS.cb_indexador.currentText() == "CDI+":
                        self.novos_dados_serie["indexador"] = 2
                    elif self.dadosUBS.cb_indexador.currentText() == "Dólar":
                        self.novos_dados_serie["indexador"] = 3
                    elif self.dadosUBS.cb_indexador.currentText() == "IPCA":
                        self.novos_dados_serie["indexador"] = 4
                    elif self.dadosUBS.cb_indexador.currentText() == "Prefixado":
                        self.novos_dados_serie["indexador"] = 5

                    self.novos_dados_serie["ref_ntnb"] = self.dadosUBS.le_informar_referencia.text()
                    self.novos_dados_serie["taxa"] = self.dadosUBS.le_taxa.text().replace('.', '').replace(',', '.')

                    if self.dadosUBS.cb_publicoAlvoMercadoPrimario.currentText() == "Profissional":
                        self.novos_dados_serie["pub_merc_primario"] = 1
                    elif self.dadosUBS.cb_publicoAlvoMercadoPrimario.currentText() == "Qualificado":
                        self.novos_dados_serie["pub_merc_primario"] = 2
                    elif self.dadosUBS.cb_publicoAlvoMercadoPrimario.currentText() == "Público Geral":
                        self.novos_dados_serie["pub_merc_primario"] = 3

                    if self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Profissional":
                        self.novos_dados_serie["pub_merc_secundario"] = 1
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Qualificado":
                        self.novos_dados_serie["pub_merc_secundario"] = 2
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Público Geral":
                        self.novos_dados_serie["pub_merc_secundario"] = 3
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Qualificado, somente mediante registro de emissor":
                        self.novos_dados_serie["pub_merc_secundario"] = 4
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Qualificado, após lock up de 3 meses":
                        self.novos_dados_serie["pub_merc_secundario"] = 5
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Qualificado, após lock up de 6 meses":
                        self.novos_dados_serie["pub_merc_secundario"] = 6
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Público Geral, somente mediante registro de emissor":
                        self.novos_dados_serie["pub_merc_secundario"] = 7
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Público Geral, após lock up de 6 meses":
                        self.novos_dados_serie["pub_merc_secundario"] = 8
                    elif self.dadosUBS.cb_publicoAlvoMercadoSecundario.currentText() == "Público Geral, após lock up de 1 ano":
                        self.novos_dados_serie["pub_merc_secundario"] = 9

                    self.serie = self.serie + 1
                    self.dadosUBS.seriesFila.setText(str(int(self.dadosUBS.seriesFila.text()) + 1))
                    self.listaSeries.append(self.novos_dados_serie)

                    ctypes.windll.user32.MessageBoxW(0, "Série inserida com sucesso", "Série", 0)

                    self.limparCamposSerie()

                    print(self.listaSeries)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Há dados vazio. Preencher antes de incluir", "Série", 0)

            else:
                ctypes.windll.user32.MessageBoxW(0, "Clique em 'Alterar' antes de incluir uma série", "Série", 0)

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - incluir_nova_serie", 0)

    def limparCamposSerie(self):
        try:
            self.dadosUBS.cb_tipo.setCurrentText(str(""))
            self.dadosUBS.cb_pagamento_principal.setCurrentText(str(""))
            self.dadosUBS.cb_pagamento_juros.setCurrentText(str(""))
            self.dadosUBS.cb_indexador.setCurrentText(str(""))
            self.dadosUBS.cb_publicoAlvoMercadoPrimario.setCurrentText(str(""))
            self.dadosUBS.cb_publicoAlvoMercadoSecundario.setCurrentText(str(""))

            self.dadosUBS.le_prazo_total.clear()
            self.dadosUBS.le_carencia_principal.clear()
            self.dadosUBS.le_carencia_juros.clear()
            self.dadosUBS.le_inicio_pagamento_principal.clear()
            self.dadosUBS.le_informar_referencia.clear()
            self.dadosUBS.le_taxa.clear()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - limparCamposSerie", 0)

    def versionar_dados_status(self):
        try:
            print("Caputurar dados inseridos pelo usuário")
            self.novos_dados_status["id"] = self.id
            self.novos_dados_status["versao"] = int(self.dadosUBS.versao.text())
            self.novos_dados_status["motivo"] = self.dadosUBS.te_motivo_status.toPlainText()

            if self.dadosUBS.comboBox_status.currentText() == "Em estudo":
                self.novos_dados_status["status"] = 1
            elif self.dadosUBS.comboBox_status.currentText() == "Pipeline":
                self.novos_dados_status["status"] = 2
            elif self.dadosUBS.comboBox_status.currentText() == "Mandatada":
                self.novos_dados_status["status"] = 3
            elif self.dadosUBS.comboBox_status.currentText() == "Mandatada e Aprovada":
                self.novos_dados_status["status"] = 4
            elif self.dadosUBS.comboBox_status.currentText() == "Cancelada":
                self.novos_dados_status["status"] = 5
            elif self.dadosUBS.comboBox_status.currentText() == "Perdida":
                self.novos_dados_status["status"] = 6
            elif self.dadosUBS.comboBox_status.currentText() == "Desistência cliente":
                self.novos_dados_status["status"] = 7
            elif self.dadosUBS.comboBox_status.currentText() == "Liquidada":
                self.novos_dados_status["status"] = 8

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_dados_status", 0)

    def versionar_dados_estudo(self):
        try:
            print("Caputurar dados inseridos pelo usuário")
            self.novos_dados_estudo["id"] = self.id
            self.novos_dados_estudo["versionamento"] = int(self.dadosUBS.versao.text())

            self.novos_dados_estudo["assessor_bbbi"] = self.dadosUBS.cb_assessorBBBI.currentText()
            self.novos_dados_estudo["estrategia_distribuicao"] = self.dadosUBS.cb_estrategia_distribuicao.currentText()

            if self.dadosUBS.simTVM.isChecked():
                self.novos_dados_estudo["consulta_viabilidade_tvm"] = '1'
            elif self.dadosUBS.naoTVM.isChecked():
                self.novos_dados_estudo["consulta_viabilidade_tvm"] = '0'

            if self.dadosUBS.simUPB.isChecked():
                self.novos_dados_estudo["consulta_upb"] = '1'
            elif self.dadosUBS.naoUPB.isChecked():
                self.novos_dados_estudo["consulta_upb"] = '0'

            self.novos_dados_estudo["pz_estmd_vnd_secun_upb"] = self.dadosUBS.le_prazo_venda_upb.text().replace('.', '').replace(',', '.')
            self.novos_dados_estudo["impacto_prob"] = self.dadosUBS.le_impactoxprobabilidade.text().replace('.', '').replace(',', '.')
            self.novos_dados_estudo["limite_global_rc"] = self.dadosUBS.le_limite_global_rc.text().replace('.', '').replace(',', '.')
            self.novos_dados_estudo["limite_especifico_rc"] = self.dadosUBS.le_limite_especifico_rc.text().replace('.', '').replace(',', '.')

            self.novos_dados_estudo["dt_consulta_viab_tvm"] = datetime.strptime(self.dadosUBS.de_consulta_viab_tvm.text(), '%d/%m/%Y').date()
            self.novos_dados_estudo["dt_consulta_upb"] = datetime.strptime(self.dadosUBS.de_consulta_upb.text(), '%d/%m/%Y').date()
            self.novos_dados_estudo["dt_proposta_negocios"] = datetime.strptime(self.dadosUBS.de_proposta_negocios.text(), '%d/%m/%Y').date()

            self.novos_dados_estudo["te_retorno_consulta_viabilidade_tvm"] = self.dadosUBS.te_retorno_consulta_viabilidade_tvm.toPlainText()
            self.novos_dados_estudo["te_retorno_consulta_upb"] = self.dadosUBS.te_retorno_consulta_upb.toPlainText()
            self.novos_dados_estudo["te_resultado_proposta_negocios"] = self.dadosUBS.te_resultado_proposta_negocios.toPlainText()

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_dados_estudo", 0)

    def versionar_dados_aprovacao(self):
        try:
            print("Caputurar dados inseridos pelo usuário")
            self.novos_dados_aprovacao["id"] = self.id
            self.novos_dados_aprovacao["versionamento"] = int(self.dadosUBS.versao.text())
            self.novos_dados_aprovacao["nr_estudo_tecnico"] = self.dadosUBS.le_numero_estudo_tecnico.text()
            self.novos_dados_aprovacao["dt_apvcao_estd_tcnco"] = datetime.strptime(self.dadosUBS.de_aprovacao_estudo_tecnico.text(), '%d/%m/%Y').date()
            self.novos_dados_aprovacao["valor_gf_apvda_estdo_tcnco"] = self.dadosUBS.le_valor_gf_estudo_tecnico.text().replace('.', '').replace(',', '.')
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_dados_aprovacao", 0)

    def versionar_dados_estruturacao(self):
        try:
            print("Caputurar dados inseridos pelo usuário")
            self.novos_dados_estruturacao["id"] = self.id
            self.novos_dados_estruturacao["versionamento"] = int(self.dadosUBS.versao.text())

            self.novos_dados_estruturacao["nm_sec_adm"] = self.dadosUBS.le_nomeSecuritizadoraAdm.text()
            self.novos_dados_estruturacao["cnpj_sec_adm"] = (self.dadosUBS.le_cnpjSecuritizadoraAdm.text()).replace('/','').replace('.', '').replace('-', '')
            self.novos_dados_estruturacao["nm_agente_fid"] = self.dadosUBS.le_nomeAgendeFiduciario.text()
            self.novos_dados_estruturacao["cnpj_agente_fid"] = (self.dadosUBS.le_cnpjAgendeFiduciario.text()).replace('/','').replace('.', '').replace('-', '')

            if self.dadosUBS.cb_especie.currentText() == "Quirografária":
                self.novos_dados_estruturacao["especie"] = 1
            elif self.dadosUBS.cb_especie.currentText() == "Subordinada":
                self.novos_dados_estruturacao["especie"] = 2
            elif self.dadosUBS.cb_especie.currentText() == "Garantia real":
                self.novos_dados_estruturacao["especie"] = 3
            elif self.dadosUBS.cb_especie.currentText() == "Flutuante":
                self.novos_dados_estruturacao["especie"] = 4

            if self.dadosUBS.cb_indexador_operacao.currentText() == "IPCA":
                self.novos_dados_estruturacao["indexador"] = 4
            elif self.dadosUBS.cb_indexador_operacao.currentText() == "CDI":
                self.novos_dados_estruturacao["indexador"] = 1

            if self.dadosUBS.cb_percentual_spreead_operacao.currentText() == '%':
                self.novos_dados_estruturacao["percent_spread"] = 1
            elif self.dadosUBS.cb_percentual_spreead_operacao.currentText() == 'Spread':
                self.novos_dados_estruturacao["percent_spread"] = 2

            self.novos_dados_estruturacao["nr_emissao"] = self.dadosUBS.le_numero_emissao.text()
            self.novos_dados_estruturacao["classe"] = self.dadosUBS.le_classe.text()
            self.novos_dados_estruturacao["series"] = self.dadosUBS.le_series_estruturacao.text()

            #self.novos_dados_estruturacao["taxa_op"] = self.dadosUBS.le_taxa_operacao.text().replace('.', '').replace(',', '.')
            #self.novos_dados_estruturacao["pu_emissao"] = self.dadosUBS.le_pu_emissao.text().replace('.', '').replace(',', '.')
            self.novos_dados_estruturacao["fee_estruturacao"] = self.dadosUBS.le_fee_estrturacao.text().replace('.', '').replace(',', '.')
            self.novos_dados_estruturacao["fee_sucesso"] = self.dadosUBS.le_fee_sucesso.text().replace('.', '').replace(',', '.')
            self.novos_dados_estruturacao["fee_garant_firme"] = self.dadosUBS.le_fee_garantia_firme.text().replace('.', '').replace(',', '.')
            self.novos_dados_estruturacao["fees_outras"] = self.dadosUBS.le_outras_fees.text().replace('.', '').replace(',', '.')
            self.novos_dados_estruturacao["fee_distrib_canal"] = self.dadosUBS.le_fee_distribuicao_canal.text().replace('.', '').replace(',', '.')

            # self.novos_dados_estruturacao["dt_emissao"] = datetime.strptime(self.dadosUBS.de_data_emissao.text(), '%d/%m/%Y').date()
            # self.novos_dados_estruturacao["dt_venc_emissao"] = datetime.strptime(self.dadosUBS.de_data_vencimento_emissao.text(), '%d/%m/%Y').date()
            # self.novos_dados_estruturacao["dt_inicial_juros"] = datetime.strptime(self.dadosUBS.de_data_inicial_juros.text(), '%d/%m/%Y').date()
            # self.novos_dados_estruturacao["dt_final_juros"] = datetime.strptime(self.dadosUBS.de_data_final_juros.text(), '%d/%m/%Y').date()
            # self.novos_dados_estruturacao["dt_inicial_amort"] = datetime.strptime(self.dadosUBS.de_data_inicial_amortizacao.text(), '%d/%m/%Y').date()
            # self.novos_dados_estruturacao["dt_final_amort"] = datetime.strptime(self.dadosUBS.de_data_final_amortizacao.text(), '%d/%m/%Y').date()
            self.novos_dados_estruturacao["dt_bookbuilding"] = datetime.strptime(self.dadosUBS.de_data_bookbuilding.text(), '%d/%m/%Y').date()
            self.novos_dados_estruturacao["dt_liquidacao"] = datetime.strptime(self.dadosUBS.de_data_liquidacao.text(), '%d/%m/%Y').date()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_dados_estruturacao", 0)

    def versionar_dados_liquidacao(self):
        try:
            print("Caputurar dados inseridos pelo usuário")
            self.novos_dados_liquidacao["id"] = self.id
            self.novos_dados_liquidacao["versionamento"] = int(self.dadosUBS.versao.text())

            self.novos_dados_liquidacao["codigo_ativo"] = self.dadosUBS.le_codigo_ativo.text()
            self.novos_dados_liquidacao["insi"] = self.dadosUBS.le_insi.text()
            self.novos_dados_liquidacao["pu_liquidacao"] = self.dadosUBS.le_pu_liquidacao.text().replace('.', '').replace(',', '.')

            if self.dadosUBS.simGFSE.isChecked():
                self.novos_dados_liquidacao["grtia_frm_exercida"] = '1'
            elif self.dadosUBS.naoGFSE.isChecked():
                self.novos_dados_liquidacao["grtia_frm_exercida"] = '0'

            print(self.novos_dados_liquidacao["grtia_frm_exercida"])

            self.novos_dados_liquidacao["vol_adquirido"] = self.dadosUBS.le_volume_adquirido.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["qtd_vlrs_mob_adq"] = self.dadosUBS.le_qtd_valores_mob_adquirido.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["porcent_sobras"] = self.dadosUBS.le_porcent_sobras.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["prob_col_realizada"] = self.dadosUBS.le_prob_colocacao_realizada.text()
            self.novos_dados_liquidacao["demanda_upb_merc_pri"] = self.dadosUBS.le_demanda_upb_merc_primario.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["aloc_upb_merc_pri"] = self.dadosUBS.le_alocacao_upb_mercado_primario.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["fee_upb_merc_pri"] = self.dadosUBS.le_fee_upb_mercado_primario.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["fee_retida_dist_merc_sec"] = self.dadosUBS.le_fee_retirada_dist_mercado_secundario.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["fee_recebida_bbbi"] = self.dadosUBS.le_fee_recebida_BBBI.text().replace('.', '').replace(',', '.')
            self.novos_dados_liquidacao["carteira_rm"] = self.dadosUBS.le_carteira_rm.text()
            self.novos_dados_liquidacao["grupo_rm"] = self.dadosUBS.le_grupo_rm.text()
            self.novos_dados_liquidacao["livro_rm"] = self.dadosUBS.le_livro_rm.text()
            self.novos_dados_liquidacao["categoria_contabil"] = self.dadosUBS.le_categoria_contabil.text()
            self.novos_dados_liquidacao["camara_registro"] = self.dadosUBS.le_camara_registro.text()
            self.novos_dados_liquidacao["codigo_grupo"] = self.dadosUBS.le_codigo_grupo.text()
            self.novos_dados_liquidacao["grupo"] = self.dadosUBS.le_grupo.text()
            self.novos_dados_liquidacao["codigo_livro"] = self.dadosUBS.le_codigo_livro.text()
            self.novos_dados_liquidacao["livro"] = self.dadosUBS.le_livro.text()
            self.novos_dados_liquidacao["cod_sub_livro"] = self.dadosUBS.le_codigo_sub_livro.text()
            self.novos_dados_liquidacao["sub_livro"] = self.dadosUBS.le_sub_livro.text()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - versionar_dados_liquidacao", 0)

    def campos_alterados_liquidacao(self):
        try:
            self.dadosUBS.le_prob_colocacao_realizada.clear()

            if self.dadosUBS.le_qtd_valores_mob_adquirido.text() != "":
                #colocar uma pausa aqui
                numerador = float(self.dadosUBS.le_qtd_valores_mob_adquirido.text().replace('.', '').replace(",", "."))
                print(numerador)
                denominador = float(self.dadosUBS.le_partGarantiaFirme.text().replace('.', '').replace(",", "."))
                print(denominador)

                if numerador != 0.0 and denominador != 0.0:
                    self.resultado = numerador/denominador
                    print(self.resultado)
                    self.result_porcet = round((self.resultado * 100), 4)
                else:
                    self.resultado = 0.0
                    self.result_porcet = 0.0

                self.dadosUBS.le_porcent_sobras.setText((str("{:,.2f}".format(self.result_porcet).replace(",", "X").replace(".", ",").replace("X", ".")) + "%"))

                if self.result_porcet == 1:
                    self.dadosUBS.le_prob_colocacao_realizada.setText(str("Muito Baixa"))
                elif 80.0 <= self.result_porcet <= 100.0:
                    self.dadosUBS.le_prob_colocacao_realizada.setText(str("Baixa"))
                elif 60.0 <= self.result_porcet < 80.0:
                    self.dadosUBS.le_prob_colocacao_realizada.setText(str("Média"))
                elif 40.0 <= self.result_porcet < 60.0:
                    self.dadosUBS.le_prob_colocacao_realizada.setText(str("Alta"))
                elif 0.0 <= self.result_porcet <= 20.0:
                    self.dadosUBS.le_prob_colocacao_realizada.setText(str("Muito Alta"))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - campos_alterados_liquidacao", 0)

    def campos_alterados_estudo(self):
        try:
            self.x = ""
            self.y = ""
            if self.dadosUBS.le_partGarantiaFirme.text() != '' and self.dadosUBS.cb_probabilidadeColocacao.currentText() != '':
                self.x = float(self.dadosUBS.le_partGarantiaFirme.text().replace(".", "").replace(",", "."))
                print(self.x)
                self.y = self.dadosUBS.cb_probabilidadeColocacao.currentText()
                print(self.y)

                if self.y == "Muito Baixa":
                    self.dadosUBS.le_impactoxprobabilidade.setText(str("{:,.2f}".format(1 * self.x).replace(",", "X").replace(".", ",").replace("X", ".")))
                elif self.y == "Baixa":
                    self.dadosUBS.le_impactoxprobabilidade.setText(str("{:,.2f}".format(0.8 * self.x).replace(",", "X").replace(".", ",").replace("X", ".")))
                elif self.y == "Média":
                    self.dadosUBS.le_impactoxprobabilidade.setText(str("{:,.2f}".format(0.6 * self.x).replace(",", "X").replace(".", ",").replace("X", ".")))
                elif self.y == "Alta":
                    self.dadosUBS.le_impactoxprobabilidade.setText(str("{:,.2f}".format(0.4 * self.x).replace(",", "X").replace(".", ",").replace("X", ".")))
                elif self.y == "Muito Alta":
                    self.dadosUBS.le_impactoxprobabilidade.setText(str("{:,.2f}".format(0.2 * self.x).replace(",", "X").replace(".", ",").replace("X", ".")))
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - campos_alterados_estudo", 0)

    def verificar_alteracao_cnpj(self, cnpj_antigo):
        try:
            print(cnpj_antigo)

            cnpj_novo = int((self.dadosUBS.cnpj_emissor.text()).replace('/','').replace('.', '').replace('-', ''))
            print(cnpj_novo)

            if cnpj_antigo != cnpj_novo:
                # limpar dados do clientes
                self.limpar_cliente()
                self.insere_dados_cliente()

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - verificar_alteracao_cnpj", 0)

    def limpar_formulario(self):
        try:
            self.limpar_status()
            self.limpar_cliente()
            self.limpar_ubs()
            self.limpar_cb_lastros()
            self.limpar_lastros()
            self.limpar_series()
            self.limpar_estudo()
            self.limpar_aprovacao()
            self.limpar_estruturacao()
            self.limpar_liquidacao()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - limpar_formulario", 0)

    def limpar_status(self):
        self.dadosUBS.comboBox_status.setCurrentText(str(""))
        self.dadosUBS.te_motivo_status.clear()

    def limpar_cliente(self):
        self.dadosUBS.le_mci.clear()
        self.dadosUBS.le_grupo_economico.clear()
        self.dadosUBS.le_nome_grupo_economico.clear()
        self.dadosUBS.le_uor.clear()
        self.dadosUBS.le_cep.clear()
        self.dadosUBS.le_prefixo.clear()
        self.dadosUBS.le_carteira.clear()

        self.dadosUBS.le_agencia.clear()
        self.dadosUBS.le_conta.clear()

        self.dadosUBS.le_uor_diretoria.clear()
        self.dadosUBS.le_prefixo_diretoria.clear()
        self.dadosUBS.le_nome_diretoria.clear()

        self.dadosUBS.le_uor_regional.clear()
        self.dadosUBS.le_prefixo_regional.clear()
        self.dadosUBS.le_nome_regional.clear()

        self.dadosUBS.le_uor_super.clear()
        self.dadosUBS.le_prefixo_super.clear()
        self.dadosUBS.le_nome_super.clear()

        self.dadosUBS.le_matricula_gerente_geral.clear()
        self.dadosUBS.le_nome_gerente_geral.clear()

        self.dadosUBS.le_matricula_gerente_negocios.clear()
        self.dadosUBS.le_nome_gerente_negocios.clear()

        self.dadosUBS.le_matricula_gerente_relacionamento.clear()
        self.dadosUBS.le_nome_gerente_relacionamento.clear()

        self.dadosUBS.le_limite_aprovado.clear()
        self.dadosUBS.le_limite_disponivel.clear()

        self.dadosUBS.le_limite_aprovado_tvm.clear()
        self.dadosUBS.le_limite_disponivel_tvm.clear()

        self.dadosUBS.le_limite_aprovado_distribuicao.clear()
        self.dadosUBS.le_limite_disponivel_distribuicao.clear()

    def limpar_ubs(self):
        self.dadosUBS.cb_ativo.setCurrentText(str(""))
        self.dadosUBS.nome_emissor.clear()
        self.dadosUBS.cnpj_emissor.clear()
        self.dadosUBS.coordenador_lider.clear()
        self.dadosUBS.demais_coordenadores.clear()

        self.dadosUBS.simLei.setChecked(False)
        self.dadosUBS.simConversiveisAcao.setChecked(False)
        self.dadosUBS.simLoteAdicional.setChecked(False)
        self.dadosUBS.simHaveraEsforcos.setChecked(False)
        self.dadosUBS.simTeraGarantia.setChecked(False)
        self.dadosUBS.simPermiteResgate.setChecked(False)
        self.dadosUBS.simMarketMac.setChecked(False)
        self.dadosUBS.simBalancoAuditado.setChecked(False)
        self.dadosUBS.simBalancoDivulgado.setChecked(False)
        self.dadosUBS.simRFP.setChecked(False)
        self.dadosUBS.simESG.setChecked(False)

        self.dadosUBS.naoLei.setChecked(False)
        self.dadosUBS.naoConversiveisAcao.setChecked(False)
        self.dadosUBS.naoLoteAdicional.setChecked(False)
        self.dadosUBS.naoHaveraEsforcos.setChecked(False)
        self.dadosUBS.naoTeraGarantia.setChecked(False)
        self.dadosUBS.naoPermiteResgate.setChecked(False)
        self.dadosUBS.naoMarketMac.setChecked(False)
        self.dadosUBS.naoBalancoAuditado.setChecked(False)
        self.dadosUBS.naoBalancoDivulgado.setChecked(False)
        self.dadosUBS.naoRFP.setChecked(False)
        self.dadosUBS.naoESG.setChecked(False)

        self.dadosUBS.cb_nomeCoordenador.setCurrentText(str(""))
        self.dadosUBS.cb_cnpjCoordenador.setCurrentText(str(""))
        self.dadosUBS.cb_legislacaoCVM.setCurrentText(str(""))
        self.dadosUBS.cb_ritoRegistro.setCurrentText(str(""))
        self.dadosUBS.cb_documentoOferta.setCurrentText(str(""))
        self.dadosUBS.cb_regimeColocacao.setCurrentText(str(""))
        self.dadosUBS.cb_ratingEmissora.setCurrentText(str(""))
        self.dadosUBS.cb_ratingOferta.setCurrentText(str(""))
        self.dadosUBS.cb_probabilidadeColocacao.setCurrentText(str(""))
        self.dadosUBS.cb_tipoEmissor.setCurrentText(str(""))
        self.dadosUBS.cb_fee_forma_calculo.setCurrentText(str(""))

        self.dadosUBS.le_valorEmissao.clear()
        self.dadosUBS.te_destinacaoRecursos.clear()
        self.dadosUBS.le_partGarantiaFirme.clear()
        self.dadosUBS.le_loteAdicionalMax.clear()
        self.dadosUBS.le_premioResgAntBFF.clear()
        self.dadosUBS.te_garantia.clear()
        self.dadosUBS.le_feeTotal.clear()
        self.dadosUBS.le_feeCanal.clear()
        self.dadosUBS.le_outrasFees.clear()
        self.dadosUBS.spinBox_series.clear()
        self.dadosUBS.de_previsaoLiquidacao.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_dtLimiteEnvioProp.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.le_empresaAudit.clear()
        self.dadosUBS.te_justificativa.clear()
        self.dadosUBS.te_covenants.clear()
        self.dadosUBS.te_observacoes.clear()

    def limpar_cb_lastros(self):
        self.dadosUBS.cb_lastro.setCurrentText(str(""))

    def limpar_lastros(self):
        self.dadosUBS.simResolvencia.setChecked(False)
        self.dadosUBS.naoResolvencia.setChecked(False)
        self.dadosUBS.simSubordinacao.setChecked(False)
        self.dadosUBS.naoSubordinacao.setChecked(False)
        self.dadosUBS.simSeguro.setChecked(False)
        self.dadosUBS.naoSeguro.setChecked(False)

        self.dadosUBS.le_lastroVolMedio.clear()
        self.dadosUBS.le_lastroTicketMedio.clear()
        self.dadosUBS.le_lastroVolTotalCarteira.clear()
        self.dadosUBS.le_lastroVolDispCessao.clear()
        self.dadosUBS.le_lastroInadMedia.clear()
        self.dadosUBS.te_lastroConcCarteira.clear()
        self.dadosUBS.te_lastroIndiceMedioPagAtraso.clear()
        self.dadosUBS.te_lastro10MaioresDeve.clear()
        self.dadosUBS.te_lastroPrazoMedioPagAtraso.clear()
        self.dadosUBS.te_astroPrazoMedioCarteira.clear()
        self.dadosUBS.te_IndiceMedioDistratoDevol.clear()

    def limpar_series(self):
        self.dadosUBS.cb_tipo.setCurrentText(str(""))
        self.dadosUBS.cb_pagamento_principal.setCurrentText(str(""))
        self.dadosUBS.cb_pagamento_juros.setCurrentText(str(""))
        self.dadosUBS.cb_indexador.setCurrentText(str(""))
        self.dadosUBS.cb_publicoAlvoMercadoPrimario.setCurrentText(str(""))
        self.dadosUBS.cb_publicoAlvoMercadoSecundario.setCurrentText(str(""))

        self.dadosUBS.le_prazo_total.clear()
        self.dadosUBS.le_carencia_principal.clear()
        self.dadosUBS.le_carencia_juros.clear()
        self.dadosUBS.le_inicio_pagamento_principal.clear()
        self.dadosUBS.le_informar_referencia.clear()
        self.dadosUBS.le_taxa.clear()

    def limpar_estudo(self):
        self.dadosUBS.cb_assessorBBBI.setCurrentText(str(""))
        self.dadosUBS.cb_estrategia_distribuicao.setCurrentText(str(""))

        self.dadosUBS.simTVM.setChecked(False)
        self.dadosUBS.naoTVM.setChecked(False)

        self.dadosUBS.simUPB.setChecked(False)
        self.dadosUBS.naoUPB.setChecked(False)

        self.dadosUBS.le_prazo_venda_upb.clear()
        self.dadosUBS.le_impactoxprobabilidade.clear()
        self.dadosUBS.le_limite_global_rc.clear()
        self.dadosUBS.le_limite_especifico_rc.clear()
        self.dadosUBS.de_consulta_viab_tvm.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_consulta_upb.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_proposta_negocios.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.te_retorno_consulta_viabilidade_tvm.clear()
        self.dadosUBS.te_retorno_consulta_upb.clear()
        self.dadosUBS.te_resultado_proposta_negocios.clear()

    def limpar_aprovacao(self):
        self.dadosUBS.le_numero_estudo_tecnico.clear()
        self.dadosUBS.de_aprovacao_estudo_tecnico.clear()
        self.dadosUBS.le_valor_gf_estudo_tecnico.clear()

    def limpar_estruturacao(self):
        self.dadosUBS.le_nomeSecuritizadoraAdm.clear()
        self.dadosUBS.le_cnpjSecuritizadoraAdm.clear()
        self.dadosUBS.le_nomeAgendeFiduciario.clear()
        self.dadosUBS.le_cnpjAgendeFiduciario.clear()

        self.dadosUBS.cb_especie.setCurrentText(str(""))
        self.dadosUBS.cb_indexador_operacao.setCurrentText(str(""))
        self.dadosUBS.cb_percentual_spreead_operacao.setCurrentText(str(""))

        self.dadosUBS.le_numero_emissao.clear()
        self.dadosUBS.le_classe.clear()
        self.dadosUBS.le_series_estruturacao.clear()
        #self.dadosUBS.le_taxa_operacao.clear()
        #self.dadosUBS.le_pu_emissao.clear()
        self.dadosUBS.le_fee_estrturacao.clear()
        self.dadosUBS.le_fee_sucesso.clear()
        self.dadosUBS.le_fee_garantia_firme.clear()
        self.dadosUBS.le_outras_fees.clear()
        self.dadosUBS.le_fee_distribuicao_canal.clear()

        # self.dadosUBS.de_data_emissao.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_vencimento_emissao.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_inicial_juros.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_final_juros.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_inicial_amortizacao.setDateTime(QtCore.QDateTime.currentDateTime())
        # self.dadosUBS.de_data_final_amortizacao.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_data_bookbuilding.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dadosUBS.de_data_liquidacao.setDateTime(QtCore.QDateTime.currentDateTime())
    def limpar_liquidacao(self):
        self.dadosUBS.le_codigo_ativo.clear()
        self.dadosUBS.le_insi.clear()
        self.dadosUBS.le_pu_liquidacao.clear()

        self.dadosUBS.simGFSE.setChecked(False)
        self.dadosUBS.naoGFSE.setChecked(False)

        self.dadosUBS.le_volume_adquirido.clear()
        self.dadosUBS.le_qtd_valores_mob_adquirido.clear()
        self.dadosUBS.le_porcent_sobras.clear()
        self.dadosUBS.le_prob_colocacao_realizada.clear()

        self.dadosUBS.le_demanda_upb_merc_primario.clear()
        self.dadosUBS.le_alocacao_upb_mercado_primario.clear()
        self.dadosUBS.le_fee_upb_mercado_primario.clear()
        self.dadosUBS.le_fee_retirada_dist_mercado_secundario.clear()
        self.dadosUBS.le_fee_recebida_BBBI.clear()
        self.dadosUBS.le_carteira_rm.clear()
        self.dadosUBS.le_grupo_rm.clear()
        self.dadosUBS.le_livro_rm.clear()
        self.dadosUBS.le_categoria_contabil.clear()
        self.dadosUBS.le_camara_registro.clear()
        self.dadosUBS.le_codigo_grupo.clear()
        self.dadosUBS.le_grupo.clear()
        self.dadosUBS.le_codigo_livro.clear()
        self.dadosUBS.le_livro.clear()
        self.dadosUBS.le_codigo_sub_livro.clear()
        self.dadosUBS.le_sub_livro.clear()

    def funcao_inserir_tab(self):
        self.dadosUBS.tabWidget.setTabVisible(0, True)
        self.dadosUBS.tabWidget.setTabVisible(1, False)
        self.dadosUBS.tabWidget.setTabVisible(2, False)
        self.dadosUBS.tabWidget.setTabVisible(3, False)
        self.dadosUBS.tabWidget.setTabVisible(4, False)
        self.nr_tabs = self.dadosUBS.spinBox_series_efetivadas.value()
        print(self.nr_tabs)
        for i in range (self.nr_tabs):
            self.dadosUBS.tabWidget.setTabVisible(i, True)

    def capturar_dados(self):
        print(self.nr_tabs)
        for i in range (self.nr_tabs):
            spinBox_serie = self.dadosUBS.tabWidget.findChild(QSpinBox, "spinBox_serie_" + str(i))
            print(spinBox_serie)

            if spinBox_serie:
                value = spinBox_serie.value()
                print(value)

""""
if __name__ == "__main__":
    import sys

    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QtWidgets.QApplication(sys.argv)
    p = PreencherPlanilha()
    p.dadosUBS.show()
    sys.exit(app.exec_())
"""