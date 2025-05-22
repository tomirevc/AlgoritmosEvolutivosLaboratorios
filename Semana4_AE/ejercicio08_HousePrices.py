# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Ajuste de hiper-parámetros en regresión Ridge sobre dataset HousePrices.
# Se desea encontrar el mejor valor de α que minimice el error cuadrático medio (RMSE).
# Se usará una población de 20 individuos y DEAP para implementar hill climbing
# con mutación gaussiana y sin cruce. Se selecciona siempre el mejor individuo (greedy).
# Se reporta el valor óptimo de α y la curva de convergencia del RMSE.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Usar DEAP para encontrar el valor de α en Ridge que dé el menor RMSE posible.

# ------------------ CÓDIGO ------------------

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from deap import base, creator, tools

# Fijar semillas para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer los datos
df = pd.read_excel("dataset.xlsx", sheet_name="HousePrices")
X = df[["Rooms", "Area_m2"]].values
y = df["Price_Soles"].values

# Dividir entre entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Mostrar vista previa y datos relevantes
print("Vista previa del dataset:")
print(df.head())
print(f"\nTotal de datos: {len(df)}")
print("Entrenando modelo Ridge para encontrar el mejor α...")

# Crear clases de DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0.1, 10.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluar el modelo con un valor dado de alpha
def eval_ridge(individual):
    alpha = individual[0]
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return (rmse,)

toolbox.register("evaluate", eval_ridge)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=1.0)
toolbox.register("select", tools.selBest)

# Crear población
pop = toolbox.population(n=20)
rmse_values = []

# Ejecutar algoritmo hill climbing por 50 generaciones
N_GEN = 50
for gen in range(N_GEN):
    # Evaluar población
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Guardar mejor RMSE
    best_rmse = tools.selBest(pop, 1)[0].fitness.values[0]
    rmse_values.append(best_rmse)

    # Tomar el mejor y generar mutaciones
    best_ind = tools.selBest(pop, 1)[0]
    pop = [toolbox.clone(best_ind) for _ in range(20)]
    for ind in pop:
        toolbox.mutate(ind)
        # Corregir alpha si quedó fuera de rango
        ind[0] = max(0.0, min(ind[0], 10.0))
        del ind.fitness.values

# Mostrar mejor resultado
best_alpha = tools.selBest(pop, 1)[0][0]
print(f"\nMejor valor de α encontrado: {best_alpha:.4f}")
print(f"RMSE mínimo obtenido: {rmse_values[-1]:.4f}")

# Graficar convergencia
plt.plot(rmse_values, label="RMSE")
plt.xlabel("Generación")
plt.ylabel("RMSE")
plt.title("Curva de convergencia del RMSE")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# El mejor α encontrado es el valor que hace que el modelo tenga menor error (RMSE).
# Esto ayuda a afinar el modelo Ridge para que haga predicciones más precisas.
