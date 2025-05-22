import socket
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5000

UDP_IP = '0.0.0.0'
UDP_PORT = 6000

mensagens_comuns = [
    "Preciso de ajuda urgente!",
    "Estou me sentindo insegura.",
    "Alguém está me seguindo.",
    "Estou sentindo cólicas",
    "Chame a polícia, por favor!",
]

def mostrar_mensagens():
    print("Escolha uma mensagem comum ou digite uma mensagem personalizada:")
    for i, msg in enumerate(mensagens_comuns, start=1):
        print(f"{i}. {msg}")
    print("0. Digitar mensagem personalizada")

def enviar_alerta(nome, mensagem, localizacao):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_IP, TCP_PORT))

    client.sendall(f"{nome}|{mensagem}|{localizacao}".encode('utf-8'))

    resposta = client.recv(1024)
    print("Resposta do servidor TCP:", resposta.decode())
    client.close()

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Esperando alertas UDP na porta {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        print("Mensagem UDP recebida:", data.decode('utf-8'))

if __name__ == "__main__":
    nome = input("Seu nome: ")
    
    mostrar_mensagens()
    escolha = input("Digite o número da mensagem que quer enviar: ")

    if escolha == "0":
        mensagem = input("Digite sua mensagem personalizada: ")
    elif escolha.isdigit() and 1 <= int(escolha) <= len(mensagens_comuns):
        mensagem = mensagens_comuns[int(escolha) - 1]
    else:
        print("Escolha inválida! Usando mensagem padrão.")
        mensagem = mensagens_comuns[0]

    localizacao = input("Localização: ")

    thread_udp = threading.Thread(target=udp_listener, daemon=True)
    thread_udp.start()

    enviar_alerta(nome, mensagem, localizacao)

    print("Pressione Ctrl+C para sair...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Encerrando cliente.")
