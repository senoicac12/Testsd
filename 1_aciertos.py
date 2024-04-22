import matplotlib.pyplot as plt

# Leer el archivo y extraer los valores relevantes
with open('data.txt', 'r') as file:
    lines = file.readlines()

# Procesar las líneas para extraer los valores relevantes
# En este ejemplo, supondremos que las líneas tienen un formato específico y que queremos extraer valores específicos

# Por ejemplo, si cada línea tiene el formato "Contador aciertos caché: <contador>", donde <contador> es el valor relevante
# Podríamos extraer esos valores de la siguiente manera:
contador_values = []
for line in lines:
    if "Contador aciertos caché:" in line:
        parts = line.split(":")
        contador_values.append(int(parts[1].strip()))

# Crear el gráfico
plt.plot(contador_values)
plt.xlabel('Número de solicitud')
plt.ylabel('Valor del contador')
plt.title('Gráfico del contador de aciertos de caché')
plt.grid(True)

# Guardar el gráfico en un archivo
plt.savefig('1_aciertos.png')
