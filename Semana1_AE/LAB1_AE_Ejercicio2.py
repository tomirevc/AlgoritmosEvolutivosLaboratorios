
#TORRES MILLA JOSÉ ANTONIO
#202114009
#ALGORITMOS EVOLUTIVOS

import pandas as pd

# Constante gobal
PRECIO_POR_HORA = 2.0
MAYOR = 6.0
MENOR = 6.0

def crear_dataframe():
    # Crea el DataFrame inicial con los datos
    datos = {
        'Estudiante': ['Ana', 'Luis', 'María', 'Juan', 'Carla'],
        'Horas_usadas': [3, 5, 2, 4, 1]
    }
    df = pd.DataFrame(datos)
    return df

def calcular_costos(df):
    #Agrega una columna con el costo total por estudiante
    df['Costo_total'] = df['Horas_usadas'] * PRECIO_POR_HORA
    return df

def mostrar_estadisticas(df):

    #realizar las operaciones
    estadisticas=df['Costo_total'].describe()
    promedio = df['Costo_total'].mean()
    estudiantes_mayor = df[df['Costo_total'] > MAYOR]['Estudiante'].tolist()
    estudiantes_menor = df[df['Costo_total'] < MENOR]['Estudiante'].tolist()

    #imprimir

    print("📋 DataFrame completo:")
    print(df)
    print("\n📈 Estadísticas de 'Costo_total':")
    print(estadisticas)
    print(f"\n📊 Resumen:")
    print(f"Gasto promedio: S/ {promedio:.2f}; ")
    print(f"Gastaron más de S/{MAYOR:.2f}: {', '.join(estudiantes_mayor)}.")
    print(f"Gastaron menos de S/{MENOR:.2f}: {', '.join(estudiantes_menor)}.")

def main():
    df = crear_dataframe()
    df = calcular_costos(df)
    mostrar_estadisticas(df)

# Ejecutar el flujo principal
if __name__ == "__main__":
    main()
