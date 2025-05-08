import numpy as np

# Presupuesto disponible
presupuesto = 8

# Precios por página en cada copistería
precios = np.array([0.10, 0.12, 0.08])

# Calculamos cuántas páginas puede fotocopiar en cada copistería
paginas = np.floor(presupuesto / precios)

# Mostramos los resultados
print("*******************************************************************************************")
print(f"PRESUPUESTO:",presupuesto)
print("*******************************************************************************************")
# Información de cada copistería
print("Resumen por copistería:")
for i in range(len(precios)): #len devuelve cantidad
    print(f"Copistería {i + 1}: Precio S/ {precios[i]:.2f} por página → {int(paginas[i])} páginas posibles")

# Determinamos la mejor opción
mejor_opcion = np.argmax(paginas)
print(f"\n✅ La mejor opción es la Copistería {mejor_opcion + 1} con {int(paginas[mejor_opcion])} páginas.")
print("*******************************************************************************************")
