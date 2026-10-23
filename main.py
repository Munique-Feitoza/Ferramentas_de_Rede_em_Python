#!/usr/bin/env python3
"""
NetTools Suite 2.0 - Cyberpunk Network Recon & Security Toolkit
Desenvolvido por Munique Feitoza

Módulo principal de orquestração com suporte a CLI completo e TUI Interativa.
"""

import sys
import os
import argparse
import asyncio
import time
from typing import List, Dict, Any

# Garante importação limpa dos módulos internos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ui import (
    Colors, BANNER_ASCII, print_banner, print_section, 
    print_status, print_success, print_info, print_warning, 
    print_error, print_table
)
from core.port_scanner import AsyncPortScanner, parse_port_range, TOP_PORTS
from core.banner_grabber import grab_banner
from core.tcp_tools import AsyncTCPServer, TCPClientTester, format_hex_dump
from core.reporter import export_json, export_markdown_report


async def run_scan_workflow(target: str, ports_str: str, timeout: float = 1.2, concurrency: int = 150, output_file: str = None):
    """Executa a rotina completa de escaneamento de portas assíncrono."""
    print_section("AUDITORIA DE PORTAS TCP (ASYNC ENGINE)")
    scanner = AsyncPortScanner(target, timeout=timeout, concurrency=concurrency)
    
    try:
        ip, hostname = scanner.resolve_target()
        print_info(f"Alvo Alocado: {Colors.BOLD}{target}{Colors.RESET} -> IP: {Colors.PINK}{ip}{Colors.RESET} (Host: {hostname})")
    except Exception as e:
        print_error(f"Falha na resolução DNS: {e}")
        return

    ports = parse_port_range(ports_str)
    print_info(f"Portas no escopo: {Colors.CYAN}{len(ports)}{Colors.RESET} | Concorrência: {Colors.CYAN}{concurrency}{Colors.RESET} conexões simultâneas")

    start_time = time.perf_counter()
    open_ports = await scanner.run_scan(ports, show_progress=True)
    duration = time.perf_counter() - start_time

    print(f"\n{Colors.GREEN}✓ Varredura concluída em {duration:.2f} segundos.{Colors.RESET}")

    if not open_ports:
        print_warning(f"Nenhuma porta aberta detectada nas {len(ports)} portas analisadas.")
    else:
        print_success(f"{len(open_ports)} porta(s) aberta(s) encontrada(s)!")
        headers = ["Porta", "Estado", "Serviço Provável", "Latência"]
        rows = [
            [f"{p['port']}/TCP", p['state'], p['service'], f"{p['latency_ms']:.2f} ms"]
            for p in open_ports
        ]
        print_table(headers, rows)

    if output_file:
        report_data = {
            "target": target,
            "ip": ip,
            "duration_seconds": duration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ports": open_ports
        }
        if output_file.endswith(".json"):
            export_json(report_data, output_file)
            print_success(f"Relatório JSON salvo em: {Colors.BOLD}{output_file}{Colors.RESET}")
        else:
            export_markdown_report(report_data, output_file)
            print_success(f"Relatório Markdown salvo em: {Colors.BOLD}{output_file}{Colors.RESET}")

    return open_ports


