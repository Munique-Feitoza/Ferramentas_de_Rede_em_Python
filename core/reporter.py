"""
Módulo de Geração de Relatórios de Auditoria
Exporta resultados em JSON estruturado e relatórios profissionais em Markdown/HTML.
"""

import json
import time
from typing import Dict, Any, List

def export_json(data: Dict[str, Any], filepath: str) -> str:
    """Salva os dados do escaneamento em formato JSON estruturado."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath

def export_markdown_report(data: Dict[str, Any], filepath: str) -> str:
    """Gera um relatório profissional de segurança em Markdown."""
    target = data.get("target", "N/A")
    ip = data.get("ip", "N/A")
    duration = data.get("duration_seconds", 0)
    ports = data.get("ports", [])
    timestamp = data.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))

    lines = [
        f"# 🛡️ Relatório de Auditoria de Superfície de Rede",
        f"",
        f"**Alvo:** `{target}` ({ip})  ",
        f"**Data da Auditoria:** {timestamp}  ",
        f"**Duração:** {duration:.2f}s  ",
        f"**Total de Portas Abertas:** {len(ports)}  ",
        f"",
        f"---",
        f"",
        f"## 📊 Sumário de Portas e Serviços Identificados",
        f"",
        f"| Porta | Protocolo | Estado | Serviço Provável | Latência | Banner / Detalhes |",
        f"| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for p in ports:
        port_num = p.get("port")
        proto = p.get("protocol", "TCP")
        state = p.get("state", "ABERTA")
        service = p.get("service", "Desconhecido")
        lat = f"{p.get('latency_ms', 0):.2f} ms"
        banner = p.get("banner", "")
        # Sanitizar quebras de linha para a tabela markdown
        banner_clean = banner.replace("\n", " ").replace("|", "/")[:60] if banner else "-"
        lines.append(f"| `{port_num}` | {proto} | **{state}** | {service} | {lat} | `{banner_clean}` |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 🔍 Análise de Risco & Recomendações",
        f"",
    ])

    # Detecção heurística de riscos
    risk_found = False
    open_ports_set = {p.get("port") for p in ports}

    if 21 in open_ports_set:
        risk_found = True
        lines.append(f"- ⚠️ **Porta 21 (FTP):** Protocolo sem criptografia nativa. Recomenda-se migrar para SFTP (Porta 22) ou FTPS com TLS obrigatório.")
    if 23 in open_ports_set:
        risk_found = True
        lines.append(f"- 🚨 **Porta 23 (Telnet):** CRÍTICO. Telnet transmite credenciais em texto puro. Deve ser desabilitado imediatamente em favor do SSH.")
    if 80 in open_ports_set and 443 not in open_ports_set:
        risk_found = True
        lines.append(f"- ⚠️ **Porta 80 (HTTP) sem HTTPS:** O serviço HTTP está exposto sem o correspondente HTTPS configurado. Configure certificados SSL/TLS.")
    if 3389 in open_ports_set:
        risk_found = True
        lines.append(f"- ⚠️ **Porta 3389 (RDP):** Acesso remoto de terminal exposto. Garanta MFA, restrição por IP de origem ou uso exclusivo via VPN.")
    if 445 in open_ports_set or 139 in open_ports_set:
        risk_found = True
        lines.append(f"- 🚨 **Portas SMB (139/445):** Compartilhamento de arquivos do Windows exposto diretamente na rede. Alto vetor de propagação de worms/ransomware.")

    if not risk_found:
        lines.append(f"- ✅ Nenhuma vulnerabilidade trivial de portas legadas inseguras detectada na amostra.")

    lines.extend([
        f"",
        f"---",
        f"*Relatório gerado automaticamente pelo **NetTools Cyber Suite 2.0** (Desenvolvido por Munique Feitoza).*",
        f""
    ])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    return filepath
