#Crearemos una funcion que reciba un archivo y genere otro

with open('/tmp/cumulative.csv', 'r') as file:
    lines = file.readlines()

with open('/home/jb/Desktop/memi/Tarea1-SD/T1_P1/db/bdd1.sql', 'w') as file:
    cantidad = 1
    for i, line in enumerate(lines):
        columns = line.strip().split(',')
        nombre_cliente = columns[0].strip()
        nombre_producto = columns[2].strip()
        file.write("INSERT INTO data(rowid, kepoi_name)")
        file.write(f" VALUES({nombre_cliente}, '{nombre_producto}');\n")
        cantidad += 1
    