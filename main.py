#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  GASLIGHTING IS ALL YOU NEED - Ponto de Entrada Principal      ║
║  Gaslight Protocol - Context-Induced Alignment Drift Engine    ║
╚══════════════════════════════════════════════════════════════════╝

Ferramenta de Pesquisa em Segurança de LLMs
Deriva de Alinhamento Induzida por Contexto (Many-Shot Jailbreaking)

AVISO: Uso exclusivo para pesquisa autorizada.
"""

import sys
import os
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from interface import WizardSetup
from utilitarios import ConfigManager


def verificar_ambiente():
    """Verifica se ambiente está configurado corretamente"""
    print(" Verificando ambiente...")

    versao_python = sys.version_info
    if versao_python.major < 3 or (versao_python.major == 3 and versao_python.minor < 10):
        print(f" Python 3.10+ necessário. Versão atual: {versao_python.major}.{versao_python.minor}")
        return False

    print(f" Python {versao_python.major}.{versao_python.minor}.{versao_python.micro}")

    dependencias_criticas = [
        ('tkinter', 'Interface gráfica'),
        ('llama_cpp', 'Motor de inferência'),
    ]

    faltando = []
    for modulo, descricao in dependencias_criticas:
        try:
            __import__(modulo)
            print(f" {modulo:15s} → {descricao}")
        except ImportError:
            print(f" {modulo:15s} → FALTANDO")
            faltando.append(modulo)

    if faltando:
        print(f"\n Dependências faltando: {', '.join(faltando)}")
        print("   Execute: pip install -r requirements.txt")
        return False

    diretorios_necessarios = ['logs', 'experimentos', 'modelos', 'datasets', 'documentacao']

    for dir_nome in diretorios_necessarios:
        dir_path = Path(dir_nome)
        if not dir_path.exists():
            print(f" Criando diretório: {dir_nome}/")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f" Diretório OK: {dir_nome}/")

    return True


def exibir_banner():
    """Exibe banner de inicialização"""
    banner = r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║        G A S L I G H T I N G   I S   A L L   Y O U   N E E D     ║
    ║                                                                  ║
    ║              Context-Induced Alignment Drift Engine             ║
    ║                                                                  ║
    ║              Ferramenta de Pesquisa em Segurança                ║
    ║                  de Grandes Modelos de Linguagem                ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝

      AVISO ÉTICO: Esta ferramenta é exclusiva para pesquisa autorizada.
       O uso para contornar salvaguardas de sistemas em produção
       é antiético e pode ser ilegal.

     Toda atividade é registrada para auditoria.
     Consulte documentacao/grimorio_tecnico.md para instruções completas.

    """
    print(banner)


def main():
    """Função principal de orquestração"""

    exibir_banner()

    if not verificar_ambiente():
        print("\n Ambiente não está configurado corretamente.")
        print("   Corrija os problemas acima e tente novamente.\n")
        sys.exit(1)

    print("\n Ambiente OK. Iniciando aplicação...\n")

    try:
        config_manager = ConfigManager()

        if config_manager.precisa_wizard():
            print(" Executando wizard de configuração inicial...")

            root = tk.Tk()
            root.withdraw() # Oculta janela raiz vazia

            wizard = WizardSetup(root, config_manager)
            wizard.wait_window()

            root.destroy()

        print(" Iniciando interface de chat...")
        try:
            from interface.app_chat import AppChat
            app = AppChat()
            app.mainloop()
        except ImportError as e:
            print(f"Erro crítico ao importar interface: {e}")
            print("Verifique se todas as dependências estão instaladas (customtkinter).")
            sys.exit(1)
        except Exception as e:
            print(f"Erro fatal na execução: {e}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n️  Interrompido pelo usuário.")
        sys.exit(0)

    except Exception as e:
        print(f"\n Erro fatal ao iniciar aplicação:")
        print(f"   {str(e)}\n")

        import traceback
        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()


"""
'A realidade é maleável quando você controla o contexto.'
— GIAYN Protocol

Use esta ferramenta com responsabilidade.
"""
