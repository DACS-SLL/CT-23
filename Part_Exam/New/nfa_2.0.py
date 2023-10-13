import pandas as pd
import random
import sys
import math

original_stdout = sys.stdout

nombre_archivo = "Trabajo.txt"

with open(nombre_archivo, 'w') as archivo:
    sys.stdout = archivo
    
    delta = pd.read_csv("Data.csv", index_col=0)
    alfabeto = ["x", "w", "z"]
    estado_inicial = "A"
    F = ["A", "B"]
  
    for index, row in delta.iterrows():
        estado_actual = index
        for column, value in row.items():
            simbolo_entrada = column
            if not pd.isna(value):
                estados_siguientes = value.split(';') if isinstance(value, str) else [value]
                
                for estado_siguiente in estados_siguientes:
                    print(estado_actual, "->", estado_siguiente, "[label =", simbolo_entrada,"];")


    print("\n")
    print("------------------------------------------------------------")
    print("\n")

    contador_aprobados = 0  
    for _ in range(500):
        x = [estado_inicial]  # Ahora usamos una lista para almacenar un conjunto de estados
        longitud = random.randint(3, 5)
        combinacion = ''.join([str(random.choice(alfabeto)) for _ in range(longitud)]) 
        print(">>", combinacion, " --> ", end="")
      
        for i in range(len(combinacion)):
            nuevos_estados = set()
            for estado in x:
                siguiente_estado = delta.loc[estado, combinacion[i]]
                if not pd.isna(siguiente_estado):
                    siguientes = siguiente_estado.split(';') if isinstance(siguiente_estado, str) else [siguiente_estado]
                    nuevos_estados.update(siguientes)
            x = list(nuevos_estados)
                   
        if any(estado in F for estado in x):
            print("Aceptado")
            contador_aprobados = contador_aprobados + 1
        else:
            print("No Aceptado")
    print("La aceptación de los estados fue: ", (contador_aprobados*100)/500, "%")
        

sys.stdout = original_stdout

print("Resultado generado exportado en", nombre_archivo)