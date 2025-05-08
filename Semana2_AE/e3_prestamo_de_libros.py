import pandas as pd

# Datos de estudiantes y días que prestaron libros
datos = {
    'Estudiante': ['Rosa', 'David', 'Elena', 'Mario', 'Paula'],
    'Días_prestamo': [7, 10, 5, 12, 3]
}

# Creamos un DataFrame con los datos
df = pd.DataFrame(datos)

# Resultado
print("*******************************************************************************************")

# Mostramos el DataFrame completo
print("✅ Registro de préstamos de libros:")
print(df)

# Calculamos estadísticas
print("\n✅ Estadísticas de días de préstamo:")
print(df['Días_prestamo'].describe())

# Filtramos a los que prestaron más de 8 días
print("\n✅ Estudiantes que prestaron más de 8 días:")
filtro = df[df['Días_prestamo'] > 8]
print(filtro)

print("*******************************************************************************************")
