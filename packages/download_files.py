# Arquivo para baixar o csv com as empresas brasileiras e o arquivo contendo os cnaes. (Não atualiza).

import gdown

def download_empresas():
    print('+ Baixando arquivo empresas...\n')
    url = 'https://drive.google.com/uc?id=1VEsbUPkAoHc1tcy2huJ8snaNvXsx103j'
    gdown.download(url, 'empresas.csv', quiet=False)
    print("+ Arquivo baixado com sucesso...\n")

def download_cnaes():
    print('+ Baixando arquivo de cnaes...\n')
    url = 'https://docs.google.com/uc?id=1SecSVFSCx4IpUgf18RxFKS7JHR_Bb9So'
    gdown.download(url, 'cnaes.xlsx', quiet=False)
    print("+ Arquivo baixado com sucesso...\n")