
#TORRES MILLA JOSÉ ANTONIO
#202114009
#ALGORITMOS EVOLUTIVOS


import numpy as np

# Constantes
PRESUPUESTO = 10.0
cafeterias = ['A', 'B', 'C', 'D']
precios = np.array([2.50, 3.00, 1.75, 2.20])  # Precios por café en cada cafetería

def calcular_max_cafes(presupuesto, precios):
    #Calcula cuántos cafés puede comprar Jorge en cada cafetería
    return np.floor(presupuesto / precios)  # División vectorizada con redondeo hacia abajo

def encontrar_mejor_opcion(max_cafes, precios):
    #Encuentra la mejor cafetería en términos de cantidad de cafés
    max_cantidad = int(max_cafes.max())  # Mayor número de cafés
    mejor_indice = max_cafes.argmax()  # Índice de la mejor opción
    return max_cantidad, mejor_indice

def encontrar_menor_precio(precios):
    #Encuentra el precio mínimo y su índice
    precio_min = precios.min()
    indice_min = precios.argmin()
    return precio_min, indice_min

def mostrar_resultados(max_cafes, mejor_indice, max_cantidad, precio_min, indice_min):
    #Imprime el resumen de los resultados
    print("📊 Cantidad de cafés que Jorge puede comprar en cada cafetería:")
    for i, cantidad in enumerate(max_cafes.astype(int)):
        print(f"  - Cafetería {cafeterias[i]}: {cantidad} cafés")

    print(f"\n✅ Con S/ {PRESUPUESTO:.2f}, puede comprar como máximo {max_cantidad} cafés "
        f"en la cafetería {cafeterias[mejor_indice]}.")

    print(f"💰 El precio mínimo es S/ {precio_min:.2f}, en la cafetería {cafeterias[indice_min]}.")

# Flujo principal
max_cafes = calcular_max_cafes(PRESUPUESTO, precios)
max_cantidad, mejor_indice = encontrar_mejor_opcion(max_cafes, precios)
precio_min, indice_min = encontrar_menor_precio(precios)

mostrar_resultados(max_cafes, mejor_indice, max_cantidad, precio_min, indice_min)
