# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# Pesado de reglas anti-spam → Se desea evolucionar 6 pesos (1 umbral + 5 features) que
# maximicen el F1-score de clasificación de correos como spam.
# Cada individuo es una lista de 6 floats y realiza un paso de hill climbing local
# luego de mutar. Se reportan los mejores pesos encontrados y se grafica el F1 por generación.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Encontrar los mejores valores de 6 parámetros (1 umbral y 5 pesos para features)
# que permitan clasificar correos como spam con el mejor F1-score posible.

# ------------------ CÓDIGO ------------------
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from deap import base, creator, tools

# Fijar semillas para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer el dataset
df = pd.read_excel("dataset.xlsx", sheet_name="Emails")
X = df[["Feature1", "Feature2", "Feature3", "Feature4", "Feature5"]].values
y = df["Spam"].values

# Separar en entrenamiento y validación
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3)

# Mostrar datos relevantes
print("Vista previa del dataset:")
print(df.head())
print(f"\nTotal de datos: {len(df)}")
print("Iniciando optimización de pesos anti-spam...\n")

# Crear clases en DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # F1-score a maximizar
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Cada individuo tiene 6 floats: 1 umbral y 5 pesos de features
toolbox.register("attr_float", random.uniform, -3.0, 3.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de evaluación: aplica pesos y umbral, calcula F1
def eval_spam(individual):
    threshold = individual[0]
    weights = np.array(individual[1:])
    scores = np.dot(X_val, weights)
    predictions = (scores > threshold).astype(int)
    return (f1_score(y_val, predictions),)

toolbox.register("evaluate", eval_spam)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=1.0)
toolbox.register("select", tools.selBest)

# Crear población inicial
pop = toolbox.population(n=20)
f1_scores = []

# Ejecutar por 40 generaciones
N_GEN = 40
for gen in range(N_GEN):
    # Evaluar cada individuo
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)
    
    # Guardar mejor F1 de la generación
    best = tools.selBest(pop, 1)[0]
    f1_scores.append(best.fitness.values[0])

    # Nueva población: clonar al mejor y aplicar mutación y hill climbing local
    new_pop = []
    for ind in pop:
        clone = toolbox.clone(ind)
        toolbox.mutate(clone)
        # Hill climbing local: probar pequeñas variaciones y quedarse con la mejor
        neighbors = []
        for i in range(len(clone)):
            neighbor = toolbox.clone(clone)
            neighbor[i] += random.gauss(0, 0.1)
            neighbors.append(neighbor)
        neighbors.append(clone)
        # Evaluar todos los vecinos
        for n in neighbors:
            n.fitness.values = toolbox.evaluate(n)
        # Escoger el mejor
        best_neighbor = tools.selBest(neighbors, 1)[0]
        new_pop.append(toolbox.clone(best_neighbor))
    
    pop = new_pop

# Resultado final
best_final = tools.selBest(pop, 1)[0]
print("Mejores pesos encontrados:")
print(f"  Umbral: {best_final[0]:.4f}")
for i, w in enumerate(best_final[1:], start=1):
    print(f"  Peso Feature{i}: {w:.4f}")
print(f"\nF1-score final: {best_final.fitness.values[0]:.4f}")

# Graficar curva de F1 por generación
plt.plot(f1_scores, label="F1-score")
plt.xlabel("Generación")
plt.ylabel("F1-score")
plt.title("Curva de F1-score por generación")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# El algoritmo encontró los valores óptimos de pesos y umbral para detectar spam.
# Un mayor F1-score indica un mejor balance entre precisión y recall.
