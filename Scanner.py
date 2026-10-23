#!/usr/bin/env python3
"""
NetTools Suite - Scanner de Redes Híbrido (Nmap + Native Async Engine)
Desenvolvido por Munique Feitoza
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.ui import Colors, print_banner, print_section, print_info, print_success, print_warning, print_error, print_table
from core.port_scanner import AsyncPortScanner, TOP_PORTS

# Tenta carregar python-nmap se disponível no ambiente
try:
    import nmap
    HAS_NMAP = True
except ImportError:
    HAS_NMAP = False


def scan_with_nmap(ip_addr: str, option: str):
    """Executa varredura via binário local do Nmap."""
    scanner = nmap.PortScanner()
    print_info(f"Nmap Engine versão: {scanner.nmap_version()}")

    if option == '1':
        print_info("Executando varredura TCP SYN (-v -sS na faixa 1-1024)...")
        scanner.scan(ip_addr, '1-1024', '-v -sS')
    elif option == '2':
        print_info("Executando varredura UDP (-v -sU na faixa 1-1024)...")
        scanner.scan(ip_addr, '1-1024', '-v -sU')
    elif option == '3':
        print_info("Executando varredura abrangente (-v -sS -sU -A -O na faixa 1-1024)...")
        scanner.scan(ip_addr, '1-1024', '-v -sS -sU -A -O')

    if ip_addr in scanner.all_hosts():
        print_success(f"Status do host {ip_addr}: {scanner[ip_addr].state()}")
        for proto in scanner[ip_addr].all_protocols():
            ports = list(scanner[ip_addr][proto].keys())
            print_info(f"Portas abertas [{proto.upper()}]: {ports}")
    else:
        print_warning("Nenhuma resposta recebida do host informado.")


def scan_with_native_engine(ip_addr: str):
    """Executa varredura usando o motor assíncrono nativo em Python puro."""
    print_info("Usando o Motor Assíncrono Nativo (Zero Dependências)...")
    scanner = AsyncPortScanner(ip_addr, timeout=1.2, concurrency=100)
    
    try:
        ip, host = scanner.resolve_target()
        print_info(f"Alvo: {ip} ({host})")
    except Exception as e:
        print_error(f"Erro na resolução: {e}")
        return

    ports = list(range(1, 1025))
    print_info(f"Iniciando escaneamento rápido de 1 a 1024 portas TCP...")
    open_ports = asyncio.run(scanner.run_scan(ports, show_progress=True))

    if not open_ports:
        print_warning("Nenhuma porta aberta detectada no intervalo 1-1024.")
    else:
        print_success(f"{len(open_ports)} porta(s) aberta(s) encontrada(s)!")
        headers = ["Porta", "Estado", "Serviço", "Latência"]
        rows = [[f"{p['port']}/TCP", p['state'], p['service'], f"{p['latency_ms']:.2f} ms"] for p in open_ports]
        print_table(headers, rows)


def main():
    print_banner()
    print_section("SCANNER DE REDES & RECONHECIMENTO")

    try:
        ip_addr = input(f"{Colors.CYAN}Digite o endereço IP ou domínio para escanear: {Colors.RESET}").strip()
        if not ip_addr:
            print_error("Endereço IP não fornecido.")
            return

        if HAS_NMAP:
            print("\nEscolha o tipo de varredura:")
            print(f"  {Colors.PINK}[1]{Colors.RESET} Varredura SYN ACK (TCP)")
            print(f"  {Colors.PINK}[2]{Colors.RESET} Varredura UDP")
            print(f"  {Colors.PINK}[3]{Colors.RESET} Varredura Abrangente (OS + Serviços)")
            print(f"  {Colors.PINK}[4]{Colors.RESET} Varredura Assíncrona Nativa (Python Puro)")
            resp = input(f"\n{Colors.PINK}Opção desejada [1-4]: {Colors.RESET}").strip()

            if resp in ('1', '2', '3'):
                try:
                    scan_with_nmap(ip_addr, resp)
                except Exception as e:
                    print_error(f"Erro na execução do Nmap ({e}). Alternando para o motor nativo...")
                    scan_with_native_engine(ip_addr)
            else:
                scan_with_native_engine(ip_addr)
        else:
            print_warning("Módulo 'python-nmap' não instalado no sistema. Operando no modo Nativo Assíncrono.")
            scan_with_native_engine(ip_addr)

    except (KeyboardInterrupt, EOFError):
        print("\nVarredura interrompida pelo usuário.")


if __name__ == "__main__":
    main()
