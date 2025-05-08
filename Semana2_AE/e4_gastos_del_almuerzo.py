import pandas as pd


# Lista de gastos diarios
datos = {
    'Días': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
    'Gasto': [4.0, 3.5, 5.0, 4.2, 3.8]
}

# Creamos un DataFrame
df = pd.DataFrame(datos)

# Resultado
print("*******************************************************************************************")
# Mostramos el registro
print("Registro de gastos diarios:")
print(df)

# Calculamos el total y el promedio
total = df['Gasto'].sum()
promedio = df['Gasto'].mean()

print(f"\n✅ Gasto total semanal: S/ {total:.2f}")
print(f"✅ Gasto promedio diario: S/ {promedio:.2f}")

# Filtramos donde el gasto fue mayor que el promedio
dias_mayores = df[df['Gasto'] > promedio]

print("✅ Días con gasto superior al promedio:")
print(dias_mayores)

print("*******************************************************************************************")
