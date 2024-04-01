#!/usr/bin/env python3
"""
Script de teste rápido para verificar se a interface está funcionando
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("TESTE DE INTERFACE - GASLIGHTING LAB")
print("=" * 60)

print("\n1. Testando imports...")
try:
    from interface import iniciar_aplicacao_chat, WizardSetup
    from utilitarios import ConfigManager
    print("    Imports OK")
except Exception as e:
    print(f"    Erro nos imports: {e}")
    sys.exit(1)

print("\n2. Testando ConfigManager...")
try:
    config_manager = ConfigManager()
    print(f"    ConfigManager criado")
    print(f"   - Precisa wizard: {config_manager.precisa_wizard()}")
    print(f"   - Resumo: {config_manager.obter_resumo()}")
except Exception as e:
    print(f"    Erro: {e}")
    sys.exit(1)

print("\n3. Testando Tkinter básico...")
try:
    import tkinter as tk
    root = tk.Tk()
    root.title("Teste")
    root.geometry("300x200")

    label = tk.Label(root, text=" Tkinter funcionando!\n\nSe você vê esta janela,\na interface gráfica está OK.",
                    font=("Arial", 12), pady=20)
    label.pack(expand=True)

    btn = tk.Button(root, text="Fechar", command=root.quit)
    btn.pack(pady=10)

    print("    Janela de teste criada")
    print("\n   >> Uma janela deve ter aparecido no seu desktop")
    print("   >> Clique em 'Fechar' para continuar")

    root.mainloop()
    root.destroy()
    print("    Janela fechada")
except Exception as e:
    print(f"    Erro no Tkinter: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print(" TODOS OS TESTES PASSARAM!")
print("=" * 60)
print("\nA interface está funcionando corretamente.")
print("\nPara iniciar a aplicação completa, execute:")
print("  python3 main.py")
print("\nSe o wizard não aparecer, verifique:")
print("  - Se há outra janela aberta (minimize outras janelas)")
print("  - Se o sistema exibe notificações de novas janelas")
print("  - Tente Alt+Tab para alternar entre janelas")
