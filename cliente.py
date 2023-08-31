import socket

def main():
    host = '127.0.0.1'
    port = 65535

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            command = input("Digite o comando (d/h/dh) ou '/sair' para sair: ")
            client_socket.send(command.encode())

            if command == '/sair':
                break

            response = client_socket.recv(1024).decode()
            print("Resposta do servidor:", response)
    except KeyboardInterrupt:
        print("\nEncerrando o cliente.")

    client_socket.close()

if __name__ == "__main__":
    main()