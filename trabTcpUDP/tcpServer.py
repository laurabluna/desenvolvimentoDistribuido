import socket
import threading

TCP_IP = '0.0.0.0'
TCP_PORT = 5000

UDP_IP = '<broadcast>'
UDP_PORT = 6000

def udp_broadcast(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    sock.close()

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            nome, mensagem, localizacao = data.split('|', 1)
            print(f"Pedido recebido de {nome}: {mensagem} : {localizacao}")

            alerta = f"🔔 SOS de {nome}: “{mensagem}”: {localizacao}"
            udp_broadcast(alerta)
            conn.sendall(b"Pedido recebido e alerta enviado.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_PORT))
    server.listen(5)
    print(f"Servidor TCP ouvindo na porta {TCP_PORT}...")

    while True:
        conn, addr = server.accept()
        print(f"Conexão de {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    tcp_server()
