import socket

def main():
    # Cria um socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define o host e a porta
    host = socket.gethostname()  # Pode ser o IP da máquina também
    port = 3000

    try:
        # Faz o bind do socket para o host e a porta especificados
        server_socket.bind((host, port))
        print(f"Servidor iniciado em {host}:{port}")

        # Coloca o servidor em modo de escuta (pode aceitar até 3 conexões pendentes)
        server_socket.listen(3)
        print("Aguardando conexões...")

        while True:
            # Aceita uma nova conexão
            client_socket, address = server_socket.accept()
            print(f"Conexão recebida de: {address}")

            # Mensagem a ser enviada para o cliente
            message = "Hello World!"
            client_socket.send(message.encode('ascii'))

            # Fecha a conexão com o cliente
            client_socket.close()

    except socket.error as e:
        # Captura erros relacionados a socket
        print(f"Erro de socket: {e}")

    except Exception as e:
        # Captura qualquer outro tipo de erro
        print(f"Ocorreu um erro: {e}")

    finally:
        # Garante que o servidor será fechado corretamente
        server_socket.close()
        print("Servidor encerrado.")

if __name__ == "__main__":
    main()
