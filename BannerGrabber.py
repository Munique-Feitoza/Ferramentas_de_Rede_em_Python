import socket

def banner(ip, port):
    """Função para capturar o banner do serviço rodando em determinada porta."""
    try:
        # Cria o socket
        s = socket.socket()
        
        # Define o tempo limite para resposta
        s.settimeout(5)

        # Conecta ao IP e porta fornecidos
        s.connect((ip, int(port)))

        # Recebe até 1024 bytes da resposta do servidor
        banner_data = s.recv(1024)
        
        # Exibe o banner de forma limpa
        print("Banner capturado:", banner_data.decode().strip())

    except socket.timeout:
        print("Tempo de conexão esgotado (timeout).")

    except socket.error as e:
        print(f"Erro de socket: {e}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        # Garante o fechamento do socket
        s.close()

def main():
    print("=== Banner Grabber ===")
    
    ip = input("Digite o endereço IP para escanear: ").strip()
    port = input("Digite o número da porta para escanear: ").strip()

    banner(ip, port)

if __name__ == "__main__":
    main()
