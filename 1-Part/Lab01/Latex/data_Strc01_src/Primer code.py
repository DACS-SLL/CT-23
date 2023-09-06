import pandas as pd
import random
import sys

original_stdout = sys.stdout

nombre_archivo = "Trabajo.txt"

with open(nombre_archivo, 'w') as archivo:
    sys.stdout = archivo
    
    delta = pd.read_csv("delta.csv", index_col=0)
    alfabeto = ["0", "1"]
    estado_inicial = "A"
    F = ["C"]
  
      
    for i in range(0, 2000, 1):
        x = estado_inicial
        longitud = random.randint(10, 50)
        combinacion = ''.join([str(random.choice(alfabeto)) for _ in range(longitud)]) 
        print(">>", combinacion, " --> ", end="")
      
        for i in range(0, len(combinacion), 1):
            x = delta.loc[x, combinacion[i]]
                   
        if x in F:
            print("Aceptado")
        else:
            print("No Aceptado")

sys.stdout = original_stdout

print("Resultado generado exportado en", nombre_archivo)








    

