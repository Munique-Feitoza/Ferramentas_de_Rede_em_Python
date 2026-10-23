"""
Módulo de Scanner de Portas Assíncrono de Alta Performance
Executa varreduras concorrentes via asyncio com identificação de serviços conhecidos e medição de latência.
"""

import asyncio
import socket
import time
from typing import List, Dict, Optional, Tuple
from core.ui import render_progress_bar

# Mapeamento expandido de serviços de rede mais comuns
KNOWN_SERVICES: Dict[int, str] = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP Server",
    68: "DHCP Client",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    135: "MS-RPC",
    137: "NetBIOS-NS",
    138: "NetBIOS-DGM",
    139: "NetBIOS-SSN",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP-Trap",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB / Active Directory",
    465: "SMTPS",
    587: "SMTP Submission",
    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",
    1433: "Microsoft SQL Server",
    1521: "Oracle DB",
    2049: "NFS",
    2375: "Docker Daemon (Insecure)",
    2376: "Docker Daemon (TLS)",
    3306: "MySQL / MariaDB",
    3389: "RDP (Remote Desktop)",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    6443: "Kubernetes API Server",
    8000: "HTTP Dev Server",
    8080: "HTTP Proxy / Tomcat",
    8443: "HTTPS Alternate",
    9000: "SonarQube / Portainer",
    9090: "Prometheus / Cockpit",
    9200: "Elasticsearch",
    11211: "Memcached",
    27017: "MongoDB"
}

TOP_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 6379, 8080, 8443, 27017]

class AsyncPortScanner:
    def __init__(self, target: str, timeout: float = 1.2, concurrency: int = 150):
        self.target_input = target
        self.timeout = timeout
        self.concurrency = concurrency
        self.ip: Optional[str] = None
        self.hostname: Optional[str] = None

    def resolve_target(self) -> Tuple[str, str]:
        """Resolve o hostname para IP e obtém o Reverse DNS."""
        try:
            self.ip = socket.gethostbyname(self.target_input)
            try:
                self.hostname = socket.gethostbyaddr(self.ip)[0]
            except Exception:
                self.hostname = self.target_input
            return self.ip, self.hostname
        except socket.gaierror:
            raise ValueError(f"Não foi possível resolver o host: '{self.target_input}'")

    async def scan_single_port(self, port: int, sem: asyncio.Semaphore) -> Optional[Dict]:
        """Verifica uma única porta assincronamente com medição de latência."""
        async with sem:
            start_time = time.perf_counter()
            try:
                # Tenta abrir conexão TCP direta
                conn = asyncio.open_connection(self.ip, port)
                reader, writer = await asyncio.wait_for(conn, timeout=self.timeout)
                elapsed_ms = (time.perf_counter() - start_time) * 1000

                writer.close()
                await writer.wait_closed()

                service = KNOWN_SERVICES.get(port, "Desconhecido")
                return {
                    "port": port,
                    "state": "ABERTA",
                    "service": service,
                    "latency_ms": round(elapsed_ms, 2)
                }
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return None

    async def run_scan(self, ports: List[int], show_progress: bool = True) -> List[Dict]:
        """Executa a varredura concorrente sobre a lista de portas."""
        if not self.ip:
            self.resolve_target()

        sem = asyncio.Semaphore(self.concurrency)
        total = len(ports)
        completed = 0
        open_ports = []

        async def worker(p):
            nonlocal completed
            res = await self.scan_single_port(p, sem)
            completed += 1
            if show_progress and (completed % 5 == 0 or completed == total):
                render_progress_bar(completed, total)
            return res

        tasks = [worker(p) for p in ports]
        results = await asyncio.gather(*tasks)

        for r in results:
            if r is not None:
                open_ports.append(r)

        # Ordena portas abertas numericamente
        open_ports.sort(key=lambda x: x["port"])
        return open_ports

def parse_port_range(ports_str: str) -> List[int]:
    """Interpreta formatos de porta como: '80', '80,443,8080', '1-1024', 'top'."""
    ports_str = ports_str.strip().lower()
    if ports_str == "top":
        return TOP_PORTS
    
    ports = set()
    parts = ports_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            sub = part.split("-")
            if len(sub) == 2 and sub[0].isdigit() and sub[1].isdigit():
                start, end = int(sub[0]), int(sub[1])
                start, end = max(1, start), min(65535, end)
                if start <= end:
                    ports.update(range(start, end + 1))
        elif part.isdigit():
            p = int(part)
            if 1 <= p <= 65535:
                ports.add(p)
                
    if not ports:
        return TOP_PORTS
    return sorted(list(ports))
