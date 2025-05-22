# ------------------ ENUNCIADO DEL EJERCICIO ------------------
# DISEÑO DE MINI-RED NEURONAL PARA PREDICCIÓN DE MATRÍCULAS
# Contexto: Se desea predecir la categoría de matrícula (Alta, Media o Baja) usando una red neuronal.
# Para ello, se optimiza evolutivamente el número de capas (1-3), cantidad de neuronas por capa y learning rate.
# Se utiliza hill climbing local para afinar cada individuo.
# Métrica: accuracy. Límite de entrenamiento: 20 epochs.
# Dataset: Enrollments (excel), con columnas: Credits, Prev_GPA, Extracurricular_hours, Category.

# ------------------ OBJETIVO DEL CÓDIGO ------------------
# Crear una red neuronal simple y optimizar su arquitectura (capas, neuronas y tasa de aprendizaje)
# usando DEAP + hill climbing para clasificar la categoría de matrícula con la mayor exactitud posible.

# ------------------ CÓDIGO ------------------
# Importar librerías necesarias
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from deap import base, creator, tools
import random
import matplotlib.pyplot as plt

# Fijar semillas para reproducibilidad
random.seed(42)
np.random.seed(42)

# Leer dataset desde Excel
df = pd.read_excel('dataset.xlsx', sheet_name='Enrollments')

# Separar variables y etiquetas
X = df[['Credits', 'Prev_GPA', 'Extracurricular_hours']].values
y = df['Category'].values

# Codificar etiquetas como números
le = LabelEncoder()
y = le.fit_transform(y)

# Normalizar características
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# Función para construir y evaluar una red
def build_and_evaluate(layers, neurons, lr):
    model = Sequential()
    model.add(Dense(neurons, input_dim=X_train.shape[1], activation='relu'))
    for _ in range(layers - 1):
        model.add(Dense(neurons, activation='relu'))
    model.add(Dense(3, activation='softmax'))  # 3 clases

    model.compile(optimizer=Adam(learning_rate=lr),
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=20, verbose=0)
    y_pred = np.argmax(model.predict(X_test), axis=1)
    return accuracy_score(y_test, y_pred)

# Configurar DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Genotipo: [n_capas, n_neuronas, learning_rate]
toolbox.register("n_capas", random.randint, 1, 3)
toolbox.register("n_neuronas", random.randint, 4, 64)
toolbox.register("lr", random.uniform, 0.001, 0.1)
toolbox.register("individual", tools.initCycle, creator.Individual,
                    (toolbox.n_capas, toolbox.n_neuronas, toolbox.lr), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluar individuo
def evaluate(ind):
    capas, neuronas, lr = ind
    acc = build_and_evaluate(int(capas), int(neuronas), max(lr, 0.0001))
    return (acc,)

toolbox.register("evaluate", evaluate)

# Mutación simple y hill climbing (ajuste local)
def mutate(ind):
    if random.random() < 0.33:
        ind[0] = np.clip(ind[0] + random.choice([-1, 1]), 1, 3)
    if random.random() < 0.33:
        ind[1] = np.clip(ind[1] + random.randint(-4, 4), 4, 64)
    if random.random() < 0.33:
        ind[2] = max(0.0001, ind[2] + random.gauss(0, 0.005))
    return ind,

toolbox.register("mutate", mutate)
toolbox.register("select", tools.selBest)

# Inicializar población
pop = toolbox.population(n=10)
fitness_history = []

# Evaluar población inicial
for ind in pop:
    ind.fitness.values = toolbox.evaluate(ind)

# Ejecutar evolución por 10 generaciones
for gen in range(10):
    offspring = []
    for ind in pop:
        neighbor = creator.Individual(ind[:])
        mutate(neighbor)
        neighbor.fitness.values = toolbox.evaluate(neighbor)
        # Reemplazar si el vecino es mejor
        if neighbor.fitness.values[0] > ind.fitness.values[0]:
            offspring.append(neighbor)
        else:
            offspring.append(ind)
    pop[:] = offspring
    best = tools.selBest(pop, 1)[0]
    fitness_history.append(best.fitness.values[0])
    print(f"Generación {gen+1}: Mejor Accuracy = {best.fitness.values[0]:.4f}")

# Mostrar mejor solución final
mejor = tools.selBest(pop, 1)[0]
print("\n--- RESULTADOS ---")
print(f"Mejor arquitectura encontrada: {int(mejor[0])} capas, {int(mejor[1])} neuronas, learning rate = {mejor[2]:.5f}")
print(f"Accuracy final: {mejor.fitness.values[0]:.4f}")

# Mostrar curva de convergencia
plt.plot(fitness_history, marker='o')
plt.title("Curva de convergencia - Accuracy")
plt.xlabel("Generación")
plt.ylabel("Accuracy")
plt.grid()
plt.show()

# ------------------ INTERPRETACIÓN DEL RESULTADO ------------------
# El gráfico muestra cómo fue mejorando el rendimiento en cada generación, dependiendo de la cantidad
