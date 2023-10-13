import pandas as pd
import random
import sys

original_stdout = sys.stdout

nombre_archivo = "Trabajo_DFA.txt"

with open(nombre_archivo, 'w') as archivo:
    sys.stdout = archivo
    
    delta = pd.read_csv("Data.csv", index_col=0)
    alfabeto = ["x", "w", "z"]
    estado_inicial = "A"
    F = ["A", "B"]
  
    estados_dfa = dict()
    transiciones_dfa = []

    # Función para obtener el cierre-épsilon de un conjunto de estados
    def epsilon_closure(estados):
        closure = set(estados)
        stack = list(estados)

        while stack:
            estado = stack.pop()
            epsilon_transiciones = delta.loc[estado, "e"]
            
            if not pd.isna(epsilon_transiciones):
                siguientes = epsilon_transiciones.split(';') if isinstance(epsilon_transiciones, str) else [epsilon_transiciones]
                for siguiente in siguientes:
                    if siguiente not in closure:
                        closure.add(siguiente)
                        stack.append(siguiente)

        return closure

    # Función para obtener las transiciones del DFA
    def obtener_transiciones_dfa(estado_dfa, simbolo):
        nuevos_estados = set()

        for estado_nfa in estado_dfa:
            transicion = delta.loc[estado_nfa, simbolo]
            if not pd.isna(transicion):
                siguientes = transicion.split(';') if isinstance(transicion, str) else [transicion]
                nuevos_estados.update(siguientes)

        epsilon_closures = epsilon_closure(nuevos_estados)
        return epsilon_closures

    # Inicializar el DFA con el cierre-épsilon del estado inicial del NFA
    estado_inicial_dfa = epsilon_closure([estado_inicial])
    estados_dfa[tuple(estado_inicial_dfa)] = 'a'

    stack_dfa = [estado_inicial_dfa]

    while stack_dfa:
        estado_dfa_actual = stack_dfa.pop()

        for simbolo in alfabeto:
            nuevos_estados_dfa = obtener_transiciones_dfa(estado_dfa_actual, simbolo)
            if tuple(nuevos_estados_dfa) not in estados_dfa:
                letra = chr(ord(max(estados_dfa.values(), default='@')) + 1)
                estados_dfa[tuple(nuevos_estados_dfa)] = letra
                stack_dfa.append(tuple(nuevos_estados_dfa))
            transiciones_dfa.append((estados_dfa[tuple(estado_dfa_actual)], simbolo, estados_dfa[tuple(nuevos_estados_dfa)]))

    # Imprimir las transiciones del DFA
    for transicion in transiciones_dfa:
        print(transicion[0], "->", transicion[2], "[label =", transicion[1], "];")

    print("\n")
    print("------------------------------------------------------------")
    print("\n")

    contador_aprobados = 0
    F_dfa = set()

    for estado_nfa in F:
        estado_dfa = estados_dfa[tuple(epsilon_closure([estado_nfa]))]
        F_dfa.add(estado_dfa)

    for _ in range(500):
        x = list(estado_inicial_dfa)
        longitud = random.randint(10, 50)
        combinacion = ''.join([str(random.choice(alfabeto)) for _ in range(longitud)]) 
        print(">>", combinacion, " --> ", end="")
    
        for i in range(len(combinacion)):
            nuevos_estados = set()
            for estado in x:
                transicion = delta.loc[estado, combinacion[i]]
                if not pd.isna(transicion):
                    siguientes = transicion.split(';') if isinstance(transicion, str) else [transicion]
                    nuevos_estados.update(siguientes)

            epsilon_closures = epsilon_closure(nuevos_estados)
            x = list(epsilon_closures)
                
        if any(estado in F_dfa for estado in x):
            print("Aceptado")
            contador_aprobados = contador_aprobados + 1
        else:
            print("No Aceptado")


    print("La aceptación de los estados fue: ", (contador_aprobados*100)/500, "%")
        

sys.stdout = original_stdout

print("Resultado generado exportado en", nombre_archivo)

def generar_dot(estados, transiciones, nombre_archivo_dot, estado_inicial, estados_finales):
    with open(nombre_archivo_dot, 'w') as archivo_dot:
        archivo_dot.write("digraph DFA {\n")
        
        for estado, letra in estados.items():
            if estado == estado_inicial:
                archivo_dot.write(f'  {letra} [shape=circle, style=bold];\n')
            elif estado in estados_finales:
                archivo_dot.write(f'  {letra} [shape=doublecircle];\n')
            else:
                archivo_dot.write(f'  {letra} [shape=circle];\n')

        for transicion in transiciones:
            archivo_dot.write(f'  {transicion[0]} -> {transicion[2]} [label="{transicion[1]}"];\n')

        archivo_dot.write("}\n")

nombre_archivo_dot = "DFA.dot"
generar_dot(estados_dfa, transiciones_dfa, nombre_archivo_dot, 'a', F)
print("Archivo .dot generado en", nombre_archivo_dot)