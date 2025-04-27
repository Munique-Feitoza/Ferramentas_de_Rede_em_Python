# Projeto: Ferramentas de Rede em Python

Este projeto contém diversas ferramentas de rede simples e úteis desenvolvidas em Python, incluindo scanner de portas, banner grabbing, servidor e cliente TCP, e automação de varredura com Nmap.

---

## 📂 Conteúdo do Projeto

### 1. **TCP Server e TCP Client**
- **TCP Server (`TCP Server.py`)**
  - Cria um servidor TCP que aguarda conexões.
  - Quando um cliente se conecta, o servidor envia a mensagem "Hello World!" e fecha a conexão.
  
- **TCP Client (`TCP Client.py`)**
  - Se conecta ao servidor TCP criado.
  - Recebe a mensagem enviada e a imprime no terminal.

### 2. **Scanner com Nmap (`Server.py`)**
- Ferramenta interativa que usa a biblioteca `python-nmap` para realizar diferentes tipos de varredura em um IP:
  - Varredura **SYN ACK** (TCP).
  - Varredura **UDP**.
  - Varredura **Abrangente** (TCP + UDP + detecção de sistema operacional e serviços).
- Solicita ao usuário o IP e o tipo de varredura.

### 3. **Banner Grabber (`BannerGrabber.py`)**
- Conecta a um IP e porta fornecidos.
- Captura e exibe o **banner** do serviço que está rodando (por exemplo, servidores HTTP, FTP, etc.).
- Útil para identificar serviços de rede.

### 4. **Port Scanner (`PortScanner.py`)**
- Escaneia uma **porta específica** de um IP informado.
- Informa se a porta está **aberta** ou **fechada**.

---

## ⚙️ Requisitos

- Python 3.x
- Bibliotecas:
  - `socket` (já incluída no Python)
  - `python-nmap` (para o scanner com Nmap)

### Instalação do `python-nmap`
```bash
pip install python-nmap
```

⚠️ **Observação:** Para usar `python-nmap`, você precisa ter o **Nmap** instalado no seu sistema:
- [Download do Nmap](https://nmap.org/download.html)

---

## 🚀 Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```
2. Acesse a pasta do projeto:
```bash
cd nome-do-projeto
```
3. Execute o script que deseja utilizar:
```bash
python3 TCP\ Server.py
python3 TCP\ Client.py
python3 Server.py
python3 BannerGrabber.py
python3 PortScanner.py
```

---

## 📚 Conceitos Aprendidos / Utilizados

- Programação de **sockets** em Python.
- Varredura de **portas** TCP e UDP.
- Captura de **banners** de serviços.
- Uso de **Nmap** via biblioteca Python.
- Tratamento de exceções e conexão de rede segura.

---

# 📸 Exemplos de Uso

## 1. TCP Server e TCP Client

### Execução do `TCP Server.py`
```bash
Servidor iniciado em DESKTOP-1234:3000
Aguardando conexões...
Conexão recebida de: ('192.168.1.5', 58734)
```

### Execução do `TCP Client.py`
```bash
Conectado ao servidor DESKTOP-1234:3000
Mensagem recebida do servidor: Hello World!
Conexão encerrada.
```

---

## 2. Scanner com Nmap (`Server.py`)

### Execução
```bash
Bem-vindo à ferramenta de automação de varredura com Nmap!
<----------------------------------------------------------->
Digite o endereço IP para escanear: 192.168.1.1
O endereço IP informado é: 192.168.1.1

Escolha o tipo de varredura que deseja realizar:
1. Varredura SYN ACK (TCP)
2. Varredura UDP
3. Varredura Abrangente

Digite o número da opção desejada: 1

Você selecionou a opção: 1

Versão do Nmap: (7, 93)
Informações da varredura: {'tcp': 'syn'}
Status do IP: up
Protocolos detectados: ['tcp']
Portas abertas (tcp): dict_keys([22, 80, 443])
```

---

## 3. Banner Grabber (`BannerGrabber.py`)

### Execução
```bash
=== Banner Grabber ===
Digite o endereço IP para escanear: 192.168.1.1
Digite o número da porta para escanear: 80

Banner capturado: HTTP/1.1 400 Bad Request
Server: nginx/1.18.0
Date: Sun, 27 Apr 2025 15:00:00 GMT
```

---

## 4. Port Scanner (`PortScanner.py`)

### Execução
```bash
=== Scanner de Porta ===
Digite o endereço IP ou hostname a ser escaneado: 192.168.1.1
Digite o número da porta a ser escaneada: 22

Porta 22 está ABERTA no host 192.168.1.1.
```

---

# 📋 Observações

- Alguns resultados podem variar dependendo do firewall ou das configurações do destino.
- Para escanear portas baixas (0-1024) em sistemas Unix/Linux, pode ser necessário executar como **sudo**.
- Use estas ferramentas com responsabilidade! ⚠️

---

# 🌟 Finalizando

Este projeto inclui:
- Scripts de rede em Python 💻
- README.md completo 📗
- Exemplos de uso 📷

Bons estudos e boas explorações de rede! 🚀

---

## 📌 License

Projeto licenciado sob a Licença MIT.

