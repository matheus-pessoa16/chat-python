import socket
import threading

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 10000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)


def listen():
    global tcp
    while True:
        print(tcp.recv(1024))

t = threading.Thread(target =listen)
t.start()

print("Informe seu nome")
msg = input()
tcp.sendall(bytes(msg , 'utf-8'))
print (msg + '\n')

while msg != 'exit()':
    print(msg)
    tcp.sendall(bytes(msg , "utf-8"))
    msg = input()
tcp.close()
