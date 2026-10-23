"""
Módulo de Banner Grabbing Inteligente e Inspeção de Serviços
Envia probes sob medida para HTTP/HTTPS, SSH, FTP, SMTP e TLS com extração de certificados e headers.
"""

import socket
import ssl
from typing import Dict, Any, Optional

def grab_banner(host: str, port: int, timeout: float = 3.0) -> Dict[str, Any]:
    """Captura e analisa inteligentemente o banner e metadados de uma porta."""
    result: Dict[str, Any] = {
        "host": host,
        "port": port,
        "raw_banner": "",
        "detected_service": "Desconhecido",
        "details": {}
    }

    # Probes especializados
    if port in (443, 8443):
        return _grab_tls_banner(host, port, timeout, result)
    elif port in (80, 8080, 8000, 8888):
        return _grab_http_banner(host, port, timeout, result)
    elif port == 22:
        return _grab_ssh_banner(host, port, timeout, result)
    elif port in (21,):
        return _grab_ftp_banner(host, port, timeout, result)
    elif port in (25, 587):
        return _grab_smtp_banner(host, port, timeout, result)
    else:
        return _grab_generic_banner(host, port, timeout, result)

def _grab_http_banner(host: str, port: int, timeout: float, res: Dict) -> Dict:
    res["detected_service"] = "HTTP Web Server"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        
        probe = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: NetTools-Cyber/2.0\r\nConnection: close\r\n\r\n"
        s.sendall(probe.encode("ascii"))
        
        response = s.recv(2048).decode("utf-8", errors="ignore")
        s.close()

        lines = response.split("\r\n")
        res["raw_banner"] = lines[0] if lines else response
        
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()
        
        server = headers.get("server", "Não divulgado")
        powered_by = headers.get("x-powered-by", "")
        res["details"]["Server"] = server
        if powered_by:
            res["details"]["Powered-By"] = powered_by
        res["details"]["Status-Line"] = lines[0] if lines else "N/A"
    except Exception as e:
        res["raw_banner"] = f"Erro ao coletar banner HTTP: {e}"
    return res

def _grab_tls_banner(host: str, port: int, timeout: float, res: Dict) -> Dict:
    res["detected_service"] = "HTTPS / TLS Service"
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE  # Permite inspecionar self-signed
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        ssock = ctx.wrap_socket(sock, server_hostname=host)
        ssock.connect((host, port))

        cipher = ssock.cipher()
        version = ssock.version()
        res["details"]["TLS Version"] = version
        res["details"]["Cipher Suite"] = cipher[0] if cipher else "N/A"

        # Tenta obter banner HTTP via TLS
        probe = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: NetTools-Cyber/2.0\r\nConnection: close\r\n\r\n"
        ssock.sendall(probe.encode("ascii"))
        http_data = ssock.recv(2048).decode("utf-8", errors="ignore")
        ssock.close()

        lines = http_data.split("\r\n")
        res["raw_banner"] = lines[0] if lines else f"{version} ({cipher[0]})"
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                if k.strip().lower() in ("server", "x-powered-by"):
                    res["details"][k.strip()] = v.strip()
    except Exception as e:
        res["raw_banner"] = f"Erro no handshake TLS: {e}"
    return res

def _grab_ssh_banner(host: str, port: int, timeout: float, res: Dict) -> Dict:
    res["detected_service"] = "SSH (Secure Shell)"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        banner_data = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        res["raw_banner"] = banner_data
        res["details"]["Identificação SSH"] = banner_data
    except Exception as e:
        res["raw_banner"] = f"Erro SSH: {e}"
    return res

def _grab_ftp_banner(host: str, port: int, timeout: float, res: Dict) -> Dict:
    res["detected_service"] = "FTP (File Transfer)"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        banner_data = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        res["raw_banner"] = banner_data
        res["details"]["Banner FTP"] = banner_data
    except Exception as e:
        res["raw_banner"] = f"Erro FTP: {e}"
    return res

def _grab_smtp_banner(host: str, port: int, timeout: float, res: Dict) -> Dict:
    res["detected_service"] = "SMTP (Mail Transfer)"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        init_banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        res["raw_banner"] = init_banner
        
        # Envia EHLO para descobrir capacidades suportadas
        s.sendall(b"EHLO audit.local\r\n")
        ehlo_resp = s.recv(2048).decode("utf-8", errors="ignore").strip()
        s.close()

        res["details"]["Init"] = init_banner
        capabilities = [l for l in ehlo_resp.split("\n") if "250" in l]
        if capabilities:
            res["details"]["Capabilities"] = f"{len(capabilities)} extensões detectadas"
    except Exception as e:
        res["raw_banner"] = f"Erro SMTP: {e}"
    return res

def _grab_generic_banner(host: str, port: int, timeout: float, res: Dict) -> Dict:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        
        # Tenta receber passivamente primeiro
        s.settimeout(1.5)
        try:
            data = s.recv(1024)
        except socket.timeout:
            # Se não mandar nada, envia um newline probe
            s.sendall(b"\r\n\r\n")
            s.settimeout(timeout)
            try:
                data = s.recv(1024)
            except socket.timeout:
                data = b""

        s.close()
        text = data.decode("utf-8", errors="ignore").strip()
        res["raw_banner"] = text if text else "Porta aberta, mas nenhum banner retornado."
    except Exception as e:
        res["raw_banner"] = f"Conexão aceita (sem resposta de banner legível): {e}"
    return res
