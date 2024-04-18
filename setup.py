import shutil
import os
from cx_Freeze import setup, Executable
from objetos.versao import Versao

versao = Versao()
print('Versao', versao.versao)

# Atualizar o arquivo 'requirements.txt'
os.system('pip freeze > requirements.txt')

if os.path.exists('dist'): shutil.rmtree('dist')
if os.path.exists('build'): shutil.rmtree('build')
os.mkdir('dist')
os.mkdir('build')

inicio  = "controles/controle_principal.py"


setup(
    summary_data={
        "author": "Banco do Brasil S/A.",
        "comments": "Programa para Gestão-BB-BI"
    },
    description="Gestão-BB-BI",
    name="Gestão-BB-BI",
    version=versao.versao,
    options={"build_exe": {
        'packages': ["os",
                     "sys",
                     "ctypes",
                     "win32con",
                     "xlwt",
                     "pandas",
                     "controles",
                     "objetos",
                     "querys",
                     "numpy",
                     "apis",
                     'sqlalchemy'
                    ],
        'excludes': [
            'test',
            'sqlite3',
            'unittest'
        ],
        'include_files': [
            'controles/bbbi.png',
            'controles/formulario_dados.ui',
            'controles/formulario_principal.ui',
            'controles/formulario_lista_operacoes.ui',
            'controles/logo_bb.ico',
            'controles/logo_bb.png',
            'controles/manutencao.jpg',
            'controles/estamosEmManutencao.jpeg',
            'controles/ubs.png'
        ],
        'include_msvcr': True,
    }, 'bdist_msi': {
        'initial_target_dir': 'C:\\Aplicativos BB\\Gestão-BB-BI',
        'upgrade_code': versao.retornar_upgrade_code(),
        'target_name': versao.nome_instalador(),
        'add_to_path': False,

     }},

    executables=[Executable(inicio, base="Win32GUI",
                            icon="controles/logo_bb.ico",
                            target_name="Gestão-BB-BI")]

)

""" Usar o comando abaixo no terminal para gerar o executavel:
    python setup.py bdist_msi """

