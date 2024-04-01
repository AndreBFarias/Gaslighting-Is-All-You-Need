#!/usr/bin/env python3
"""
Wizard simplificado para debug - apenas widgets nativos
"""
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from utilitarios import ConfigManager, presets


class WizardSimples(tk.Toplevel):
    """Wizard simplificado sem componentes customizados"""

    def __init__(self, parent, config_manager):
        super().__init__(parent)

        self.config_manager = config_manager

        self.title("Setup Wizard")
        self.geometry("600x400")

        tk.Label(self, text="Bem-vindo!", font=("Arial", 16)).pack(pady=20)

        tk.Label(self, text="Modelo:").pack()
        self.var_modelo = tk.StringVar(value="llama3-8b")
        for key in presets.MODELOS_RECOMENDADOS.keys():
            tk.Radiobutton(self, text=key, variable=self.var_modelo, value=key).pack()

        tk.Button(self, text="Salvar e Fechar", command=self.salvar).pack(pady=20)

    def salvar(self):
        modelo_id = self.var_modelo.get()
        modelo_info = presets.MODELOS_RECOMENDADOS[modelo_id]
        caminho_modelo = Path("modelos") / Path(modelo_info["url"]).name

        self.config_manager.atualizar_modelo(
            modelo_id,
            str(caminho_modelo),
            modelo_info["contexto_recomendado"]
        )
        self.config_manager.marcar_wizard_completo()

        messagebox.showinfo("OK", "Salvo!")
        self.destroy()


if __name__ == "__main__":
    print("Testando wizard simples...")

    config_manager = ConfigManager()

    root = tk.Tk()
    print("Root criado")

    wizard = WizardSimples(root, config_manager)
    print("Wizard criado - janela deve aparecer!")

    root.wait_window(wizard)
    print("Wizard fechado")

    root.destroy()
    print("Sucesso!")
