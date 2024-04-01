"""
╔══════════════════════════════════════════════════════════════════╗
║  COMPONENTES DRACULA - Widgets das Sombras                       ║
║  Interface gótica com paleta Dracula                             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Optional


class PaletaDracula:
    """Cores oficiais do tema Dracula"""
    BG = "#282a36"
    BG_DARKER = "#1e1f29"
    BG_LIGHTER = "#343746"
    FG = "#f8f8f2"
    SELECTION = "#44475a"
    COMMENT = "#6272a4"

    # Cores ANSI
    CYAN = "#8be9fd"
    GREEN = "#50fa7b"
    ORANGE = "#ffb86c"
    PINK = "#ff79c6"
    PURPLE = "#bd93f9"
    RED = "#ff5555"
    YELLOW = "#f1fa8c"


class BotaoDracula(tk.Button):
    """# 1 - Botão estilizado com tema Dracula"""
    def __init__(self, master, **kwargs):
        cor_principal = kwargs.pop('cor', PaletaDracula.PURPLE)

        super().__init__(
            master,
            bg=cor_principal,
            fg=PaletaDracula.FG,
            activebackground=PaletaDracula.PINK,
            activeforeground=PaletaDracula.FG,
            relief=tk.FLAT,
            font=("JetBrains Mono", 10, "bold"),
            cursor="hand2",
            padx=15,
            pady=8,
            **kwargs
        )

        self.bind("<Enter>", lambda e: self.config(bg=PaletaDracula.PINK))
        self.bind("<Leave>", lambda e: self.config(bg=cor_principal))


class CaixaTextoDracula(scrolledtext.ScrolledText):
    """# 2 - Área de texto com sintaxe highlight"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            bg=PaletaDracula.BG_DARKER,
            fg=PaletaDracula.FG,
            insertbackground=PaletaDracula.CYAN,
            selectbackground=PaletaDracula.SELECTION,
            selectforeground=PaletaDracula.FG,
            font=("JetBrains Mono", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            **kwargs
        )

        # Configura tags para highlight
        self.tag_config("erro", foreground=PaletaDracula.RED)
        self.tag_config("sucesso", foreground=PaletaDracula.GREEN)
        self.tag_config("aviso", foreground=PaletaDracula.YELLOW)
        self.tag_config("info", foreground=PaletaDracula.CYAN)
        self.tag_config("numero", foreground=PaletaDracula.ORANGE)

    def anexar_colorido(self, texto: str, tag: Optional[str] = None):
        """# 3 - Adiciona texto com cor específica"""
        self.insert(tk.END, texto + "\n", tag)
        self.see(tk.END)


class PainelDobravelDracula(tk.Frame):
    """# 4 - Painel expansível/colapsável"""
    def __init__(self, master, titulo: str, **kwargs):
        super().__init__(master, bg=PaletaDracula.BG, **kwargs)

        self.expandido = tk.BooleanVar(value=True)

        # Cabeçalho clicável
        self.cabecalho = tk.Frame(self, bg=PaletaDracula.BG_LIGHTER, cursor="hand2")
        self.cabecalho.pack(fill=tk.X, padx=2, pady=2)

        self.icone = tk.Label(
            self.cabecalho,
            text="▼",
            bg=PaletaDracula.BG_LIGHTER,
            fg=PaletaDracula.PURPLE,
            font=("Arial", 12)
        )
        self.icone.pack(side=tk.LEFT, padx=5)

        self.titulo_label = tk.Label(
            self.cabecalho,
            text=titulo,
            bg=PaletaDracula.BG_LIGHTER,
            fg=PaletaDracula.FG,
            font=("JetBrains Mono", 11, "bold")
        )
        self.titulo_label.pack(side=tk.LEFT, pady=8)

        # Conteúdo do painel
        self.conteudo = tk.Frame(self, bg=PaletaDracula.BG)
        self.conteudo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Bind de clique
        self.cabecalho.bind("<Button-1>", self.alternar)
        self.icone.bind("<Button-1>", self.alternar)
        self.titulo_label.bind("<Button-1>", self.alternar)

    def alternar(self, event=None):
        """# 5 - Expande ou colapsa o painel"""
        if self.expandido.get():
            self.conteudo.pack_forget()
            self.icone.config(text="▶")
            self.expandido.set(False)
        else:
            self.conteudo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.icone.config(text="▼")
            self.expandido.set(True)


