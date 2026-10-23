# 🛡️ NetTools Cyber Recon Toolkit v2.0
> **Suite de Auditoria de Redes, Fingerprinting de Serviços e Reconhecimento Cibersegurança em Python Puro.**  
> *Desenvolvido por [Munique Feitoza](https://github.com/Munique-Feitoza).*

---

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue?style=for-the-badge)](LICENSE)
[![Zero-Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Stdlib)-brightgreen?style=for-the-badge)]()
[![Cyberpunk TUI](https://img.shields.io/badge/Interface-Cyberpunk%20TUI-9cf?style=for-the-badge)]()

O **NetTools Suite** é uma plataforma modular de auditoria de superfície de ataque, diagnóstico de conectividade e análise forense de portas desenvolvida com foco em **altíssimo desempenho, concorrência assíncrona e zero dependências externas obrigatórias**.

Projetado tanto para operadores de segurança defensiva quanto para administradores de infraestrutura que necessitam de um canivete suíço imediato em qualquer terminal Linux/macOS/Windows sem depender de gerenciadores de pacotes externos.

---

## ⚡ Principais Capacidades

- 🚀 **Motor Assíncrono Concorrente (`asyncio`)**: Varre milhares de portas TCP por segundo utilizando semáforos de concorrência adaptativos e cálculo de latência (RTT) por porta.
- 🔍 **Banner Grabbing & Service Fingerprinting Multiprocolo**:
  - Probes sob medida para **HTTP/HTTPS** (análise de cabeçalhos `Server`, `X-Powered-By`), **SSH**, **FTP**, e **SMTP**.
  - **Inspeção Criptográfica SSL/TLS**: Extrai automaticamente a versão de cifras (`TLSv1.3`), emissor do certificado (CA), `CommonName` (CN), SAN e validade temporal.
- 📡 **Servidor TCP Listener & Packet Inspector**:
  - Capturador multiconexão assíncrono com **Hexadecimal Dump** padrão Wireshark/xxd em tempo real.
- 📶 **Cliente TCP & RTT Tester**:
  - Medição de latência real de conexão (mínima, média, máxima, jitter e perda de pacotes) + terminal interativo de envio de dados.
- 📊 **Gerador de Relatórios Profissionais de Segurança**:
  - Exporta relatórios completos de auditoria e superfície de ataque em **Markdown estruturado** ou **JSON** com heurísticas automáticas de risco (ex: FTP/Telnet sem criptografia, SMB exposto).
- 🎨 **Interface Cyberpunk Terminal (TUI)**:
  - Cores ANSI 24-bit TrueColor, tabelas dinâmicas, barras de progresso nativas e banners ASCII.

---

## 🏗️ Arquitetura do Repositório

```text
Ferramentas_de_Rede_em_Python/
├── core/                         # Motor de Alta Performance Modular
│   ├── __init__.py               # Metadados e versão do Toolkit
│   ├── ui.py                     # Motor ANSI TrueColor, Banners, Tabelas e Barras de Progresso
│   ├── port_scanner.py           # Scanner TCP assíncrono e catálogo de portas conhecidas
│   ├── banner_grabber.py         # Probes inteligentes (HTTP, TLS, SSH, FTP, SMTP)
│   ├── tcp_tools.py              # Listener TCP assíncrono multicliente & Testador de RTT
│   └── reporter.py               # Exportador para Markdown e JSON com análise de risco
├── main.py                       # Orquestrador com Menu Interativo TUI e CLI completa
├── PortScanner.py                # Wrapper moderno para varredura de porta específica
├── Scanner.py                    # Scanner híbrido (Nmap + Native Async Engine)
├── BannerGrabber.py              # Wrapper moderno para banner grabbing individual
├── TCP Server.py                 # Servidor de escuta TCP com packet dump
├── TCP Client.py                 # Cliente TCP interativo com medição de latência
├── requirements.txt              # Zero dependências obrigatórias
├── LICENSE                       # Licença GPL-2.0
└── README.md                     # Documentação completa do projeto
```

---

## 🚀 Como Executar

### 1. Clonar o Repositório
```bash
git clone https://github.com/Munique-Feitoza/Ferramentas_de_Rede_em_Python.git
cd Ferramentas_de_Rede_em_Python
```

### 2. Modo Interativo (TUI Cyberpunk)
Basta executar o orquestrador principal sem argumentos para abrir o painel de controle interativo:
```bash
python3 main.py
```

### 3. Linha de Comando (CLI Avançada)

#### 🔹 Varredura Rápida de Portas Assíncrona
```bash
# Varre as principais portas TCP mais comuns (Top Ports)
python3 main.py --scan 192.168.1.1

# Varre um intervalo customizado com 250 conexões simultâneas
python3 main.py --scan 10.0.0.1 --ports 1-1024 --concurrency 250

# Varre portas específicas
python3 main.py --scan target.com --ports 21,22,80,443,3306,8080
```

#### 🔹 Auditoria Completa com Fingerprint e Relatório
```bash
# Executa varredura, captura banners e salva relatório em Markdown
python3 main.py --audit 192.168.1.50 --ports top -o auditoria_servidor.md

# Salva em JSON estruturado para ingestão em pipelines de SIEM / SecOps
python3 main.py --audit 192.168.1.50 --ports 80,443,8080 -o scan.json
```

#### 🔹 Banner Grabbing & Inspeção SSL/TLS
```bash
# Identifica versão de servidor web ou certificado SSL
python3 main.py --banner google.com 443

# Identifica versão de daemon SSH
python3 main.py --banner 192.168.1.1 22
```

#### 🔹 Servidor Listener TCP com Hex Dump
```bash
# Ouve na porta 4444 exibindo todos os pacotes recebidos em hexadecimal e ASCII
python3 main.py --server --port 4444
```

#### 🔹 Teste de Latência de Rede (RTT & Jitter)
```bash
python3 main.py --rtt 1.1.1.1 53
```

---

## 📸 Exemplo de Relatório Gerado (Markdown)

```markdown
# 🛡️ Relatório de Auditoria de Superfície de Rede
**Alvo:** `192.168.1.1` | **Data:** 2026-10-23 12:00:00

| Porta | Protocolo | Estado | Serviço Provável | Latência | Banner / Detalhes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `22` | TCP | **ABERTA** | SSH | 1.84 ms | `SSH-2.0-OpenSSH_9.6p1` |
| `80` | TCP | **ABERTA** | HTTP | 2.15 ms | `nginx/1.24.0` |
| `443` | TCP | **ABERTA** | HTTPS | 2.40 ms | `TLSv1.3 (Issuer: Let's Encrypt)` |

## 🔍 Análise de Risco & Recomendações
- ⚠️ **Porta 80 (HTTP) sem HTTPS:** O serviço HTTP está exposto sem o correspondente HTTPS configurado.
```

---

## 🔒 Aviso de Uso Ético (Disclaimer)

Esta ferramenta foi desenvolvida estritamente para **fins educacionais, auditorias de segurança autorizadas, diagnósticos de rede e testes de conformidade defensiva**. O escaneamento de redes de terceiros sem autorização prévia por escrito pode constituir infração legal conforme a legislação vigente (como o Marco Civil da Internet e a Lei nº 12.737/2012 no Brasil).

---

## 👩‍💻 Autora

**Munique Feitoza**  
- GitHub: [@Munique-Feitoza](https://github.com/Munique-Feitoza)  
- LinkedIn: [Munique Feitoza](https://www.linkedin.com/in/munique-feitoza-77034b231/)  

Licença: [GPL-2.0](LICENSE)
