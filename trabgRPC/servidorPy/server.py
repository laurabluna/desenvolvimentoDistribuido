import grpc
from concurrent import futures
import time
import sintomas_pb2
import sintomas_pb2_grpc
import joblib

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


def sintomas_para_vetor(lista_sintomas):
    return [1 if sint in lista_sintomas else 0 for sint in sintomas_base]

class SintomasServiceServicer(sintomas_pb2_grpc.SintomasServiceServicer):
    def Analisar(self, request, context):
        vetor = sintomas_para_vetor(request.sintomas)
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
    server.start
