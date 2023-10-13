import pandas as pd
import random
import matplotlib.pyplot as plt
import networkx as nx

nombre_archivo_dot = "Trabajo.dot"
nombre_archivo_png = "Trabajo.png"

# Lectura de Archivo
try:
    delta = pd.read_csv("Data_Inicial.csv", index_col=0)
except FileNotFoundError:
    print("Error: Archivo 'Data_Inicial.csv' no encontrado.")
    exit(1)

# Generación de Grafo
G = nx.DiGraph()

def construir_conexiones(row):
    estado_actual = row.name
    for column, estado_siguiente in row.items():
        if estado_siguiente != "vac":
            G.add_edge(estado_actual, estado_siguiente, label=str(column))

delta.apply(construir_conexiones, axis=1)

# Visualización con Matplotlib
pos = nx.spring_layout(G)  # Puedes ajustar el layout según tus preferencias

edge_labels = {(n1, n2): label['label'] for n1, n2, label in G.edges(data=True)}
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.savefig(nombre_archivo_png, format="png", dpi=300)
plt.show()

# Escritura en Archivo DOT
# Escritura en Archivo DOT
with open(nombre_archivo_dot, 'w') as archivo_dot:
    archivo_dot.write("digraph AFN {\n")
    for (estado_actual, simbolo_entrada, label) in G.edges(data=True):
        archivo_dot.write(f'  "{estado_actual}" -> "{label["label"]}" [label="{simbolo_entrada}"];\n')
    archivo_dot.write("}\n")


print(f"Resultado generado exportado en {nombre_archivo_dot} y {nombre_archivo_png}")

def simular_afn(estado_actual, combinacion, conexiones):
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

    return simular_afn(nuevo_estado, combinacion[1:], conexiones)

# Resto del código...

# Uso de la función simular_afn con conexiones como argumento
for _ in range(1000):
    estado_actual = "B"
    estados_finales = ["C", "F", "I"]
    contador_aceptados = 0

    longitud = random.randint(3, 5)
    combinacion = ''.join([str(random.choice(["0", "1"])) for _ in range(longitud)])
    print(f">> {combinacion}  --> ", end="")

    resultado_simulacion = simular_afn(estado_actual, combinacion, G.edges)

    if resultado_simulacion in estados_finales:
        print("Aceptado")
        contador_aceptados += 1
    else:
        print("No Aceptado")

# Cálculos y Estadísticas
porcentaje_aceptados = (contador_aceptados / 1000) * 100
porcentaje_rechazados = 100 - porcentaje_aceptados