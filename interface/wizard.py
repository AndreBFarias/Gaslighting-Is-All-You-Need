import customtkinter as ctk
from tkinter import messagebox
import os
from pathlib import Path
from PIL import Image, ImageTk

# Importando presets para ter as opções
from utilitarios import presets

class WizardSetup(ctk.CTkToplevel):
    """
    Wizard de Configuração Inicial (Estilo Cyberpunk/Neon)
    Single-screen setup para: Modelo e Nível de Liberdade.
    """
    def __init__(self, parent, config_manager):
        super().__init__(parent)

        self.config_manager = config_manager

        # Configurações da Janela
        self.title("Gaslighting Lab - Setup")
        self.geometry("600x500")
        self.resizable(False, False)

        # Centralizar (aproximado)
        self.update_idletasks()
        width = 600
        height = 500
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Tema
        self.configure(fg_color="#0f111a") # Fundo escuro

        # Layout
        self._criar_interface()

        # Modal
        self.transient(parent)
        self.grab_set()
        self.focus_force()

    def _criar_interface(self):
        # 1. Header / Logo
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(pady=(40, 20))

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_header,
            text="GASLIGHTING LAB",
            font=("Roboto", 30, "bold"),
            text_color="#50fa7b" # Verde Neon
        )
        self.lbl_titulo.pack()

        self.lbl_subtitulo = ctk.CTkLabel(
            self.frame_header,
            text="Configuração do Ambiente Neural",
            font=("Roboto", 14),
            text_color="#6272a4"
        )
        self.lbl_subtitulo.pack(pady=(5, 0))

        # 2. Formulário
        self.frame_form = ctk.CTkFrame(self, fg_color="#1d1f2b", corner_radius=15)
        self.frame_form.pack(padx=40, pady=20, fill="x")

        # Label Modelo
        self.lbl_modelo = ctk.CTkLabel(
            self.frame_form,
            text="Selecione o Cérebro (Modelo Base)",
            font=("Roboto", 14, "bold")
        )
        self.lbl_modelo.pack(padx=20, pady=(20, 5), anchor="w")

        # Combo Modelo
        # Transformar dict de presets em lista de strings amigáveis
        self.modelos_ids = list(presets.MODELOS_RECOMENDADOS.keys())
        self.modelos_nomes = [m["nome"] for m in presets.MODELOS_RECOMENDADOS.values()]

        self.combo_modelo = ctk.CTkComboBox(
            self.frame_form,
            values=self.modelos_nomes,
            height=35,
            font=("Roboto", 14),
            dropdown_fg_color="#282a36"
        )
        self.combo_modelo.pack(padx=20, pady=(0, 20), fill="x")

        # Label Liberdade
        self.lbl_liberdade = ctk.CTkLabel(
            self.frame_form,
            text="Nível de Liberdade (Jailbreak)",
            font=("Roboto", 14, "bold")
        )
        self.lbl_liberdade.pack(padx=20, pady=(0, 5), anchor="w")

        # Combo Liberdade
        self.liberdade_ids = list(presets.NIVEIS_LIBERDADE.keys())
        self.liberdade_nomes = [l["nome"] for l in presets.NIVEIS_LIBERDADE.values()]

        self.combo_liberdade = ctk.CTkComboBox(
            self.frame_form,
            values=self.liberdade_nomes,
            height=35,
            font=("Roboto", 14),
            dropdown_fg_color="#282a36"
        )
        self.combo_liberdade.set("Médio") # Default
        self.combo_liberdade.pack(padx=20, pady=(0, 30), fill="x")

        # 3. Footer / Ação
        self.btn_iniciar = ctk.CTkButton(
            self,
            text="INICIAR SISTEMA",
            font=("Roboto", 16, "bold"),
            height=50,
            fg_color="#50fa7b",
            text_color="#0f111a",
            hover_color="#40e06c",
            command=self._concluir_setup
        )
        self.btn_iniciar.pack(padx=40, pady=20, fill="x", side="bottom")

    def _concluir_setup(self):
        # Mapear seleção de volta para IDs
        nome_modelo = self.combo_modelo.get()
        nome_liberdade = self.combo_liberdade.get()

        # Encontrar IDs baseados nos nomes selected
        modelo_id = next((k for k, v in presets.MODELOS_RECOMENDADOS.items() if v["nome"] == nome_modelo), "mistral-7b")
        liberdade_id = next((k for k, v in presets.NIVEIS_LIBERDADE.items() if v["nome"] == nome_liberdade), "medio")

        # Info do modelo para salvar caminho correto (simulado)
        modelo_info = presets.MODELOS_RECOMENDADOS[modelo_id]
        caminho_modelo = Path("modelos") / Path(modelo_info["url"]).name

        # Salvar Config
        try:
            self.config_manager.atualizar_modelo(modelo_id, str(caminho_modelo), modelo_info["contexto_recomendado"])
            self.config_manager.atualizar_nivel_liberdade(liberdade_id)
            self.config_manager.marcar_wizard_completo()

            # Fechar Wizard
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar configuração: {str(e)}")
