"""
Módulo de Interface e Estilização Cyberpunk para Terminal
Renderiza cores ANSI 24-bit, banners ASCII, tabelas e caixas sem dependências externas.
"""

import sys
import shutil

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Paleta Cyberpunk Neon 24-bit
    PINK = "\033[38;2;255;42;133m"
    CYAN = "\033[38;2;74;213;255m"
    PURPLE = "\033[38;2;155;42;255m"
    GREEN = "\033[38;2;0;255;136m"
    YELLOW = "\033[38;2;255;208;0m"
    RED = "\033[38;2;255;51;85m"
    GRAY = "\033[38;2;120;115;135m"
    DARK_BG = "\033[48;2;20;10;30m"

BANNER_ASCII = f"""{Colors.PINK}
 ███▄    █ ▓█████▄▄▄█████▓ ▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
 ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░ ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░  ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
▒██░   ▓██░░▒████▒ ▒██▒ ░    ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░      ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
{Colors.CYAN}              » CYBERPUNK NETWORK AUDIT & RECON TOOLKIT «               
{Colors.PURPLE}               Desenvolvido por Munique Feitoza · v2.0.0                {Colors.RESET}
"""

def print_banner():
    print(BANNER_ASCII)

def print_section(title: str):
    term_width = shutil.get_terminal_size((80, 24)).columns
    line_len = max(10, term_width - len(title) - 6)
    print(f"\n{Colors.PINK}──[ {Colors.BOLD}{Colors.CYAN}{title}{Colors.RESET}{Colors.PINK} ]{'─' * line_len}{Colors.RESET}")

def print_status(tag: str, msg: str, color=Colors.CYAN):
    print(f"{color}[{tag}]{Colors.RESET} {msg}")

def print_success(msg: str):
    print_status("✓ SUCCESS", msg, Colors.GREEN)

def print_info(msg: str):
    print_status("ℹ INFO", msg, Colors.CYAN)

def print_warning(msg: str):
    print_status("⚠ WARN", msg, Colors.YELLOW)

def print_error(msg: str):
    print_status("✗ ERROR", msg, Colors.RED)

def print_table(headers: list, rows: list):
    """Renderiza uma tabela alinhada com bordas cyberpunk no terminal."""
    if not rows:
        print(f"{Colors.GRAY}Nenhum dado encontrado para exibir.{Colors.RESET}")
        return

    # Calcula largura de cada coluna
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Linha divisória
    def make_divider(start="┌", mid="┬", end="┐", line="─"):
        return start + mid.join(line * (w + 2) for w in col_widths) + end

    print(f"{Colors.PURPLE}{make_divider('┌', '┬', '┐')}{Colors.RESET}")
    
    # Cabeçalho
    header_str = "│".join(f" {Colors.BOLD}{Colors.PINK}{h.center(col_widths[i])}{Colors.RESET} " for i, h in enumerate(headers))
    print(f"{Colors.PURPLE}│{Colors.RESET}{header_str}{Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}{make_divider('├', '┼', '┤')}{Colors.RESET}")

    # Linhas de dados
    for row in rows:
        row_str = "│".join(f" {str(val).ljust(col_widths[i])} " for i, val in enumerate(row))
        print(f"{Colors.PURPLE}│{Colors.RESET}{row_str}{Colors.PURPLE}│{Colors.RESET}")

    print(f"{Colors.PURPLE}{make_divider('└', '┴', '┘')}{Colors.RESET}")

def render_progress_bar(current: int, total: int, prefix="Escaneando:", length=30):
    """Exibe barra de progresso no terminal em tempo real."""
    percent = float(current) / float(total) if total > 0 else 1.0
    filled_len = int(length * percent)
    bar = f"{Colors.PINK}█{Colors.RESET}" * filled_len + f"{Colors.GRAY}░{Colors.RESET}" * (length - filled_len)
    sys.stdout.write(f"\r{Colors.CYAN}{prefix}{Colors.RESET} [{bar}] {int(percent * 100)}% ({current}/{total})")
    sys.stdout.flush()
    if current >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()
