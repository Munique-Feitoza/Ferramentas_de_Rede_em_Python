import socket

def main():
    # Cria o socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define o host e a porta do servidor
    host = socket.gethostname()  # Ou coloque o IP do servidor
    port = 3000

    try:
        # Tenta se conectar ao servidor
        client_socket.connect((host, port))
        print(f"Conectado ao servidor {host}:{port}")

        # Recebe a mensagem (até 1024 bytes)
        message = client_socket.recv(1024)
        print("Mensagem recebida do servidor:", message.decode('ascii'))

    except socket.error as e:
        # Captura qualquer erro relacionado a socket
        print(f"Erro de conexão: {e}")

    except Exception as e:
        # Captura qualquer outro tipo de erro
        print(f"Ocorreu um erro: {e}")

    finally:
        # Garante que o socket será fechado, mesmo se der erro
        client_socket.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()
