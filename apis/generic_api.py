import requests
import json
import ctypes
from getpass import getpass
# from objetos.usuario import Usuario
import pymsgbox


class Generic_Api:
    token = ""
    status_api = ""
    status_api_post = ""
    req_token = ""
    req_token_final = ""
    status_api_get = ""

    def gera_token(self, chave, senha, autenticador=""):
        try:
            # Tenta gerar o token via chave e senha
            if len(autenticador) == 0:
                url = "https://gsv.uop.bb.com.br:8443/gsv/api/autenticador/v1/openAM"
                header = {'Content-type': 'application/json'}
                body = {"usuario": chave, "senha": senha}
                self.req_token = requests.post(url, headers=header, data=json.dumps(body), verify=False)
                # print(self.req_token)
                # print(type(self.req_token))
                self.req_token_final = json.loads(self.req_token.text)
                # print(self.req_token_final)
                self.token = self.req_token_final['BBSSOTokenUOP']
                # print(self.token)
                return self.token

            elif len(autenticador) == 6:
                url2 = "https://gsv.uop.bb.com.br:8443/gsv/api/autenticador/v1/openAM2FA"
                header = {'Content-type': 'application/json'}
                body = {"usuario": chave, "senha": senha, "sfa": autenticador}
                self.req_token = requests.post(url2, headers=header, data=json.dumps(body), verify=False)

                if self.req_token.status_code == 401 and 'senha' not in self.req_token.text:
                    autenticador = pymsgbox.prompt('Digite seu codigo 2FA:', '2FA')
                    self.gera_token(chave, senha, autenticador)
                    return self.token

                    # print(self.req_token)
                self.req_token_final = json.loads(self.req_token.text)
                # print(self.req_token_final)
                self.token = self.req_token_final['BBSSOTokenUOP']

                # print(self.token)
                return self.token

            else:
                ctypes.windll.user32.MessageBoxW(0, "Você digitou um número de autenticador inválido", "Atenção", 0)
                return False

        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            if 'BBSSOTokenUOP' in retorno:
                ctypes.windll.user32.MessageBoxW(0, "Chave ou Senha invalida", "Erro", 0)
            else:
                ctypes.windll.user32.MessageBoxW(0, "API indisponível. Contate o administrativo", "Atenção", 0)
            return False

    def executarAPIPostToken(self, gson, url, token, tipo=1):

        header = {'Content-type': 'application/json',
                  "Cookie": "BBSSOToken=" + token + ";ssoacr=sso.intranet.bb.com.br;", }
        if tipo == 1:  # joker
            header["Authorization"] = "Basic Y29uY2lsaWFjYW9DREM6ZXZRMTQjdko2JHp4YjNWIQ=="
        if 'query' in gson:
            gson['query'] = gson['query'].strip().replace("\n", " ").replace("\t", " ")

        req = requests.post(url, data=json.dumps(gson), headers=header,
                            verify=False)  # requests.post(url, headers=header, data=json.dumps(gson), verify=False)
        self.status_api_post = req.status_code
        if self.status_api_post > 400:
            print('Erro na API\n' + req.text)
            return []
        return json.loads(req.text)


    def executarAPIGet(self, url):
        req = requests.get(url, verify=False)
        # print(req)
        self.status_api_get = req.status_code
        # print(self.status_api_get)
        return req

    def executarAPIGetToken(self, url, token):
        headerToken = {"Cookie": "BBSSOToken=" + token}
        req = requests.get(url, headers=headerToken, verify=False)
        # print(req)
        self.status_api_get = req.status_code
        # print(self.status_api_get)
        return req