import nmap

def main():
    # Cria uma instância do scanner Nmap
    scanner = nmap.PortScanner()

    print("Bem-vindo à ferramenta de automação de varredura com Nmap!")
    print("<----------------------------------------------------------->")

    # Solicita o IP do alvo
    ip_addr = input("Digite o endereço IP para escanear: ").strip()
    print(f"O endereço IP informado é: {ip_addr}")

    # Escolha do tipo de varredura
    print("\nEscolha o tipo de varredura que deseja realizar:")
    print("1. Varredura SYN ACK (TCP)")
    print("2. Varredura UDP")
    print("3. Varredura Abrangente")
    
    resp = input("\nDigite o número da opção desejada: ").strip()

    print(f"\nVocê selecionou a opção: {resp}\n")

    try:
        if resp == '1':
            print("Versão do Nmap:", scanner.nmap_version())
            scanner.scan(ip_addr, '1-1024', '-v -sS')  # Varredura TCP SYN
            exibir_resultados(scanner, ip_addr)

        elif resp == '2':
            print("Versão do Nmap:", scanner.nmap_version())
            scanner.scan(ip_addr, '1-1024', '-v -sU')  # Varredura UDP
            exibir_resultados(scanner, ip_addr)

        elif resp == '3':
            print("Versão do Nmap:", scanner.nmap_version())
            scanner.scan(ip_addr, '1-1024', '-v -sS -sU -A -O')  # Varredura completa
            exibir_resultados(scanner, ip_addr)

        else:
            print("Opção inválida. Por favor, tente novamente.")

    except nmap.PortScannerError as e:
        print(f"Erro ao executar o Nmap: {e}")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def exibir_resultados(scanner, ip_addr):
    """Função auxiliar para exibir os resultados da varredura."""
    print("Informações da varredura:", scanner.scaninfo())
    print("Status do IP:", scanner[ip_addr].state())
    print("Protocolos detectados:", scanner[ip_addr].all_protocols())

    for protocolo in scanner[ip_addr].all_protocols():
        print(f"Portas abertas ({protocolo}):", scanner[ip_addr][protocolo].keys())

if __name__ == "__main__":
    main()
