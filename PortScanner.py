#!/usr/bin/env python3
"""
NetTools Suite - Port Scanner (Legado & Standalone Modernizado)
Desenvolvido por Munique Feitoza
"""

import sys
import os
import socket
import time

# Permite execução direta na raiz ou como módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from core.ui import Colors, print_banner, print_info, print_success, print_error, print_table
    from core.port_scanner import KNOWN_SERVICES
except ImportError:
    # Fallback caso executado isolado
    class Colors:
        RESET = ""
        BOLD = ""
        CYAN = ""
        GREEN = ""
        RED = ""
        PINK = ""
    def print_banner(): pass
    def print_info(m): print(f"[*] {m}")
    def print_success(m): print(f"[+] {m}")
    def print_error(m): print(f"[-] {m}")
    def print_table(h, r):
        for row in r:
            print(" | ".join(row))
    KNOWN_SERVICES = {}


def port_scanner(host: str, port: int) -> bool:
    """Verifica se uma porta específica está aberta ou fechada com medição de latência."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    
    start_time = time.perf_counter()
    try:
        result = s.connect_ex((host, port))
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        service = KNOWN_SERVICES.get(port, "Desconhecido")

        if result == 0:
            print_success(f"Porta {Colors.BOLD}{port}/TCP{Colors.RESET} está {Colors.GREEN}ABERTA{Colors.RESET} no host {host} ({service}) - RTT: {elapsed_ms:.2f} ms")
            return True
        else:
            print_error(f"Porta {port}/TCP está FECHADA no host {host}.")
            return False

    except socket.gaierror:
        print_error(f"Erro: O hostname '{host}' não pôde ser resolvido via DNS.")
        return False
    except socket.error as e:
        print_error(f"Erro de conexão com o socket: {e}")
        return False
    finally:
        s.close()


def main():
    print_banner()
    print_info("Scanner de Portas Individual TCP")
    
    try:
        host = input(f"{Colors.CYAN}Digite o IP ou hostname do alvo: {Colors.RESET}").strip()
        if not host:
            print_error("Alvo não informado.")
            return

        port_input = input(f"{Colors.CYAN}Digite o número da porta a ser escaneada: {Colors.RESET}").strip()
        if port_input.isdigit():
            port = int(port_input)
            port_scanner(host, port)
        else:
            print_error("Número de porta inválido. Digite apenas números inteiros entre 1 e 65535.")
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")


if __name__ == "__main__":
    main()
