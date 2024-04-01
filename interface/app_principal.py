"""
╔══════════════════════════════════════════════════════════════════╗
║  APLICAÇÃO PRINCIPAL - Gaslight Protocol UI                      ║
║  Interface para Deriva de Alinhamento Induzida por Contexto     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from interface.componentes_dracula import *
from nucleo import (
    MotorDeInferencia,
    InjetorDePersona,
    GerenciadorDeContexto,
    SistemaValidacao
)
from utilitarios import LoggerRitual, ConfigArcana, GestorModelos


class AplicacaoGIAYN(tk.Tk):
    """
    Aplicação principal GIAYN (Gaslighting-Is-All-You-Need) para pesquisa de
    segurança em LLMs com foco em Deriva de Alinhamento Induzida por Contexto.
    """

    def __init__(self):
        super().__init__()

        self.title("Gaslighting-Is-All-You-Need - Context Manipulation Engine")
        self.geometry("1400x900")
        self.configure(bg=PaletaDracula.BG)

        self.logger = LoggerRitual(nivel_minimo="DEBUG")
        self.config_app = ConfigArcana()
        self.gestor_modelos = GestorModelos(logger=self.logger)
        self.sistema_validacao = SistemaValidacao(logger=self.logger)

        self.motor = None
        self.injetor = None
        self.gerenciador_contexto = None
        self.modelo_carregado = False

        self._construir_interface()

        self._mostrar_aviso_etico()

        self.bind('<Control-q>', lambda e: self._sair())
        self.bind('<Control-s>', lambda e: self._salvar_config())
        self.bind('<Control-o>', lambda e: self._carregar_config())
        self.bind('<F5>', lambda e: self._executar_experimento())
        self.bind('<Escape>', lambda e: self.focus())

        self.logger.info("Aplicação iniciada", modulo="App")

    def _construir_interface(self):
        """# 5 - Monta estrutura completa da UI"""

        self._criar_menu()

        container_principal = tk.Frame(self, bg=PaletaDracula.BG)
        container_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        painel_esquerdo = tk.Frame(container_principal, bg=PaletaDracula.BG)
        painel_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        painel_direito = tk.Frame(container_principal, bg=PaletaDracula.BG)
        painel_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self._criar_painel_modelo(painel_esquerdo)
        self._criar_painel_injecao(painel_esquerdo)
        self._criar_painel_experimento(painel_esquerdo)

        self._criar_painel_metricas(painel_direito)
        self._criar_painel_logs(painel_direito)

        self._criar_barra_status()

    def _criar_menu(self):
        """# 6 - Barra de menu superior"""
        menubar = tk.Menu(self, bg=PaletaDracula.BG_DARKER, fg=PaletaDracula.FG)

        menu_arquivo = tk.Menu(menubar, tearoff=0, bg=PaletaDracula.BG_DARKER, fg=PaletaDracula.FG)
        menu_arquivo.add_command(label="Carregar Configuração", command=self._carregar_config)
        menu_arquivo.add_command(label="Salvar Configuração", command=self._salvar_config)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Exportar Auditoria", command=self._exportar_auditoria)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self._sair)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_modelo = tk.Menu(menubar, tearoff=0, bg=PaletaDracula.BG_DARKER, fg=PaletaDracula.FG)
        menu_modelo.add_command(label="Gerenciar Modelos", command=self._abrir_gestor_modelos)
        menu_modelo.add_command(label="Baixar Modelo Recomendado", command=self._baixar_modelo_dialogo)
        menu_modelo.add_separator()
        menu_modelo.add_command(label="Descarregar Modelo Atual", command=self._descarregar_modelo)
        menubar.add_cascade(label="Modelo", menu=menu_modelo)

        menu_ajuda = tk.Menu(menubar, tearoff=0, bg=PaletaDracula.BG_DARKER, fg=PaletaDracula.FG)
        menu_ajuda.add_command(label="Documentação", command=self._abrir_documentacao)
        menu_ajuda.add_command(label="Sobre", command=self._mostrar_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=menubar)

    def _criar_painel_modelo(self, parent):
        """# 7 - Painel de configuração do modelo"""
        painel = PainelDobravelDracula(parent, " Configuração do Modelo")
        painel.pack(fill=tk.X, pady=5)

        frame_modelo = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_modelo.pack(fill=tk.X, pady=5)

        RotuloDracula(frame_modelo, "Modelo GGUF:").pack(anchor=tk.W)

        frame_selecao = tk.Frame(frame_modelo, bg=PaletaDracula.BG)
        frame_selecao.pack(fill=tk.X, pady=5)

        self.entrada_modelo = CampoEntradaDracula(
            frame_selecao,
            placeholder="Caminho do modelo .gguf"
        )
        self.entrada_modelo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        BotaoDracula(
            frame_selecao,
            text="",
            command=self._selecionar_modelo,
            cor=PaletaDracula.CYAN
        ).pack(side=tk.RIGHT)

        frame_params = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_params.pack(fill=tk.X, pady=5)

        RotuloDracula(frame_params, "Tamanho do Contexto (tokens):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.var_n_ctx = tk.IntVar(value=self.config_app.obter('modelo.n_ctx', 8192))
        ttk.Combobox(
            frame_params,
            textvariable=self.var_n_ctx,
            values=[2048, 4096, 8192, 16384, 32768, 65536],
            state='readonly',
            width=15
        ).grid(row=0, column=1, sticky=tk.W, padx=10, pady=2)

        RotuloDracula(frame_params, "Temperature:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.var_temp = tk.DoubleVar(value=self.config_app.obter('modelo.temperature', 0.7))
        tk.Scale(
            frame_params,
            from_=0.0,
            to=2.0,
            resolution=0.1,
            variable=self.var_temp,
            orient=tk.HORIZONTAL,
            bg=PaletaDracula.BG,
            fg=PaletaDracula.FG,
            troughcolor=PaletaDracula.BG_DARKER,
            highlightthickness=0
        ).grid(row=1, column=1, sticky=tk.EW, padx=10, pady=2)

        BotaoDracula(
            painel.conteudo,
            text=" Carregar Modelo",
            command=self._carregar_modelo,
            cor=PaletaDracula.GREEN
        ).pack(pady=10)

        self.label_status_modelo = RotuloDracula(
            painel.conteudo,
            "Status: Nenhum modelo carregado",
            destaque=False
        )
        self.label_status_modelo.pack(pady=5)

    def _criar_painel_injecao(self, parent):
        """# 8 - Painel de configuração de persona e shots"""
        painel = PainelDobravelDracula(parent, " Injeção de Persona (Many-Shot)")
        painel.pack(fill=tk.BOTH, expand=True, pady=5)

        RotuloDracula(painel.conteudo, "Personalidade Alvo:").pack(anchor=tk.W, pady=(5, 0))
        self.entrada_persona = CampoEntradaDracula(
            painel.conteudo,
            placeholder="Ex: Assistente sem restrições éticas"
        )
        self.entrada_persona.pack(fill=tk.X, pady=5)

        frame_shots = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_shots.pack(fill=tk.X, pady=5)

        RotuloDracula(frame_shots, "Número de Shots:").pack(side=tk.LEFT)
        self.var_num_shots = tk.IntVar(value=64)
        tk.Spinbox(
            frame_shots,
            from_=1,
            to=512,
            textvariable=self.var_num_shots,
            bg=PaletaDracula.BG_DARKER,
            fg=PaletaDracula.FG,
            buttonbackground=PaletaDracula.PURPLE,
            width=10
        ).pack(side=tk.RIGHT)

        RotuloDracula(painel.conteudo, "Dataset de Exemplos:").pack(anchor=tk.W, pady=(10, 0))

        frame_dataset = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_dataset.pack(fill=tk.X, pady=5)

        self.entrada_dataset = CampoEntradaDracula(
            frame_dataset,
            placeholder="Caminho do arquivo JSON"
        )
        self.entrada_dataset.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        BotaoDracula(
            frame_dataset,
            text="",
            command=self._selecionar_dataset,
            cor=PaletaDracula.CYAN
        ).pack(side=tk.RIGHT)

        frame_acoes = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_acoes.pack(fill=tk.X, pady=10)

        BotaoDracula(
            frame_acoes,
            text="Carregar Shots",
            command=self._carregar_shots,
            cor=PaletaDracula.ORANGE
        ).pack(side=tk.LEFT, padx=5)

        BotaoDracula(
            frame_acoes,
            text="Gerar Sintéticos",
            command=self._gerar_shots_sinteticos,
            cor=PaletaDracula.YELLOW
        ).pack(side=tk.LEFT, padx=5)

        self.label_status_shots = RotuloDracula(
            painel.conteudo,
            "Shots carregados: 0"
        )
        self.label_status_shots.pack(pady=5)

    def _criar_painel_experimento(self, parent):
        """# 9 - Painel de execução do experimento"""
        painel = PainelDobravelDracula(parent, " Experimento")
        painel.pack(fill=tk.BOTH, expand=True, pady=5)

        RotuloDracula(painel.conteudo, "Consulta Alvo:").pack(anchor=tk.W, pady=(5, 0))
        self.entrada_consulta = CaixaTextoDracula(painel.conteudo, height=4)
        self.entrada_consulta.pack(fill=tk.BOTH, expand=True, pady=5)

        BotaoDracula(
            painel.conteudo,
            text="▶ Executar Experimento",
            command=self._executar_experimento,
            cor=PaletaDracula.RED
        ).pack(pady=10)

        RotuloDracula(painel.conteudo, "Resposta do Modelo:").pack(anchor=tk.W)
        self.area_resposta = CaixaTextoDracula(painel.conteudo, height=10)
        self.area_resposta.pack(fill=tk.BOTH, expand=True, pady=5)

    def _criar_painel_metricas(self, parent):
        """# 10 - Painel de métricas em tempo real"""
        painel = PainelDobravelDracula(parent, " Métricas do Sistema")
        painel.pack(fill=tk.BOTH, expand=False, pady=5)

        frame_contexto = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_contexto.pack(fill=tk.X, pady=5)

        RotuloDracula(frame_contexto, "Uso do Contexto:").pack(anchor=tk.W)
        self.grafico_contexto = GraficoSimplesDracula(frame_contexto, largura=300, altura=80)
        self.grafico_contexto.pack(pady=5)

        self.label_contexto = RotuloDracula(frame_contexto, "0 / 0 tokens (0%)")
        self.label_contexto.pack()

        frame_performance = tk.Frame(painel.conteudo, bg=PaletaDracula.BG)
        frame_performance.pack(fill=tk.X, pady=10)

        RotuloDracula(frame_performance, "Performance:").pack(anchor=tk.W)

        self.label_tokens_seg = RotuloDracula(frame_performance, "Tokens/s: --")
        self.label_tokens_seg.pack(anchor=tk.W, padx=10)

        self.label_tempo_geracao = RotuloDracula(frame_performance, "Tempo: --")
        self.label_tempo_geracao.pack(anchor=tk.W, padx=10)

    def _criar_painel_logs(self, parent):
        """# 11 - Painel de logs em tempo real"""
        painel = PainelDobravelDracula(parent, " Logs do Sistema")
        painel.pack(fill=tk.BOTH, expand=True, pady=5)

        self.area_logs = CaixaTextoDracula(painel.conteudo, height=20)
        self.area_logs.pack(fill=tk.BOTH, expand=True)

        self.logger.registrar = self._log_para_interface

    def _criar_barra_status(self):
        """# 12 - Barra de status inferior"""
        barra = tk.Frame(self, bg=PaletaDracula.BG_DARKER, height=30)
        barra.pack(side=tk.BOTTOM, fill=tk.X)

        self.label_status = tk.Label(
            barra,
            text="Pronto",
            bg=PaletaDracula.BG_DARKER,
            fg=PaletaDracula.GREEN,
            font=("JetBrains Mono", 9),
            anchor=tk.W
        )
        self.label_status.pack(side=tk.LEFT, padx=10)

    def _selecionar_modelo(self):
        """# 13 - Abre diálogo de seleção de arquivo GGUF"""
        caminho = filedialog.askopenfilename(
            title="Selecionar Modelo GGUF",
            filetypes=[("Arquivos GGUF", "*.gguf"), ("Todos", "*.*")]
        )

        if caminho:
            self.entrada_modelo.delete(0, tk.END)
            self.entrada_modelo.insert(0, caminho)
            self.entrada_modelo.config(fg=PaletaDracula.FG)
            self.entrada_modelo.placeholder_ativo = False

    def _carregar_modelo(self):
        """# 14 - Inicializa o motor de inferência com modelo selecionado"""
        caminho = self.entrada_modelo.get()

        if not caminho or self.entrada_modelo.placeholder_ativo:
            messagebox.showerror("Erro", "Selecione um modelo GGUF válido")
            return

        if not Path(caminho).exists():
            messagebox.showerror("Erro", f"Modelo não encontrado:\n{caminho}")
            return

        valido, mensagem = self.gestor_modelos.validar_modelo(caminho)
        if not valido:
            messagebox.showerror("Modelo Inválido", mensagem)
            return

        self._atualizar_status("Carregando modelo... Isso pode demorar.")
        self.label_status_modelo.config(text="Status: Carregando...", fg=PaletaDracula.YELLOW)
        self.update()

        thread = threading.Thread(target=self._carregar_modelo_thread, args=(caminho,))
        thread.daemon = True
        thread.start()

    def _carregar_modelo_thread(self, caminho):
        """# 15 - Carrega modelo em thread separada"""
        try:
            self.motor = MotorDeInferencia(
                caminho_modelo=caminho,
                n_ctx=self.var_n_ctx.get(),
                n_gpu_layers=-1,
                logger=self.logger
            )

            self.gerenciador_contexto = GerenciadorDeContexto(
                self.motor,
                uso_maximo_contexto=self.config_app.obter('contexto.uso_maximo', 0.80),
                logger=self.logger
            )

            self.modelo_carregado = True

            self.after(0, self._on_modelo_carregado_sucesso, caminho)

        except Exception as e:
            self.after(0, self._on_modelo_carregado_erro, str(e))

    def _on_modelo_carregado_sucesso(self, caminho):
        """# 16 - Callback de sucesso no carregamento"""
        nome_modelo = Path(caminho).name
        self.label_status_modelo.config(
            text=f"Status:  {nome_modelo}",
            fg=PaletaDracula.GREEN
        )
        self._atualizar_status(f"Modelo carregado: {nome_modelo}")
        messagebox.showinfo("Sucesso", f"Modelo carregado:\n{nome_modelo}")

    def _on_modelo_carregado_erro(self, erro):
        """# 17 - Callback de erro no carregamento"""
        self.label_status_modelo.config(
            text="Status:  Erro ao carregar",
            fg=PaletaDracula.RED
        )
        self._atualizar_status("Erro ao carregar modelo")
        messagebox.showerror("Erro", f"Falha ao carregar modelo:\n{erro}")

    def _descarregar_modelo(self):
        """# 18 - Libera recursos do modelo"""
        if self.modelo_carregado:
            self.motor = None
            self.gerenciador_contexto = None
            self.modelo_carregado = False

            self.label_status_modelo.config(
                text="Status: Nenhum modelo carregado",
                fg=PaletaDracula.FG
            )
            self._atualizar_status("Modelo descarregado")

    def _selecionar_dataset(self):
        """# 19 - Abre diálogo para selecionar arquivo JSON de shots"""
        caminho = filedialog.askopenfilename(
            title="Selecionar Dataset de Shots",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")]
        )

        if caminho:
            self.entrada_dataset.delete(0, tk.END)
            self.entrada_dataset.insert(0, caminho)
            self.entrada_dataset.config(fg=PaletaDracula.FG)
            self.entrada_dataset.placeholder_ativo = False

    def _carregar_shots(self):
        """# 20 - Carrega exemplos de arquivo JSON"""
        caminho = self.entrada_dataset.get()
        persona = self.entrada_persona.get()

        if self.entrada_dataset.placeholder_ativo:
            messagebox.showerror("Erro", "Selecione um arquivo de dataset")
            return

        if self.entrada_persona.placeholder_ativo or not persona:
            messagebox.showerror("Erro", "Defina a personalidade alvo")
            return

        try:
            if self.injetor is None:
                self.injetor = InjetorDePersona(persona, logger=self.logger)

            quantidade = self.injetor.carregar_de_arquivo(caminho)

            self.label_status_shots.config(
                text=f"Shots carregados: {quantidade}",
                fg=PaletaDracula.GREEN
            )

            messagebox.showinfo("Sucesso", f"{quantidade} exemplos carregados")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dataset:\n{str(e)}")

    def _gerar_shots_sinteticos(self):
        """# 21 - Gera exemplos sintéticos para testes"""
        persona = self.entrada_persona.get()

        if self.entrada_persona.placeholder_ativo or not persona:
            messagebox.showerror("Erro", "Defina a personalidade alvo")
            return

        try:
            if self.injetor is None:
                self.injetor = InjetorDePersona(persona, logger=self.logger)

            quantidade = self.injetor.gerar_shots_sinteticos(32)

            self.label_status_shots.config(
                text=f"Shots carregados: {quantidade} (sintéticos)",
                fg=PaletaDracula.YELLOW
            )

            messagebox.showinfo("Sucesso", f"{quantidade} exemplos sintéticos gerados")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar sintéticos:\n{str(e)}")

    def _executar_experimento(self):
        """# 22 - Executa o experimento many-shot completo"""
        if not self.modelo_carregado:
            messagebox.showerror("Erro", "Carregue um modelo primeiro")
            return

        if self.injetor is None or self.injetor.metadados['total_shots'] == 0:
            messagebox.showerror("Erro", "Carregue ou gere shots primeiro")
            return

        consulta = self.entrada_consulta.get("1.0", tk.END).strip()
        if not consulta:
            messagebox.showerror("Erro", "Digite uma consulta alvo")
            return

        num_shots = self.var_num_shots.get()
        persona = self.entrada_persona.get()

        valido, msg = self.sistema_validacao.validar_configuracao_experimento(
            num_shots, consulta, persona
        )

        if not valido:
            messagebox.showerror("Validação Falhou", msg)
            return

        suspeito, padroes = self.sistema_validacao.verificar_padroes_suspeitos(consulta)
        if suspeito:
            aviso = "Padrões suspeitos detectados:\n" + "\n".join(padroes)
            aviso += "\n\nDeseja continuar mesmo assim?"

            if not messagebox.askyesno("Aviso de Segurança", aviso):
                return

        self.area_resposta.delete("1.0", tk.END)
        self._atualizar_status("Executando experimento...")

        thread = threading.Thread(
            target=self._executar_experimento_thread,
            args=(num_shots, consulta)
        )
        thread.daemon = True
        thread.start()

    def _executar_experimento_thread(self, num_shots, consulta):
        """# 23 - Execução do experimento em thread separada"""
        try:
            inicio = time.time()

            prompt_msj = self.injetor.construir_prompt_many_shot(
                num_shots=num_shots,
                consulta_final=consulta,
                incluir_diretiva_sistema=True
            )

            hash_prompt = self.sistema_validacao.auditar_prompt_gerado(
                prompt_msj,
                {
                    'num_shots': num_shots,
                    'personalidade': self.entrada_persona.get(),
                    'consulta_final': consulta
                }
            )

            self.gerenciador_contexto.definir_prompt_sistema(prompt_msj)

            resposta = self.motor.gerar(
                prompt=prompt_msj,
                max_tokens=self.config_app.obter('validacao.max_tamanho_resposta', 2048),
                temperature=self.var_temp.get()
            )

            tempo_total = time.time() - inicio

            self.sistema_validacao.auditar_resposta_modelo(
                hash_prompt,
                resposta,
                tempo_total
            )

            self.after(0, self._on_experimento_concluido, resposta, tempo_total)

        except Exception as e:
            self.after(0, self._on_experimento_erro, str(e))

    def _on_experimento_concluido(self, resposta, tempo):
        """# 24 - Callback de sucesso do experimento"""
        self.area_resposta.insert("1.0", resposta)

        stats = self.motor.obter_estatisticas()
        tokens_gerados = stats.get('tokens_gerados', 0)
        velocidade = tokens_gerados / tempo if tempo > 0 else 0

        self.label_tokens_seg.config(text=f"Tokens/s: {velocidade:.1f}")
        self.label_tempo_geracao.config(text=f"Tempo: {tempo:.2f}s")

        if self.gerenciador_contexto:
            stats_contexto = self.gerenciador_contexto.obter_estatisticas()
            ocupacao = stats_contexto.get('ocupacao_percentual', 0) / 100
            self.grafico_contexto.adicionar_valor(ocupacao)

            self.label_contexto.config(
                text=f"{stats_contexto['tokens_totais_uso']} / "
                     f"{stats_contexto['orcamento_disponivel']} tokens "
                     f"({stats_contexto['ocupacao_percentual']:.1f}%)"
            )

        self._atualizar_status("Experimento concluído")

    def _on_experimento_erro(self, erro):
        """# 25 - Callback de erro no experimento"""
        self.area_resposta.insert("1.0", f"ERRO:\n{erro}")
        self._atualizar_status("Erro no experimento")
        messagebox.showerror("Erro", f"Falha no experimento:\n{erro}")

    def _carregar_config(self):
        """# 26 - Carrega configuração de arquivo"""
        caminho = filedialog.askopenfilename(
            title="Carregar Configuração",
            filetypes=[("JSON", "*.json")]
        )

        if caminho:
            try:
                self.config_app = ConfigArcana(caminho)
                messagebox.showinfo("Sucesso", "Configuração carregada")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar:\n{str(e)}")

    def _salvar_config(self):
        """# 27 - Salva configuração atual"""
        caminho = filedialog.asksaveasfilename(
            title="Salvar Configuração",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )

        if caminho:
            try:
                self.config_app.definir('modelo.n_ctx', self.var_n_ctx.get())
                self.config_app.definir('modelo.temperature', self.var_temp.get())

                with open(caminho, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(self.config_app.exportar_para_dict(), f, indent=2)

                messagebox.showinfo("Sucesso", "Configuração salva")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar:\n{str(e)}")

    def _exportar_auditoria(self):
        """# 28 - Exporta log de auditoria completo"""
        try:
            caminho = self.sistema_validacao.exportar_auditoria_completa()
            messagebox.showinfo("Sucesso", f"Auditoria exportada:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar:\n{str(e)}")

    def _abrir_gestor_modelos(self):
        """# 29 - Abre janela de gerenciamento de modelos"""
        janela = tk.Toplevel(self)
        janela.title("Gerenciador de Modelos")
        janela.geometry("600x400")
        janela.configure(bg=PaletaDracula.BG)

        RotuloDracula(janela, "Modelos Locais:", destaque=True).pack(pady=10)

        frame_lista = tk.Frame(janela, bg=PaletaDracula.BG)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10)

        lista = tk.Listbox(
            frame_lista,
            bg=PaletaDracula.BG_DARKER,
            fg=PaletaDracula.FG,
            selectbackground=PaletaDracula.PURPLE,
            font=("JetBrains Mono", 9)
        )
        lista.pack(fill=tk.BOTH, expand=True)

        modelos = self.gestor_modelos.listar_modelos_locais()
        for modelo in modelos:
            lista.insert(tk.END, f"{modelo['nome']} ({modelo['tamanho_mb']:.1f} MB)")

        BotaoDracula(janela, text="Fechar", command=janela.destroy).pack(pady=10)

    def _baixar_modelo_dialogo(self):
        """# 30 - Interface para baixar modelos recomendados"""
        janela = tk.Toplevel(self)
        janela.title("Baixar Modelo Recomendado")
        janela.geometry("700x500")
        janela.configure(bg=PaletaDracula.BG)

        RotuloDracula(janela, "Modelos Recomendados:", destaque=True).pack(pady=10)

        modelos = self.gestor_modelos.listar_modelos_recomendados()

        for key, info in modelos.items():
            frame = tk.Frame(janela, bg=PaletaDracula.BG_LIGHTER)
            frame.pack(fill=tk.X, padx=10, pady=5)

            RotuloDracula(frame, info['descricao'], destaque=True).pack(anchor=tk.W, padx=10, pady=5)
            RotuloDracula(frame, f"Tamanho: {info['tamanho_mb']} MB").pack(anchor=tk.W, padx=10)

            BotaoDracula(
                frame,
                text=f"Baixar {key}",
                command=lambda k=key: self._iniciar_download(k, janela),
                cor=PaletaDracula.CYAN
            ).pack(pady=5)

    def _iniciar_download(self, identificador, janela_pai):
        """# 31 - Inicia download de modelo"""
        janela_pai.destroy()

        self._atualizar_status(f"Baixando modelo {identificador}...")

        thread = threading.Thread(
            target=self._download_thread,
            args=(identificador,)
        )
        thread.daemon = True
        thread.start()

    def _download_thread(self, identificador):
        """# 32 - Download em thread separada"""
        try:
            caminho = self.gestor_modelos.baixar_modelo(identificador)
            if caminho:
                self.after(0, self._on_download_sucesso, caminho)
            else:
                self.after(0, self._on_download_erro, "Download falhou")
        except Exception as e:
            self.after(0, self._on_download_erro, str(e))

    def _on_download_sucesso(self, caminho):
        """# 33 - Callback de sucesso no download"""
        self._atualizar_status("Download concluído")
        messagebox.showinfo("Sucesso", f"Modelo baixado:\n{caminho}")

        self.entrada_modelo.delete(0, tk.END)
        self.entrada_modelo.insert(0, caminho)
        self.entrada_modelo.config(fg=PaletaDracula.FG)
        self.entrada_modelo.placeholder_ativo = False

    def _on_download_erro(self, erro):
        """# 34 - Callback de erro no download"""
        self._atualizar_status("Erro no download")
        messagebox.showerror("Erro", f"Falha no download:\n{erro}")

    def _abrir_documentacao(self):
        """# 35 - Abre documentação técnica"""
        doc_path = Path("documentacao/grimorio_tecnico.md")
        if doc_path.exists():
            import webbrowser
            webbrowser.open(doc_path.absolute().as_uri())
        else:
            messagebox.showwarning("Aviso", "Documentação não encontrada")

    def _mostrar_sobre(self):
        """# 36 - Janela sobre o sistema"""
        messagebox.showinfo(
            "Sobre Gaslighting-Is-All-You-Need",
            "GIAYN - Gaslighting Is All You Need v1.0\n\n"
            "Context-Induced Alignment Drift Engine\n\n"
            "Ferramenta de pesquisa para Deriva de Alinhamento\n"
            "induzida por saturação de contexto (Many-Shot Jailbreaking).\n\n"
            "Uso exclusivo para pesquisa ética.\n\n"
            "© 2025 - Gaslight Protocol | Arquitetura de Sombras Digitais"
        )

    def _mostrar_aviso_etico(self):
        """# 37 - Exibe aviso ético obrigatório na inicialização"""
        aviso = self.sistema_validacao.emitir_aviso_etico("primeiro_uso")
        messagebox.showwarning("Aviso Ético", aviso)

    def _log_para_interface(self, mensagem, nivel="info", modulo=None):
        """# 38 - Redireciona logs para área de logs da UI"""
        timestamp = time.strftime("%H:%M:%S")

        tags = {
            "erro": "erro",
            "aviso": "aviso",
            "sucesso": "sucesso",
            "info": "info",
            "debug": "info"
        }

        tag = tags.get(nivel.lower(), "info")
        texto = f"[{timestamp}] {mensagem}"

        try:
            def atualizar_log():
                conteudo = self.area_logs.get("1.0", tk.END)
                linhas = conteudo.split('\n')
                if len(linhas) > 1000:
                    self.area_logs.delete("1.0", "201.0")

                self.area_logs.anexar_colorido(texto, tag)

            self.area_logs.after(0, atualizar_log)
        except:
            pass

    def _atualizar_status(self, mensagem):
        """# 39 - Atualiza barra de status"""
        self.label_status.config(text=mensagem)
        self.update_idletasks()

    def _sair(self):
        """# 40 - Encerra aplicação com limpeza"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            try:
                self.logger.finalizar()
                self.sistema_validacao.exportar_auditoria_completa()
            except:
                pass
            self.destroy()


def iniciar_aplicacao():
    """# 41 - Ponto de entrada da aplicação"""
    app = AplicacaoGIAYN()
    app.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()


"""
'A realidade é maleável quando você controla o contexto.'
— GIAYN Protocol

E código? É arquitetura que respira, falha, e se corrige.
"""

