import matplotlib.pyplot as plt
import re

# Leer el archivo y extraer los valores relevantes
with open('data.txt', 'r') as file:
    lines = file.readlines()

# Expresión regular para encontrar los números seguidos de "ms"
ms_pattern = re.compile(r'(\d+)ms')

# Lista para almacenar los tiempos en milisegundos
times = []

# Procesar las líneas para extraer los tiempos
for line in lines:
    # Buscar todos los números seguidos de "ms" en la línea actual
    matches = ms_pattern.findall(line)
    # Si se encuentran coincidencias, agregar los tiempos a la lista
    if matches:
        for match in matches:
            times.append(int(match))

# Crear el gráfico
plt.hist(times, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Tiempo (ms)')
plt.ylabel('Frecuencia')
plt.title('Histograma de tiempos en milisegundos')
plt.grid(True)

# Mostrar el gráfico
plt.savefig('1_tiempos.png')
