import grpc
from concurrent import futures
import proto_message_pb2 as pb2
import proto_message_pb2_grpc as pb2_grpc
from time import sleep
from routes import querys

class SearchService(pb2_grpc.SearchServicer):

    #Se acceden a los atributos de esta instancia
    #Argumento
    #Keywords Argumentos
    def __init__(self, *args, **kwargs):
        pass
    #Llega peticion del cliente, y luego crea la respuesta
    #El message en este caso seria el request
    def GetServerResponse(self, request, context):

        data = []
        response = []
        #Esto puede ser message = request.message
        message = request.message
        cursor.execute("SELECT * FROM data;")
        query_res = cursor.fetchall()
        for row in query_res:
            if message in row[1]:
                data.append(row)
                print(row)
        for i in data:
            result = dict()
            result['rowid'] = i[0]
            result['kepoi_name']= i[1]
            print(result)
            response.append(result)
        
        print(pb2.SearchResults(site=response))
        return pb2.SearchResults(site=response)

def serve():
    print("Server started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SearchServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    #Esperamos la conexion para tener con el servidor o algo asi
    #Y que se carguen los datos
    sleep(18)
    conn = querys.init_db()
    cursor = conn.cursor()
    serve()