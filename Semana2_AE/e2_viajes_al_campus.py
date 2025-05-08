import numpy as np

# Presupuesto de Carlos
presupuesto = 15

# Precios por viaje de cada medio de transporte: [bus, combi, tren]
precios = np.array([2.5, 3.0, 1.8])

# Calculamos cuántos viajes puede hacer con cada medio
viajes = np.floor(presupuesto / precios)

# Nombres de los medios de transporte
medios = ['Bus', 'Combi', 'Tren']

# Resultado
print("*******************************************************************************************")
print(f"PRESUPUESTO:",presupuesto)
print("*******************************************************************************************")

# Mostramos el detalle de cada medio
print("Resumen por medio de transporte:")
for i in range(len(precios)):
    print(f"{medios[i]}: Precio S/ {precios[i]:.2f} → {int(viajes[i])} viajes posibles")

# Encontramos el máximo número de viajes
max_viajes = viajes.max()

# Buscamos el índice del medio que ofrece ese máximo
mejor_indice = np.argmax(viajes)
mejor_medio = medios[mejor_indice]

# Mostramos la mejor opción
print(f"\n✅ El mejor medio es el {mejor_medio} con {int(max_viajes)} viajes.")
print("*******************************************************************************************")
