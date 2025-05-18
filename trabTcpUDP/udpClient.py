import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 6000

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"tem alertas UDP na porta {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode('utf-8'))

if __name__ == "__main__":
    udp_listener()
