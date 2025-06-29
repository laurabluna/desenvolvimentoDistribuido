import grpc
from concurrent import futures
import sintomas_pb2
import sintomas_pb2_grpc
import joblib
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load model
modelo = joblib.load("modelo.pkl")

sintomas_base = [
    "colica",
    "fadiga",
    "nausea",
    "sangramento",
    "dor_costas",
    "vomito",
    "dor_barriga",
    "dor_cabeca"
]

def sintomas(lista_sintomas):
    return [1 if sint in lista_sintomas else 0 for sint in sintomas_base]

class SintomasServiceServicer(sintomas_pb2_grpc.SintomasServiceServicer):
    def Analisar(self, request, context):
        vetor = sintomas(request.sintomas)
        diagnostico = modelo.predict([vetor])[0]

        if diagnostico == "Possível endometriose":
            recomendacao = "Procurar um especialista"
        elif diagnostico == "Monitorar evolução":
            recomendacao = "Acompanhar por 3 dias"
        elif diagnostico == "TPM moderada":
            recomendacao = "Repouso e hidratação"
        else:
            recomendacao = "Sem necessidade imediata"

        return sintomas_pb2.RespostaDiagnostico(
            diagnostico=diagnostico,
            recomendacao=recomendacao
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sintomas_pb2_grpc.add_SintomasServiceServicer_to_server(
        SintomasServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()  
    print("Servidor gRPC rodando na porta 50051...")
    try:
        while True:
            time.sleep(86400)  
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()  