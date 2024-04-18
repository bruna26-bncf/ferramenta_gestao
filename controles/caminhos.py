import os
class Caminho:
    @staticmethod
    def caminho_ui():
        caminho = os.path.dirname(os.path.abspath(__file__))+"\\"
        if "Aplicativos BB"  in caminho:
            caminho= "C:\\Aplicativos BB\\Distribuicao\\"
        return caminho