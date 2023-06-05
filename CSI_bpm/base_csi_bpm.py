import config
from analysis.dataAnalysis import analyze
import decoders.interleaved as decoder
from plotters.AmpPhaPlotter import Plotter
import os
import dataset.coleta as dataset
#import dataset.tabela as tabela
from os.path import dirname, join
import pandas as pd
import pickle
import numpy as np

import warnings
warnings.simplefilter("ignore", np.ComplexWarning)

def verificar(objeto):
    if str(type(objeto)).find("Series") != -1:
        return False
    else:
        return True
    
def batimentos(scan, bpm):
    
    global tabela

    bpm = pd.Series(bpm)

    if verificar(tabela.get(scan)): # caso não tenha o scan
        tabela[scan] = bpm
    else:
        x = tabela.get(scan)
        tabela[scan] = pd.concat([x,bpm], ignore_index = True)


if __name__ == "__main__":

    tabela = {}

    print("########## CSI EXPLORER Begins ##########")

    path = "..\scans" # caminho dos scans
    current_dir = dirname(__file__)
    file_path = join(current_dir, path)

    scans = os.listdir(path)

    quantidade = 0

    for filename in scans: 
        caminho = os.path.join(path,filename)
        sequence = 1
        quantidade +=1

        while sequence <18 and quantidade <118:
            file = 'arq' + str(sequence)
            file_exists = dataset.check_next_file(file)
            print('Processados :', quantidade)
            if file_exists:
                
                
                bpm1,bpm2,bpm3, bpm4, bpm5, bpm6, bpm7 = dataset.process_pcap_file(file, caminho, sequence)
                print("##########  BPM   "+ file + "  " + filename + "  "+str(bpm1)+ " "+ str(bpm2)+ " " + str(bpm3))
                print(" "+ str(bpm4) + " " + str(bpm5)+ ' '+ str(bpm6) + ' ' + str(bpm7)+ "##############")

                bpm_str = str(bpm1)+","+ str(bpm2)+','+str(bpm3)+','+str(bpm4)+','+str(bpm5)+','+str(bpm6)+ ',' + str(bpm7)

                batimentos(filename, bpm_str)
                print(pd.DataFrame(tabela))
            else:
                break
            sequence += 1
    
    tab = pd.DataFrame(tabela)
    tab.to_excel("tab_config1.xlsx")       
                 
    print("########## CSI EXPLORER Ends ##########")
    comando = input('Type anything to close: ')
    os._exit(1)