async def run_audit_workflow(target: str, ports_str: str = "top", timeout: float = 1.5, concurrency: int = 150, output_file: str = None):
    """Executa auditoria completa: varredura de portas + banner grabbing em cada porta aberta + relatório."""
    print_section("AUDITORIA COMPLETA & FINGERPRINTING DE SERVIÇOS")
    scanner = AsyncPortScanner(target, timeout=timeout, concurrency=concurrency)
    
    try:
        ip, hostname = scanner.resolve_target()
        print_info(f"Alvo Alocado: {Colors.BOLD}{target}{Colors.RESET} -> IP: {Colors.PINK}{ip}{Colors.RESET}")
    except Exception as e:
        print_error(f"Falha na resolução DNS: {e}")
        return

    ports = parse_port_range(ports_str)
    print_info(f"Iniciando escaneamento de {len(ports)} portas...")
    
    start_time = time.perf_counter()
    open_ports = await scanner.run_scan(ports, show_progress=True)
    
    print_info(f"Inspecionando banners e assinaturas nas {len(open_ports)} portas abertas...")
    for p in open_ports:
        port_num = p["port"]
        banner_info = grab_banner(ip, port_num, timeout=timeout + 1.0)
        p["banner"] = banner_info.get("raw_banner", "")
        p["service"] = banner_info.get("detected_service", p["service"])
        p["details"] = banner_info.get("details", {})

    duration = time.perf_counter() - start_time
    print_success(f"Auditoria finalizada em {duration:.2f}s!")

    headers = ["Porta", "Serviço Identificado", "Banner / Assinatura"]
    rows = []
    for p in open_ports:
        b = p.get("banner", "")
        # Encurtar para visualização na tabela do terminal
        b_short = (b[:45] + "..") if len(b) > 45 else (b or "-")
        rows.append([f"{p['port']}/TCP", p["service"], b_short])
    print_table(headers, rows)

    out_path = output_file or f"relatorio_{target.replace('/', '_')}_{int(time.time())}.md"
    report_data = {
        "target": target,
        "ip": ip,
        "duration_seconds": duration,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ports": open_ports
    }
    if out_path.endswith(".json"):
        export_json(report_data, out_path)
    else:
        export_markdown_report(report_data, out_path)
        
    print_success(f"Relatório gerado com sucesso em: {Colors.BOLD}{out_path}{Colors.RESET}")


def run_banner_workflow(host: str, port: int):
    """Executa banner grabber individual."""
    print_section(f"BANNER GRABBER: {host}:{port}")
    res = grab_banner(host, port)
    
    print_info(f"Serviço Detectado: {Colors.BOLD}{Colors.GREEN}{res['detected_service']}{Colors.RESET}")
    if res.get("raw_banner"):
        print_info("Banner / Cabeçalho Retornado:")
        print(f"{Colors.CYAN}{res['raw_banner']}{Colors.RESET}")
    
    if res.get("details"):
        print_info("Metadados & Parâmetros Criptográficos:")
        for k, v in res["details"].items():
            print(f"  {Colors.PINK}▸ {k}:{Colors.RESET} {v}")