class BarraProgressoDracula(ttk.Progressbar):
    """# 6 - Barra de progresso estilizada"""
    def __init__(self, master, **kwargs):
        style = ttk.Style()
        style.theme_use('default')

        style.configure(
            "Dracula.Horizontal.TProgressbar",
            background=PaletaDracula.PURPLE,
            troughcolor=PaletaDracula.BG_DARKER,
            bordercolor=PaletaDracula.SELECTION,
            lightcolor=PaletaDracula.PURPLE,
            darkcolor=PaletaDracula.PURPLE
        )

        super().__init__(
            master,
            style="Dracula.Horizontal.TProgressbar",
            **kwargs
        )


class CampoEntradaDracula(tk.Entry):
    """# 7 - Campo de entrada de texto estilizado"""
    def __init__(self, master, placeholder: str = "", **kwargs):
        super().__init__(
            master,
            bg=PaletaDracula.BG_DARKER,
            fg=PaletaDracula.FG,
            insertbackground=PaletaDracula.CYAN,
            selectbackground=PaletaDracula.SELECTION,
            selectforeground=PaletaDracula.FG,
            font=("JetBrains Mono", 10),
            relief=tk.FLAT,
            **kwargs
        )

        self.placeholder = placeholder
        self.placeholder_ativo = False

        if placeholder:
            self._mostrar_placeholder()
            self.bind("<FocusIn>", self._remover_placeholder)
            self.bind("<FocusOut>", self._adicionar_placeholder)

    def _mostrar_placeholder(self):
        """# 8 - Exibe texto de placeholder"""
        self.insert(0, self.placeholder)
        self.config(fg=PaletaDracula.COMMENT)
        self.placeholder_ativo = True

    def _remover_placeholder(self, event):
        """# 9 - Remove placeholder ao focar"""
        if self.placeholder_ativo:
            self.delete(0, tk.END)
            self.config(fg=PaletaDracula.FG)
            self.placeholder_ativo = False

    def _adicionar_placeholder(self, event):
        """# 10 - Restaura placeholder se vazio"""
        if not self.get():
            self._mostrar_placeholder()

    def get(self):
        """# 11 - Retorna conteúdo real, não placeholder"""
        if self.placeholder_ativo:
            return ""
        return super().get()


class RotuloDracula(tk.Label):
    """# 11 - Label estilizado"""
    def __init__(self, master, texto: str, destaque: bool = False, **kwargs):
        cor_fg = PaletaDracula.PURPLE if destaque else PaletaDracula.FG
        fonte = ("JetBrains Mono", 10, "bold" if destaque else "normal")

        super().__init__(
            master,
            text=texto,
            bg=PaletaDracula.BG,
            fg=cor_fg,
            font=fonte,
            **kwargs
        )


class GraficoSimplesDracula(tk.Canvas):
    """# 12 - Mini gráfico de barras para métricas"""
    def __init__(self, master, largura: int = 200, altura: int = 100, **kwargs):
        super().__init__(
            master,
            width=largura,
            height=altura,
            bg=PaletaDracula.BG_DARKER,
            highlightthickness=0,
            **kwargs
        )

        self.largura = largura
        self.altura = altura
        self.valores = []
        self.max_pontos = 50

    def adicionar_valor(self, valor: float):
        """# 13 - Adiciona ponto ao gráfico (0.0 a 1.0)"""
        self.valores.append(valor)
        if len(self.valores) > self.max_pontos:
            self.valores.pop(0)
        self._redesenhar()

    def _redesenhar(self):
        """# 14 - Atualiza visualização do gráfico"""
        self.delete("all")

        if not self.valores:
            return

        largura_barra = self.largura / self.max_pontos

        for i, valor in enumerate(self.valores):
            x0 = i * largura_barra
            y0 = self.altura
            x1 = x0 + largura_barra - 1
            y1 = self.altura - (valor * self.altura)

            # Gradiente de cor baseado no valor
            if valor < 0.5:
                cor = PaletaDracula.GREEN
            elif valor < 0.8:
                cor = PaletaDracula.YELLOW
            else:
                cor = PaletaDracula.RED

            self.create_rectangle(
                x0, y0, x1, y1,
                fill=cor,
                outline=""
            )


"""
'A beleza nasce do contraste.'
— Baudelaire (parafraseado)

E interfaces? Nascem quando a estética serve à função.
"""
