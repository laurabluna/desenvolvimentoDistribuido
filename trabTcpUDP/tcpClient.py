import socket

TCP_IP = '127.0.0.1' 
TCP_PORT = 5000

def enviar_alerta(nome, mensagem, localizacao):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_IP, TCP_PORT))

    client.sendall(f"{nome}|{mensagem}|{localizacao}".encode('utf-8'))

    resposta = client.recv(1024)
    print("resposta do servidor:", resposta.decode())
    client.close()

if __name__ == "__main__":
    nome = input("Seu nome: ")
    mensagem = input("Mensagem de ajuda: ")
    localizacao = input("Localização")
    enviar_alerta(nome, mensagem, localizacao)
