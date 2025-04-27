import socket

def port_scanner(host, port):
    """Função para verificar se uma porta está aberta ou fechada."""
    try:
        # Cria o socket TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Define um tempo limite para a conexão
        s.settimeout(5)
        
        # Tenta se conectar
        result = s.connect_ex((host, port))

        if result == 0:
            print(f"Porta {port} está ABERTA no host {host}.")
        else:
            print(f"Porta {port} está FECHADA no host {host}.")

    except socket.gaierror:
        print("Erro: Nome do host não pôde ser resolvido.")

    except socket.error:
        print("Erro: Não foi possível conectar ao servidor.")

    finally:
        # Fecha o socket em qualquer situação
        s.close()

def main():
    print("=== Scanner de Porta ===")
    
    # Entrada do usuário
    host = input("Digite o endereço IP ou hostname a ser escaneado: ").strip()
    port = input("Digite o número da porta a ser escaneada: ").strip()

    # Verifica se o valor da porta é válido
    if port.isdigit():
        port = int(port)
        port_scanner(host, port)
    else:
        print("Número de porta inválido. Digite apenas números.")

if __name__ == "__main__":
    main()
