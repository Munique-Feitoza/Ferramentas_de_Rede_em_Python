"""
Módulo de Ferramentas TCP/UDP Avançadas e Desempenho de Rede
Inclui Servidor TCP/UDP Multicliente Assíncrono com Dump Hexadecimal e Métricas de Throughput,
e Cliente Interativo com Medição de RTT/Latência.
"""

import asyncio
import socket
import time
import binascii
from typing import Optional, Tuple
from core.ui import (
    Colors, print_section, print_info, print_success, 
    print_warning, print_error, print_status
)

def format_hex_dump(data: bytes, width: int = 16) -> str:
    """Gera um dump legível padrão hexadecimal + ASCII (estilo Wireshark/xxd)."""
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        # Preenchimento se for menor que a largura
        hex_part = hex_part.ljust(width * 3)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{Colors.GRAY}{i:04x}{Colors.RESET}  {Colors.CYAN}{hex_part}{Colors.RESET} |{Colors.GREEN}{ascii_part}{Colors.RESET}|")
    return "\n".join(lines)


class AsyncTCPServer:
    """Servidor TCP assíncrono multiconexão com monitoramento de tráfego."""

    def __init__(self, host: str = "0.0.0.0", port: int = 4444, echo_mode: bool = True):
        self.host = host
        self.port = port
        self.echo_mode = echo_mode
        self.total_bytes_received = 0
        self.total_connections = 0
        self.server: Optional[asyncio.Server] = None
        self._running = False

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_addr = writer.get_extra_info("peername")
        self.total_connections += 1
        conn_id = self.total_connections
        
        print_status(f"CONN #{conn_id}", f"Cliente conectado: {Colors.PINK}{client_addr[0]}:{client_addr[1]}{Colors.RESET}", Colors.GREEN)

        try:
            while self._running:
                data = await reader.read(4096)
                if not data:
                    break
                
                self.total_bytes_received += len(data)
                now_str = time.strftime("%H:%M:%S")
                print(f"\n{Colors.PURPLE}[{now_str}] Pacote recebido de {client_addr[0]}:{client_addr[1]} ({len(data)} bytes):{Colors.RESET}")
                print(format_hex_dump(data))

                if self.echo_mode:
                    writer.write(data)
                    await writer.drain()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print_error(f"Erro na conexão #{conn_id}: {e}")
        finally:
            print_status(f"DISCONN #{conn_id}", f"Cliente desconectado: {client_addr[0]}:{client_addr[1]}", Colors.YELLOW)
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    async def start(self):
        self._running = True
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addrs = ", ".join(str(sock.getsockname()) for sock in self.server.sockets)
        print_success(f"Servidor TCP ativo ouvindo em {Colors.BOLD}{self.host}:{self.port}{Colors.RESET} [{addrs}]")
        print_info(f"Modo Echo: {'ATIVO' if self.echo_mode else 'INATIVO'} | Pressione Ctrl+C para encerrar.")

        async with self.server:
            try:
                await self.server.serve_forever()
            except asyncio.CancelledError:
                pass

    def stop(self):
        self._running = False
        if self.server:
            self.server.close()
            print_info(f"Servidor encerrado. Total de conexões: {self.total_connections} | Bytes: {self.total_bytes_received}")


class TCPClientTester:
    """Cliente TCP para auditoria de endpoints, teste de RTT e envio interativo."""

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def test_latency(self, count: int = 4) -> dict:
        """Executa múltiplos handshakes TCP para medir o RTT de rede real."""
        latencies = []
        print_info(f"Medindo latência de conexão TCP com {Colors.CYAN}{self.host}:{self.port}{Colors.RESET} ({count} pacotes)...")

        for i in range(count):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            start = time.perf_counter()
            try:
                s.connect((self.host, self.port))
                rtt = (time.perf_counter() - start) * 1000.0
                latencies.append(rtt)
                print(f"  {Colors.GREEN}✓{Colors.RESET} Probe {i+1}: RTT = {Colors.BOLD}{rtt:.2f} ms{Colors.RESET}")
                s.close()
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} Probe {i+1}: Falha ({e})")
            time.sleep(0.15)

        if not latencies:
            return {"status": "unreachable", "loss": 100.0}

        avg_lat = sum(latencies) / len(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)
        jitter = max_lat - min_lat

        return {
            "status": "success",
            "sent": count,
            "received": len(latencies),
            "loss_pct": ((count - len(latencies)) / count) * 100.0,
            "min_ms": round(min_lat, 2),
            "avg_ms": round(avg_lat, 2),
            "max_ms": round(max_lat, 2),
            "jitter_ms": round(jitter, 2)
        }

    def interactive_session(self):
        """Abre sessão interativa enviando payloads customizados e exibindo resposta."""
        print_info(f"Conectando a {self.host}:{self.port}...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.host, self.port))
            print_success(f"Conectado com sucesso a {self.host}:{self.port}!")
            print_info("Digite sua mensagem para enviar (ou ':q' para desconectar):\n")

            while True:
                msg = input(f"{Colors.PINK}nettools> {Colors.RESET}")
                if msg.strip() in (":q", "exit", "quit"):
                    break
                if not msg:
                    continue

                payload = (msg + "\n").encode("utf-8")
                start = time.perf_counter()
                s.sendall(payload)

                try:
                    resp = s.recv(4096)
                    rtt = (time.perf_counter() - start) * 1000.0
                    if not resp:
                        print_warning("Servidor fechou a conexão.")
                        break
                    print(f"{Colors.GRAY}[Recebido {len(resp)} bytes em {rtt:.2f}ms]{Colors.RESET}")
                    print(format_hex_dump(resp))
                except socket.timeout:
                    print_warning("Timeout aguardando resposta.")
        except Exception as e:
            print_error(f"Erro na conexão: {e}")
        finally:
            try:
                s.close()
            except Exception:
                pass
            print_info("Sessão finalizada.")
