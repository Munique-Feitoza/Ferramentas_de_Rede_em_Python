#!/usr/bin/env python3
"""
NetTools Suite - Banner Grabber & Fingerprinting (Standalone Modernizado)
Desenvolvido por Munique Feitoza
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.ui import Colors, print_banner, print_section, print_info, print_success, print_warning, print_error
from core.banner_grabber import grab_banner


def banner(ip: str, port: int):
    """Captura e analisa inteligentemente o banner e metadados de uma porta."""
    print_section(f"PROBE DE SERVIÇO EM {ip}:{port}")
    res = grab_banner(ip, port)

    print_success(f"Serviço Identificado: {Colors.BOLD}{Colors.GREEN}{res['detected_service']}{Colors.RESET}")
    
    if res.get("raw_banner"):
        print_info("Banner / Cabeçalho:")
        print(f"{Colors.CYAN}{res['raw_banner']}{Colors.RESET}")
    else:
        print_warning("Nenhum banner textual foi retornado pelo serviço no tempo limite.")

    if res.get("details"):
        print_info("Metadados & Criptografia:")
        for k, v in res["details"].items():
            print(f"  {Colors.PINK}▸ {k}:{Colors.RESET} {v}")


def main():
    print_banner()
    print_info("Banner Grabber Inteligente com Suporte a TLS/HTTP/SSH/FTP/SMTP")

    try:
        ip = input(f"{Colors.CYAN}Digite o endereço IP ou domínio: {Colors.RESET}").strip()
        if not ip:
            print_error("Endereço IP não informado.")
            return

        port_s = input(f"{Colors.CYAN}Digite o número da porta [ex: 80, 443, 22]: {Colors.RESET}").strip()
        if port_s.isdigit():
            banner(ip, int(port_s))
        else:
            print_error("Porta inválida.")
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada.")


if __name__ == "__main__":
    main()
