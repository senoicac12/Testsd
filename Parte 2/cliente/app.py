from flask import Flask, request, render_template  

import grpc
import redis
import logging
from random import randint
import proto_message_pb2 as pb2_grpc
import proto_message_pb2_grpc as pb2
import json, time

#Variable global
global contador_cache
contador_cache = 0

global balanceador_entrecomillas
balanceador_entrecomillas = 0

app = Flask(__name__, template_folder='template')

# Configuración de Redis, hosts, limpieza de cache
redis_hosts = ["myredis1", "myredis2", "myredis3"]
redis_instances = [redis.Redis(host=host, port=6379, db=0) for host in redis_hosts]
[redis_instance.flushall() for redis_instance in redis_instances]


# Cliente para funcionalidad gRPC
class SearchClient(object):
    def __init__(self):

        #Stub que crea conexion entre el cliente y el backend(Servidor gRPC)
        self.stub = pb2.SearchStub(grpc.insecure_channel('{}:{}'.format('backend', '50051')))

    #Funcion utilizada para retornar la respuesta del servidor a un mensaje
    def get_url(self, message):
        message = pb2_grpc.Message(message=message)
        
        # Impresion del mensaje
        print(f'{message}') 
        # Llamada al procedimiento remoto GetServerResponse y retorno del resultado
        return self.stub.GetServerResponse(message)



@app.route('/')
def index(): 
    return render_template('index.html', contador = contador_cache)


@app.route('/search', methods=['GET'])
def search():
    # Avisamos que trabajaremos con las variables globales
    global contador_cache
    global balanceador_entrecomillas

    # Captura el tiempo de inicio de la operación
    mystart = time.time()

    # Crea una instancia de SearchClient
    client = SearchClient()

    # Realiza impresiones múltiples de la instancia client (útil para propósitos de depuración)
    print(client)

    # Obtiene el parámetro de consulta 'search' de la solicitud HTTP
    myquery = request.args['id']
    
    #Arreglo utilizado para mostrar lo solicitado en la consulta
    cache_search = [redis_instance.get(myquery) for redis_instance in redis_instances]

    # Verifica si no hay datos en la caché
    if all(value is None for value in cache_search):
        # Le pedimos la data al servidor
        data = client.get_url(message=myquery)

        if balanceador_entrecomillas == 3:
            balanceador_entrecomillas = 0
        # Almacena los datos en la instancia de Redis
        redis_instances[balanceador_entrecomillas].set(myquery, str(data))
        redis_selected = "Almacenado en el redis " + str(balanceador_entrecomillas+1)
        balanceador_entrecomillas += 1
        # Renderizamos el html con los datos obtenidos de PostgreSQL
        return render_template('index.html', mydata=data, procedencia="Datos sacados de PostgreSQL en: " + str(int((time.time() - mystart) * 1000)) + "ms", redis_selected=redis_selected, contador=contador_cache)
    else:
        # Incrementa el contador de caché
        contador_cache += 1
        # Itera sobre los datos almacenados en la caché
        for datos in cache_search:
            # Verifica si hay datos en la entrada actual de la caché
            if datos != None:
                # Crea un diccionario para almacenar los datos
                dicc = dict()
                dicc['Resultado'] = datos.decode("utf-8")
                # Renderiza la plantilla 'index.html' con los datos obtenidos de Redis
                return render_template('index.html', mydata=dicc['Resultado'], procedencia="Datos sacados de Redis en: " + str(int((time.time() - mystart) * 1000)) + "ms", contador=contador_cache)

# Ejecuta la aplicación Flask en modo de depuración si se ejecuta directamente este script
if __name__ == '__main__':
    app.run(debug=True)