#!/usr/bin/env python3
"""
NetTools Suite - Cliente TCP Interativo & Medidor de RTT
Desenvolvido por Munique Feitoza
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.ui import Colors, print_banner, print_section, print_info, print_error
from core.tcp_tools import TCPClientTester


def main():
    print_banner()
    print_section("CLIENTE TCP INTERATIVO & RTT TESTER")

    try:
        host = input(f"{Colors.CYAN}Host/IP do servidor [Padrão: 127.0.0.1]: {Colors.RESET}").strip() or "127.0.0.1"
        port_s = input(f"{Colors.CYAN}Porta [Padrão: 3000]: {Colors.RESET}").strip() or "3000"

        if not port_s.isdigit():
            print_error("Porta inválida.")
            return

        port = int(port_s)
        client = TCPClientTester(host, port)

        print("\nEscolha a operação:")
        print(f"  {Colors.PINK}[1]{Colors.RESET} Sessão Interativa de Envio/Recebimento (com Dump Hexadecimal)")
        print(f"  {Colors.PINK}[2]{Colors.RESET} Teste de Desempenho e Medição de Latência (RTT & Jitter)")
        
        op = input(f"\n{Colors.PINK}Opção [1-2]: {Colors.RESET}").strip()

        if op == "2":
            client.test_latency(count=5)
        else:
            client.interactive_session()

    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada.")


if __name__ == "__main__":
    main()
