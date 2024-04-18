from datetime import datetime
from apis.generic_api import Generic_Api
from objetos.api_token import ApiToken
from objetos.usuario import Usuario

class Api:

    ga = Generic_Api()
    token = ""
    urlJoker = "https://redediope.jokerapi.servicos.bb.com.br/query"

    def validarToken(self, token):
        try:
            tempo_token = (datetime.now().time().minute + (datetime.now().time().hour * 60)) - ApiToken.hora_inicio
            #print(ApiToken.token)
            #print(tempo_token)
            #print(type(tempo_token))
            #print(str(datetime.now().time().minute + (datetime.now().time().hour * 60)) + ' - ' + str(
                #ApiToken.hora_inicio))
            if tempo_token > 55:
                return False
            if token == {}:
                return False
            if token != "":
                return True
        except Exception as e:
            # print(req)
            print("Erro: {}".format(e.args))
            return False

    def regerarToken(self):
        ApiToken.token = self.ga.gera_token(Usuario.chave, Usuario.senha, Usuario.autenticador)
        ApiToken.hora_inicio = datetime.now().time().minute + (datetime.now().time().hour * 60)

    def dados_funci(self, matricula):
        if not self.validarToken(ApiToken.token):
            self.regerarToken()

        if self.validarToken(ApiToken.token):
            try:
                json = {"query": "SELECT MATRICULA_215, NOME_IDENTIFICACAO_215, COMISSAO_215, SEXO_215  "
                                 "FROM DB2DWH.VS_CAD_BASC "
                                 "WHERE MATRICULA_215 = " + matricula + ";"

                        }

                retorno = self.ga.executarAPIPostToken(json, self.urlJoker, ApiToken.token)
                #print(retorno)
                if retorno:
                    Usuario.nome = str(retorno[0]['NOME_IDENTIFICACAO_215'])
                    Usuario.cargo = str(retorno[0]['COMISSAO_215'])
                    Usuario.sexo = str(retorno[0]['SEXO_215'])

            except Exception as e:
                print("Erro no PY SINGLE GUI: {}".format(e.args))