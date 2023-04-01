import pandas as pd
import pickle



with open ("tabela_1_config.pkl", mode ='rb') as f:
        tabela = pickle.load(f)

tabela = pd.DataFrame(tabela)
tabela.head()