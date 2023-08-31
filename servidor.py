import socket       # Importa o módulo socket, que é usado para criar e gerenciar sockets de rede.
import threading    # Importa o módulo threading, que é usado para trabalhar com threads em Python, permitindo que o servidor lide com várias conexões simultâneas.
import datetime     # Importa o módulo datetime, que é usado para manipular datas e horas.

def handle_client(client_socket):
    while True:

        # É uma função que lida com as solicitações do cliente. O valor 1024 é o tamanho máximo dos dados a serem recebidos.
        request = client_socket.recv(1024).decode()

        if request == 'd':
            response = "Data:" + datetime.datetime.now().strftime("%d-%m-%Y")
        elif request == 'h':
            response = "Hora: " + datetime.datetime.now().strftime("%H:%M:%S")
        elif request == 'dh':
            response = "Dia/Hora: " + datetime.datetime.now().strftime("%d-%m-%Y / %H:%M:%S")
        elif request == '/sair':
            response = "Saindo..."

            # Envia a resposta gerada de volta ao cliente após a manipulação da solicitação.
            client_socket.send(response.encode())
            break
        else:
            response = "Opção inválida"

        client_socket.send(response.encode())
    
    # Fecha o socket do cliente após o loop ser encerrado.
    client_socket.close()
    
def main():
    host = '127.0.0.1'
    port = 65535

    # Cria um novo socket TCP/IP.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Liga o socket a um endereço e porta específicos.
    server_socket.bind((host, port))
    # Coloca o socket em modo de escuta, permitindo que ele aceite até 5 conexões pendentes.
    server_socket.listen(5)

    print(f"Servidor escutando em {host}:{port}")

    while True:
        # Aguarda até que uma conexão seja estabelecida e retorna o socket do cliente e o endereço do cliente.
        client_socket, client_address = server_socket.accept() 
        print(f"Conexão recebida de {client_address[0]}:{client_address[1]}")

        # Cria uma nova thread para lidar com o cliente. 
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        # Inicia a thread para lidar com o cliente.
        client_thread.start()

if __name__ == "__main__":
    main()