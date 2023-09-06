import pandas as pd

# definición del automata ####################
delta = pd.read_csv("delta.csv", index_col=0)
alfabeto = ["0", "1"]
estado_inicial = "A"
F = ["C"]
##############################################

palabra_test = "00001"

# evaluar si palabra_test pertence al lenguaje

x = delta.loc[ "A", "0" ]