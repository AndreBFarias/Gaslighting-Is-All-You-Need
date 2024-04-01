import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

# Paleta de Cores
CORES = {
    "fundo": "#0f111a",
    "surface": "#1e1f29",
    "acento_primario": "#50fa7b",  # Verde Neon
    "acento_secundario": "#bd93f9", # Roxo Elétrico
    "texto": "#f8f8f2",
    "texto_secundario": "#6272a4",
    "erro": "#ff5555"
}

class PaletaModerna:
    """Classe de compatibilidade para o Wizard (Tkinter nativo)."""
    BG = CORES["fundo"]
    FG = CORES["texto"]
    BG_LIGHTER = CORES["surface"]
    BG_INPUT = "#282a36" # Um pouco mais claro que o fundo
    BG_HEADER = "#15161e" # Um pouco mais escuro que a surface
    PRIMARY = CORES["acento_primario"]
    SECONDARY = CORES["acento_secundario"]
    FG_DIM = CORES["texto_secundario"]

class BotaoNeon(ctk.CTkButton):
    """Botão com estilo neon e cantos arredondados."""
    def __init__(self, master, text: str, command: Callable, cor: str = CORES["acento_primario"], height: int = 45, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=cor,
            hover_color=self._ajustar_brilho(cor),
            text_color="#282a36", # Dracula Background para contraste
            font=("Roboto", 16, "bold"),
            corner_radius=15,
            height=height,
            **kwargs
        )

    def _ajustar_brilho(self, hex_color: str, fator: float = 0.8) -> str:
        """Escurece a cor para o hover."""
        # Simplificação: retorna uma cor fixa mais escura se for verde, ou roxo
        if hex_color == CORES["acento_primario"]:
            return "#40c963"
        elif hex_color == CORES["acento_secundario"]:
            return "#9d7cd8"
        return hex_color

class CardNeural(ctk.CTkFrame):
    """Container para seções da sidebar."""
    def __init__(self, master, titulo: str, **kwargs):
        super().__init__(
            master,
            fg_color=CORES["surface"],
            corner_radius=15,
            border_width=1,
            border_color="#44475a",
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=("Roboto", 14, "bold"),
            text_color=CORES["texto"]
        )
        self.lbl_titulo.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

class InputIsland(ctk.CTkFrame):
    """Área de input flutuante."""
    def __init__(self, master, command: Callable, **kwargs):
        super().__init__(
            master,
            fg_color="transparent", # Fundo transparente para o container
            corner_radius=0,
            height=80, # Altura suficiente para a ilha
            border_width=0,
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)

        # Frame interno para dar o efeito de "ilha" flutuante
        self.frame_interno = ctk.CTkFrame(
            self,
            fg_color=CORES["surface"],
            corner_radius=30,
            border_width=1,
            border_color="#44475a"
        )
        self.frame_interno.pack(expand=True, fill="both", padx=20, pady=10)
        self.frame_interno.grid_columnconfigure(0, weight=1)

        self.entrada = ctk.CTkEntry(
            self.frame_interno,
            placeholder_text="Digite sua mensagem...",
            fg_color="transparent",
            border_width=0,
            text_color=CORES["texto"],
            font=("Roboto", 16), # Aumentado para 16
            height=40
        )
        self.entrada.grid(row=0, column=0, padx=(20, 10), pady=5, sticky="ew")
        self.entrada.bind("<Return>", lambda e: command())

        self.btn_enviar = ctk.CTkButton(
            self.frame_interno,
            text="",
            width=40,
            height=40,
            corner_radius=20,
            fg_color=CORES["acento_primario"],
            hover_color="#40c963",
            text_color="#282a36",
            font=("Roboto", 16, "bold"),
            command=command
        )
        self.btn_enviar.grid(row=0, column=1, padx=(0, 10), pady=5)

    def get(self) -> str:
        return self.entrada.get()

    def delete(self, first, last=None):
        self.entrada.delete(first, last)

    def focus_set(self):
        self.entrada.focus_set()

class BolhaChat(ctk.CTkFrame):
    """Bolha de mensagem do chat."""
    def __init__(self, master, texto: str, is_user: bool, **kwargs):
        # Cores e alinhamento baseados no remetente
        if is_user:
            cor_fundo = "#2d2f3a"
            cor_texto = CORES["texto"]
            align_frame = "e"
            icone = None
        else:
            cor_fundo = CORES["surface"]
            cor_texto = CORES["texto"]
            align_frame = "w"
            icone = "" # Placeholder para ícone

        super().__init__(
            master,
            fg_color=cor_fundo,
            corner_radius=15,
            **kwargs
        )

        self.grid_columnconfigure(1, weight=1)

        if icone:
            self.lbl_icone = ctk.CTkLabel(
                self,
                text=icone,
                font=("Roboto", 20),
                text_color=CORES["acento_primario"]
            )
            self.lbl_icone.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="n")

        self.lbl_texto = ctk.CTkLabel(
            self,
            text=texto,
            text_color=cor_texto,
            font=("Roboto", 16), # Aumentado para 16
            wraplength=500,
            justify="left"
        )
        self.lbl_texto.grid(row=0, column=1 if icone else 0, padx=15, pady=10, sticky="w")

