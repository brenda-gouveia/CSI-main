import os
import pandas as pd
import os.path
import json

'''
Fiz esse código afim de inserir todos os valores de batimento por posição, ao contrário 
do anterior que fazia a média.

'''

def checar(objeto):

    if (objeto.find("arq") == -1):
        return True
    if (objeto.find('arqex')>= 0):
        return True
    else:
        return False
    
def verificar(objeto):
    if str(type(objeto)).find("Series") != -1:
        return False
    else:
        return True
    
def tabelar(bpm, scan):
    
    global relogio

    bpm = pd.Series(bpm)

    if verificar(relogio.get(scan)): # caso não tenha o scan
        relogio[scan] = bpm
    else:
        x = relogio.get(scan)
        relogio[scan] = pd.concat([x,bpm], ignore_index = True)



print("########## CSI EXPLORER Begins ##########")

path = "heartRateData" # caminho dos scans

########### Escolha das pastas #################################3
relogio = {}
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, path)
scans = os.listdir(file_path)

################# Usando um loop para acessar os arquivos de cada pasta #################


for pasta in scans: # vai rodar os scans
    aux = os.listdir(pasta)
    sequence = 1
    while sequence <18:
        arquivo = 'arq' + str(sequence) + '.json'

        if checar(arquivo):
            continue

        arq = os.path.join(file_path, pasta)
        arquivo = os.path.join(arq, arquivo)

        try:
            dados = pd.read_json(arquivo)
        except FileNotFoundError:
            print(f'File {arquivo} not found.')
            exit(-1)

        #with open(arquivo, 'rb') as arq:
        #    dados = json.load(arq, arquivo)
        x = str(dados["heart_rate"].to_numpy())
        tabelar(x, pasta)
        #arquivo.close()
        sequence = sequence + 1
        print(relogio)


tab = pd.DataFrame(relogio)
tab.to_excel("relogio.xlsx")
