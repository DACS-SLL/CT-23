import pandas as pd
import random
from graphviz import Digraph

nombre_archivo_dot = "Trabajo.dot"
nombre_archivo_png = "Trabajo.png"

# Lectura de Archivo
try:
    delta = pd.read_csv("Data_Inicial.csv", index_col=0)
except FileNotFoundError:
    print("Error: Archivo 'Data_Inicial.csv' no encontrado.")
    exit(1)

# Generación de Grafo
conexiones = {}

def construir_conexiones(row):
    estado_actual = row.name
    for column, estado_siguiente in row.items():
        if estado_siguiente != "vac":
            if (estado_actual, column) not in conexiones:
                conexiones[(estado_actual, column)] = set()
            conexiones[(estado_actual, column)].add(estado_siguiente)

delta.apply(construir_conexiones, axis=1)

# Escritura en Archivo DOT
with open(nombre_archivo_dot, 'w') as archivo_dot:
    archivo_dot.write("digraph AFN {\n")
    for (estado_actual, simbolo_entrada), estados_siguientes in conexiones.items():
        for estado_siguiente in estados_siguientes:
            archivo_dot.write(f'  "{estado_actual}" -> "{estado_siguiente}" [label="{simbolo_entrada}"];\n')
    archivo_dot.write("}\n")

# Convertir DOT a PNG con Graphviz
graph = Digraph('AFN', format='png')
graph.attr(size='8,5')
graph.attr(dpi='300')
graph.render(nombre_archivo_dot, cleanup=True, format='png')
print(f"Resultado generado exportado en {nombre_archivo_dot} y {nombre_archivo_png}")


# Simulación de Autómata No Determinista
def simular_afn(estado_actual, combinacion):
  if not combinacion:
      return estado_actual

  simbolo_actual = combinacion[0]
  nuevos_estados = conexiones.get((estado_actual, simbolo_actual), set())

  if not nuevos_estados:
      # Imprimir para depuración
      print(f"No hay transiciones desde {estado_actual} con símbolo {simbolo_actual}")
      return None

  nuevo_estado = random.choice(list(nuevos_estados))
  print(f"Desde {estado_actual} con {simbolo_actual} a {nuevo_estado}")

  return simular_afn(nuevo_estado, combinacion[1:])


estados_finales = ["C"]
contador_aceptados = 0

for _ in range(1000):  # Reducido el número de iteraciones
    estado_actual = "A"

    longitud = random.randint(3, 5)
    combinacion = ''.join([str(random.choice(["0", "1"])) for _ in range(longitud)])
    print(f">> {combinacion}  --> ", end="")

    resultado_simulacion = simular_afn(estado_actual, combinacion)

    if resultado_simulacion in estados_finales:
        print("Aceptado")
        contador_aceptados += 1
    else:
        print("No Aceptado")

# Cálculos y Estadísticas
porcentaje_aceptados = (contador_aceptados / 1000) * 100
porcentaje_rechazados = 100 - porcentaje_aceptados

# Escritura en Archivo
with open(nombre_archivo, 'w') as archivo:
    for (estado_actual, simbolo_entrada), estado_siguiente in conexiones.items():
        archivo.write(f"{estado_actual} -> {estado_siguiente} [label = {simbolo_entrada}];\n")

    archivo.write("\n")
    archivo.write("------------------------------------------------------------\n\n")
    archivo.write(f"Porcentaje de Aceptados: {porcentaje_aceptados:.2f}%\n")
    archivo.write(f"Porcentaje de Rechazados: {porcentaje_rechazados:.2f}%\n")

print("Resultado generado exportado en", nombre_archivo)