def interactive_menu():
    """Menu interativo no terminal com navegação visual."""
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print_banner()
        print(f"{Colors.PINK}  [1]{Colors.RESET} ⚡ Scanner de Portas Assíncrono Ultra-Rápido")
        print(f"{Colors.PINK}  [2]{Colors.RESET} 🔍 Banner Grabbing & Inspeção SSL/TLS")
        print(f"{Colors.PINK}  [3]{Colors.RESET} 🛡️ Auditoria Completa de Alvo (Portas + Banner + Relatório)")
        print(f"{Colors.PINK}  [4]{Colors.RESET} 📡 Servidor TCP Listener / Hex Packet Dump")
        print(f"{Colors.PINK}  [5]{Colors.RESET} 📶 Cliente TCP Interativo & Teste de Latência/RTT")
        print(f"{Colors.PINK}  [0]{Colors.RESET} 🚪 Sair")
        print(f"\n{Colors.CYAN}─────────────────────────────────────────────────────────────────{Colors.RESET}")
        
        try:
            choice = input(f"{Colors.BOLD}{Colors.PINK}opção ❯ {Colors.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSaindo...")
            break

        if choice == "1":
            target = input(f"{Colors.CYAN}Informe o Host ou IP alvo: {Colors.RESET}").strip()
            if target:
                ports = input(f"{Colors.CYAN}Portas [ex: 'top', '1-1000', '80,443' | Padrão: top]: {Colors.RESET}").strip() or "top"
                asyncio.run(run_scan_workflow(target, ports))
                input(f"\n{Colors.GRAY}Pressione Enter para voltar ao menu...{Colors.RESET}")
        elif choice == "2":
            host = input(f"{Colors.CYAN}Informe o Host ou IP: {Colors.RESET}").strip()
            port_s = input(f"{Colors.CYAN}Informe a Porta: {Colors.RESET}").strip()
            if host and port_s.isdigit():
                run_banner_workflow(host, int(port_s))
                input(f"\n{Colors.GRAY}Pressione Enter para voltar ao menu...{Colors.RESET}")
        elif choice == "3":
            target = input(f"{Colors.CYAN}Informe o Host ou IP alvo: {Colors.RESET}").strip()
            if target:
                ports = input(f"{Colors.CYAN}Portas [Padrão: top]: {Colors.RESET}").strip() or "top"
                asyncio.run(run_audit_workflow(target, ports))
                input(f"\n{Colors.GRAY}Pressione Enter para voltar ao menu...{Colors.RESET}")
        elif choice == "4":
            port_s = input(f"{Colors.CYAN}Porta para escutar [Padrão: 4444]: {Colors.RESET}").strip() or "4444"
            if port_s.isdigit():
                server = AsyncTCPServer(host="0.0.0.0", port=int(port_s))
                try:
                    asyncio.run(server.start())
                except KeyboardInterrupt:
                    server.stop()
                input(f"\n{Colors.GRAY}Pressione Enter para voltar ao menu...{Colors.RESET}")
        elif choice == "5":
            host = input(f"{Colors.CYAN}Informe o Host ou IP: {Colors.RESET}").strip()
            port_s = input(f"{Colors.CYAN}Informe a Porta: {Colors.RESET}").strip()
            if host and port_s.isdigit():
                client = TCPClientTester(host, int(port_s))
                print("\n[1] Medir Latência (RTT)  |  [2] Sessão Interativa de Mensagens")
                sub = input("Escolha: ").strip()
                if sub == "1":
                    client.test_latency(count=5)
                else:
                    client.interactive_session()
                input(f"\n{Colors.GRAY}Pressione Enter para voltar ao menu...{Colors.RESET}")
        elif choice == "0":
            print_info("Encerrando NetTools Cyber Suite. Até breve!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="NetTools Cyber Recon Toolkit v2.0 - Desenvolvido por Munique Feitoza",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-s", "--scan", metavar="TARGET", help="Executa varredura de portas TCP no alvo")
    parser.add_argument("-a", "--audit", metavar="TARGET", help="Executa auditoria completa (varredura + banners + relatório)")
    parser.add_argument("-p", "--ports", default="top", help="Portas a auditar (ex: '80', '1-1024', 'top', '22,80,443')")
    parser.add_argument("-b", "--banner", nargs=2, metavar=("HOST", "PORT"), help="Captura e analisa banner da porta específica")
    parser.add_argument("--server", action="store_true", help="Inicia servidor TCP listener com hex packet dump")
    parser.add_argument("--client", nargs=2, metavar=("HOST", "PORT"), help="Inicia cliente TCP interativo")
    parser.add_argument("--rtt", nargs=2, metavar=("HOST", "PORT"), help="Testa latência e jitter de conexão TCP")
    parser.add_argument("-o", "--output", metavar="FILE", help="Exporta relatório para Markdown (.md) ou JSON (.json)")
    parser.add_argument("-c", "--concurrency", type=int, default=150, help="Número de conexões assíncronas paralelas (padrão: 150)")
    parser.add_argument("-t", "--timeout", type=float, default=1.2, help="Timeout em segundos para conexões (padrão: 1.2)")
    parser.add_argument("--port", type=int, default=4444, help="Porta para o modo servidor (padrão: 4444)")

    args = parser.parse_args()

    # Se nenhum argumento foi passado, abre o menu interativo
    if len(sys.argv) == 1:
        interactive_menu()
        return

    print_banner()

    if args.scan:
        asyncio.run(run_scan_workflow(
            target=args.scan,
            ports_str=args.ports,
            timeout=args.timeout,
            concurrency=args.concurrency,
            output_file=args.output
        ))
    elif args.audit:
        asyncio.run(run_audit_workflow(
            target=args.audit,
            ports_str=args.ports,
            timeout=args.timeout,
            concurrency=args.concurrency,
            output_file=args.output
        ))
    elif args.banner:
        run_banner_workflow(args.banner[0], int(args.banner[1]))
    elif args.server:
        server = AsyncTCPServer(host="0.0.0.0", port=args.port)
        try:
            asyncio.run(server.start())
        except KeyboardInterrupt:
            server.stop()
    elif args.client:
        client = TCPClientTester(args.client[0], int(args.client[1]), timeout=args.timeout)
        client.interactive_session()
    elif args.rtt:
        client = TCPClientTester(args.rtt[0], int(args.rtt[1]), timeout=args.timeout)
        client.test_latency()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
