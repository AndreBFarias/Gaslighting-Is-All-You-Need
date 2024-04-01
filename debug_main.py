#!/usr/bin/env python3
"""
Debug script - versão verbosa do main.py
"""

import sys
import os
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("DEBUG: Iniciando aplicação...")
print("=" * 60)

try:
    print("\n[1] Importando módulos...")
    from interface import iniciar_aplicacao_chat, WizardSetup
    from utilitarios import ConfigManager
    print("     Imports OK")

    print("\n[2] Criando ConfigManager...")
    config_manager = ConfigManager()
    print(f"     ConfigManager criado")
    print(f"    - Precisa wizard: {config_manager.precisa_wizard()}")

    print("\n[3] Criando root Tk()...")
    root = tk.Tk()
    print("     Root criado")

    print("\n[4] Fazendo root.withdraw()...")
    root.withdraw()
    print("     Root hidden")

    if config_manager.precisa_wizard():
        print("\n[5] Precisa wizard, criando WizardSetup...")
        try:
            wizard = WizardSetup(root, config_manager)
            print("     Wizard criado")

            print("\n[6] Aguardando wizard (root.wait_window)...")
            print("    >> Uma janela do wizard deve aparecer agora!")
            print("    >> Se não aparecer, pressione Ctrl+C e reporte o problema")

            root.wait_window(wizard)
            print("     Wizard concluído")

        except Exception as e:
            print(f"     ERRO no wizard: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        print("\n[5] Wizard não necessário (já configurado)")

    print("\n[7] Destruindo root temporário...")
    root.destroy()
    print("     Root destroyed")

    print("\n[8] Iniciando aplicação de chat...")
    print("    >> A interface principal deve aparecer agora!")
    iniciar_aplicacao_chat(config_manager)

except Exception as e:
    print(f"\n ERRO FATAL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