class HistoricoDropdown(ctk.CTkFrame):
    """
    Accordion expansível para o histórico de conversas.
    """
    def __init__(self, master, titulo: str = "️ Conversas Anteriores", **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            corner_radius=10,
            **kwargs
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Permite que o conteúdo expanda

        # 1. Header (Botão Toggle)
        self.btn_toggle = ctk.CTkButton(
            self,
            text=f"▶ {titulo}", # Começa fechado
            font=("Roboto", 14, "bold"),
            fg_color="#2b2d3e",
            hover_color="#36384a",
            text_color=CORES["texto_secundario"],
            anchor="w",
            height=30,
            command=self._toggle
        )
        self.btn_toggle.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # 2. Container Expansível
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.grid(row=1, column=0, sticky="nsew")
        self.frame_conteudo.grid_columnconfigure(0, weight=1)

        # Scrollable Frame Dentro
        # Height inicial 0, mas com max-height definido via configure posterior
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.frame_conteudo,
            fg_color="#181a23",
            label_text="",
            corner_radius=10,
            height=0
        )
        self.scroll_frame.grid(row=0, column=0, sticky="ew")

        self.itens = []

        # Começa fechado
        self.is_expanded = False
        self.frame_conteudo.grid_remove()

        # Estado inicial (vazio -> desativado)
        self._atualizar_estado_botao()

    def _toggle(self):
        if not self.itens: # Segurança extra
            return

        if self.is_expanded:
            self.frame_conteudo.grid_remove()
            self.btn_toggle.configure(text=self.btn_toggle.cget("text").replace("▼", "▶"))
            self.is_expanded = False
        else:
            self.frame_conteudo.grid()
            self.btn_toggle.configure(text=self.btn_toggle.cget("text").replace("▶", "▼"))
            self.is_expanded = True
            self._atualizar_altura() # Garante altura correta ao abrir

    def _atualizar_estado_botao(self):
        """Ativa/Desativa o botão baseado se há itens."""
        if not self.itens:
            self.btn_toggle.configure(state="disabled", fg_color="transparent", text_color="#44475a")
            # Se estava aberto, fecha
            if self.is_expanded:
                self._toggle()
        else:
            self.btn_toggle.configure(state="normal", fg_color="#2b2d3e", text_color=CORES["texto_secundario"])

    def limpar_itens(self):
        """Remove todos os itens da lista com segurança."""
        for item in self.itens:
            if isinstance(item, ctk.CTkBaseClass) or isinstance(item, tk.Widget):
                item.destroy()
        self.itens.clear()
        self._atualizar_altura()
        self._atualizar_estado_botao()

    def adicionar_botao(self, texto, comando):
        """Adiciona um botão de histórico com gerenciamento seguro."""
        btn = ctk.CTkButton(
            self.scroll_frame,
            text=texto,
            fg_color="transparent",
            hover_color=CORES["surface"],
            anchor="w",
            text_color="#f8f8f2",
            command=comando,
            height=35, # Altura fixa para cálculo
            font=("Roboto", 13)
        )
        btn.pack(fill="x", pady=2) # PadY para cálculo
        self.itens.append(btn)
        self._atualizar_altura()
        self._atualizar_estado_botao()

    def adicionar_label(self, texto):
        """Adiciona um label (ex: vazio)."""
        lbl = ctk.CTkLabel(self.scroll_frame, text=texto, text_color="gray")
        lbl.pack(pady=5)
        self.itens.append(lbl)
        self._atualizar_altura()
        self._atualizar_estado_botao()

    def _atualizar_altura(self):
        """Calcula e aplica a altura ideal baseada nos itens."""
        qtd = len(self.itens)

        # Altura base por item: 35px (height) + 4px (pady=2*2) = 39px
        altura_por_item = 39
        # Limite: 5 itens * 39 = 195px
        altura_maxima = 195

        altura_necessaria = qtd * altura_por_item

        # Se for maior que o máximo, trava no máximo (scroll ativa)
        # Se for menor, usa o necessário
        altura_final = min(altura_necessaria, altura_maxima)

        # Importante: Se for 0, deixa 0
        if qtd > 0 and altura_final < 39:
             altura_final = 39

        self.scroll_frame.configure(height=altura_final)
