#!/usr/bin/env python3
"""
NetTools Suite - Servidor TCP Multicliente & Inspecionador de Pacotes
Desenvolvido por Munique Feitoza
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.ui import Colors, print_banner, print_section, print_info, print_success, print_error
from core.tcp_tools import AsyncTCPServer


def main():
    print_banner()
    print_section("SERVIDOR TCP LISTENER & PACKET INSPECTOR")

    try:
        host = input(f"{Colors.CYAN}Host/Interface para escuta [Padrão: 0.0.0.0]: {Colors.RESET}").strip() or "0.0.0.0"
        port_s = input(f"{Colors.CYAN}Porta para escuta [Padrão: 3000]: {Colors.RESET}").strip() or "3000"
        
        if not port_s.isdigit():
            print_error("Porta inválida.")
            return

        port = int(port_s)
        server = AsyncTCPServer(host=host, port=port, echo_mode=True)
        
        try:
            asyncio.run(server.start())
        except KeyboardInterrupt:
            server.stop()
            print_info("\nServidor encerrado com sucesso.")

    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada.")


if __name__ == "__main__":
    main()
