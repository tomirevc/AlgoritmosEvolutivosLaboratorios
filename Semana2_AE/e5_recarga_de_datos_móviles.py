import numpy as np

# Datos de paquetes
gb = np.array([1, 2, 5, 10]) #GB
precios = np.array([5, 9, 20, 35]) #precios

# Calculamos el costo x cada GB
costo_por_gb = precios / gb

print("*******************************************************************************************")
# Mostramos
print("✅ Costo por GB de cada paquete:")
for i in range(len(gb)):
    print(f"Paquete de {gb[i]} GB → S/ {precios[i]:.2f} → Costo por GB: S/ {costo_por_gb[i]:.2f}")

# Paquete más económico 
mejor_indice = np.argmin(costo_por_gb)
min_costo = costo_por_gb.min()

print(f"\n✅ El paquete más económico es el de {gb[mejor_indice]} GB con S/ {min_costo:.2f} por GB.")
print("*******************************************************************************************")
