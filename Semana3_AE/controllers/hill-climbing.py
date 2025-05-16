'''
EJEMPLO BÁSICO:
Un estudiante quiere escoger 2 snacks de entre 5 disponibles para consumir en clase.
Cada snack tiene una cantidad de calorías y una puntuación de satisfacción (del 1 al 10).
El objetivo es maximizar la satisfacción sin consumir más de 400 calorías en total.

Aplicaremos Hill Climbing para encontrar la mejor combinación posible.
'''

import numpy as np
import pandas as pd

# Datos: 5 snacks
snacks = pd.DataFrame({
    'Snack': ['Manzana', 'Galletas', 'Barra de cereal', 'Yogurt', 'Nueces'],
    'Calorias': [95, 300, 150, 120, 200],
    'Satisfaccion': [7, 6, 8, 7, 9]
})
print("--------------------------------------")
print("DATAFRAME [INICIO] Snacks:")
print(snacks)

# Evaluar una solución: array binario de 5 elementos (elegidos o no)
def evaluar(sol, df):
    total_cal = np.sum(df['Calorias'][sol == 1])
    if total_cal > 400 or np.sum(sol) != 2:
        return -1  # inválida
    return np.sum(df['Satisfaccion'][sol == 1])

# Hill climbing
def hill_climbing(df):
    n = len(df)
    sol_actual = np.zeros(n, dtype=int)
    sol_actual[np.random.choice(n, size=2, replace=False)] = 1

    mejor_valor = evaluar(sol_actual, df)
    for _ in range(100):
        idx_1 = np.where(sol_actual == 1)[0]
        idx_0 = np.where(sol_actual == 0)[0]

        i_fuera = np.random.choice(idx_1)
        i_dentro = np.random.choice(idx_0)

        vecina = sol_actual.copy()
        vecina[i_fuera] = 0
        vecina[i_dentro] = 1

        valor_vecina = evaluar(vecina, df)
        if valor_vecina > mejor_valor:
            sol_actual = vecina
            mejor_valor = valor_vecina

    return sol_actual, mejor_valor

# Ejecutar
sol, val = hill_climbing(snacks)
print("--------------------------------------")
print("DATAFRAME [RESPUESTA] Snacks elegidos:")
print(snacks[sol == 1])
print("--------------------------------------")
print("MEJOR SATISFACCION HALLADA:", val)
print("--------------------------------------")

