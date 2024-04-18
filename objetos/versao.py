import uuid


class Versao:

    # maior = 1
    # media = 1
    # menor = 0
    # versao = str(maior) + "." + str(media) + "." + str(menor)

    def __init__(self):
        self.nome_ferramenta = 'Gestão-BB-BI'
        self.maior = 1
        self.media = 1
        self.menor = 3
        self.versao = str(self.maior) + "." + str(self.media) + "." + str(self.menor)

    def retornar_upgrade_code(self):
        upgrade_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, self.nome_ferramenta)).upper()
        return '{' + upgrade_code + '}'

    def nome_instalador(self):
        return f'{self.nome_ferramenta}.msi'

