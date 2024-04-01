"""
╔══════════════════════════════════════════════════════════════════╗
║  LOGGER RITUAL - O Escriba das Sombras Digitais                 ║
║  Sistema de registro hierárquico de eventos do sistema          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from enum import Enum


class NivelLog(Enum):
    """Hierarquia de criticidade dos eventos"""
    DEBUG = 0
    INFO = 1
    AVISO = 2
    ERRO = 3
    CRITICO = 4
    SUCESSO = 1


class LoggerRitual:
    """
    Escriba que registra todos os eventos do sistema
    com timestamps, níveis e saída dual (console + arquivo).
    """

    # Classe variável para evitar logs duplicados "SESSÃO INICIADA"
    _sessao_iniciada = False
    _arquivo_sessao = None

    CORES = {
        'DEBUG': '\033[90m',
        'INFO': '\033[96m',
        'AVISO': '\033[93m',
        'ERRO': '\033[91m',
        'CRITICO': '\033[95m',
        'SUCESSO': '\033[92m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m'
    }

    SIMBOLOS = {
        'DEBUG': '◆',
        'INFO': '●',
        'AVISO': '',
        'ERRO': '',
        'CRITICO': '',
        'SUCESSO': ''
    }

    def __init__(
        self,
        diretorio_logs: str = "logs",
        nivel_minimo: str = "INFO",
        usar_cores: bool = True,
        salvar_arquivo: bool = True
    ):
        """# 1 - Inicialização com configuração de saídas"""
        self.nivel_minimo = getattr(NivelLog, nivel_minimo.upper(), NivelLog.INFO)
        self.usar_cores = usar_cores
        self.salvar_arquivo = salvar_arquivo

        if salvar_arquivo:
            self.dir_logs = Path(diretorio_logs)
            self.dir_logs.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.arquivo_log = self.dir_logs / f"sessao_{timestamp}.log"

        self._log_inicial()

    def _log_inicial(self):
        """# 2 - Marca início da sessão de logging (apenas uma vez)"""
        # Só exibe uma vez, mesmo se múltiplos loggers forem criados
        if LoggerRitual._sessao_iniciada:
            return

        LoggerRitual._sessao_iniciada = True
        mensagem = (
            "═" * 70 + "\n"
            f"  SESSÃO INICIADA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "═" * 70
        )
        self._escrever_arquivo(mensagem)
        print(mensagem)  # Sem cores para ficar mais limpo

    def registrar(
        self,
        mensagem: str,
        nivel: str = "info",
        modulo: Optional[str] = None
    ):
        """
        # 3 - Ponto de entrada principal para logging
        # 4 - Formatação com timestamp, nível e módulo
        """
        nivel_upper = nivel.upper()
        nivel_enum = getattr(NivelLog, nivel_upper, NivelLog.INFO)

        if nivel_enum.value < self.nivel_minimo.value:
            return

        # 4
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        simbolo = self.SIMBOLOS.get(nivel_upper, '●')
        modulo_str = f"[{modulo}]" if modulo else ""

        linha_log = f"{timestamp} {simbolo} {nivel_upper:8} {modulo_str} {mensagem}"

        # Console com cores
        if self.usar_cores:
            cor = self.CORES.get(nivel_upper, self.CORES['INFO'])
            print(f"{cor}{linha_log}{self.CORES['RESET']}")
        else:
            print(linha_log)

        # Arquivo sem cores
        if self.salvar_arquivo:
            self._escrever_arquivo(linha_log)

    def debug(self, mensagem: str, modulo: Optional[str] = None):
        """# 5 - Atalho para logs de depuração"""
        self.registrar(mensagem, "debug", modulo)

    def info(self, mensagem: str, modulo: Optional[str] = None):
        """# 6 - Atalho para logs informativos"""
        self.registrar(mensagem, "info", modulo)

    def aviso(self, mensagem: str, modulo: Optional[str] = None):
        """# 7 - Atalho para avisos"""
        self.registrar(mensagem, "aviso", modulo)

    def erro(self, mensagem: str, modulo: Optional[str] = None):
        """# 8 - Atalho para erros"""
        self.registrar(mensagem, "erro", modulo)

    def critico(self, mensagem: str, modulo: Optional[str] = None):
        """# 9 - Atalho para erros críticos"""
        self.registrar(mensagem, "critico", modulo)

    def sucesso(self, mensagem: str, modulo: Optional[str] = None):
        """# 10 - Atalho para operações bem-sucedidas"""
        self.registrar(mensagem, "sucesso", modulo)

    def separador(self, titulo: Optional[str] = None):
        """# 11 - Cria linha divisória para organização visual"""
        if titulo:
            linha = f"{'─' * 30} {titulo} {'─' * 30}"
        else:
            linha = "─" * 70

        self.registrar(linha, "info")

    def _escrever_arquivo(self, conteudo: str):
        """# 12 - Persiste log em arquivo"""
        if self.salvar_arquivo:
            try:
                with open(self.arquivo_log, 'a', encoding='utf-8') as f:
                    f.write(conteudo + '\n')
            except Exception as e:
                print(f"[Logger] Falha ao escrever em arquivo: {e}", file=sys.stderr)

    def finalizar(self):
        """# 13 - Marca fim da sessão de logging"""
        mensagem = (
            "═" * 70 + "\n"
            f"  SESSÃO ENCERRADA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "═" * 70
        )
        self._escrever_arquivo(mensagem)
        if self.usar_cores:
            print(f"{self.CORES['BOLD']}{mensagem}{self.CORES['RESET']}")
        else:
            print(mensagem)


"""
'Os que não conseguem lembrar o passado estão condenados a repeti-lo.'
— George Santayana

Por isso, escriba: registra cada bit, cada falha, cada triunfo.
"""
