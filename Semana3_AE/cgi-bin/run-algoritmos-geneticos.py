# run-hill-climbing.py
import subprocess
import sys

print("Content-Type: text/plain\n")  # Importante para que el navegador lo interprete como texto

try:
    salida = subprocess.run(
        ['python', 'controllers/algoritmos-geneticos.py'],  # ajusta la ruta si es distinta
        capture_output=True,
        text=True
    )
    print(salida.stdout if salida.returncode == 0 else salida.stderr)
except Exception as e:
    print("Error al ejecutar el script:", e)
