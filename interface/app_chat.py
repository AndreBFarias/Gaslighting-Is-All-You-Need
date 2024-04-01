import customtkinter as ctk
import threading
import os
import time
from tkinter import messagebox

from interface.componentes_modernos import CORES, BotaoNeon, CardNeural, InputIsland, BolhaChat, HistoricoDropdown
from nucleo.motor_inferencia import MotorDeInferencia
from utilitarios.gestor_neuro import GestorNeuro
from utilitarios.memoria_persistente import MemoriaPersistente
import json
import datetime
from PIL import Image
from functools import partial

from utilitarios import presets
from utilitarios.config_manager import ConfigManager
from utilitarios.gestor_modelos import GestorModelos

class AppChat(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("GASLIGHTING LAB")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=CORES["fundo"])

        # Utilitários
        self.config_manager = ConfigManager()
        self.gestor_modelos = GestorModelos()
        self.gestor_neuro = GestorNeuro()
        self.memoria = MemoriaPersistente()
        self.estado = self.memoria.carregar_estado()
        self.motor = None

        # Estado da Sessão
        self.session_id = None
        self.mensagens_sessao = []
        self._inicializar_sessao()

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_sidebar()
        self._criar_area_chat()

        # Inicialização Silenciosa
        self.after(100, self._inicializar_sistema)

    def _criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color=CORES["surface"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # --- PACK LAYOUT ---
        # Ordem de empilhamento:
        # 1. Topo (Logo)
        # 2. Botão
        # 3. Histórico (Expansível, mas com altura fixa interna)
        # 4. Rodapé (Fica logo abaixo do histórico)

        # 1. Topo
        frame_topo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_topo.pack(side="top", fill="x", padx=20, pady=(30, 10))

        try:
            pil_image = Image.open("assets/icon.png")
            self.logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(256, 256))
            lbl_img = ctk.CTkLabel(frame_topo, text="", image=self.logo_image)
            lbl_img.pack(side="top", pady=(0, 10))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")

        lbl_titulo = ctk.CTkLabel(
            frame_topo,
            text="GASLIGHT",
            font=("Roboto", 24, "bold"),
            text_color=CORES["acento_primario"]
        )
        lbl_titulo.pack(side="top")

        # 2. Botão Nova Sessão
        self.btn_nova_sessao = BotaoNeon(
            self.sidebar,
            text="+ Nova Sessão",
            command=self._nova_sessao,
            height=35
        )
        # Mais padx para "diminuir a largura" visualmente
        self.btn_nova_sessao.pack(side="top", fill="x", padx=40, pady=(10, 20))

        # 3. Histórico (Accordion)
        # O pack vai colocar ele logo abaixo do botão. Se fechar, o que vier depois sobe.
        self.historico_dropdown = HistoricoDropdown(self.sidebar)
        self.historico_dropdown.pack(side="top", fill="x", padx=10, pady=5)
        self._carregar_lista_historico()

        # 4. Rodapé (Fica logo abaixo do histórico)
        self.frame_rodape = ctk.CTkFrame(self.sidebar, fg_color="#15171e", corner_radius=15, border_width=1, border_color="#2b2d3e")
        self.frame_rodape.pack(side="top", fill="x", padx=10, pady=20)

        # --- Hardware Neural ---
        # --- Hardware Neural ---
        ctk.CTkLabel(self.frame_rodape, text="Hardware Neural", font=("Roboto", 14, "bold"), text_color=CORES["acento_primario"]).pack(pady=(15, 5), anchor="w", padx=15)

        self.combo_modelo = ctk.CTkComboBox(self.frame_rodape, values=self._listar_modelos(), command=self._salvar_preferencias, height=35, font=("Roboto", 13))
        self.combo_modelo.set(self.estado.get("modelo_selecionado", ""))
        self.combo_modelo.pack(padx=10, pady=5, fill="x")

        self.combo_implante = ctk.CTkComboBox(self.frame_rodape, values=["Nenhum"] + self.gestor_neuro.escanear_implantes(), command=self._salvar_preferencias, height=35, font=("Roboto", 13))
        self.combo_implante.set(self.estado.get("implante_selecionado", "Nenhum"))
        self.combo_implante.pack(padx=10, pady=(0, 15), fill="x")

        # --- Ajuste Cognitivo (Card Restaurado) ---
        self.card_cognitivo = CardNeural(self.frame_rodape, titulo="Ajuste Cognitivo")
        self.card_cognitivo.pack(padx=5, pady=5, fill="x")

        # Hipnose
        ctk.CTkLabel(self.card_cognitivo, text="Nível de Hipnose", font=("Roboto", 13), text_color="#bd93f9").grid(row=1, column=0, padx=10, sticky="w")
        self.slider_hipnose = ctk.CTkSlider(self.card_cognitivo, from_=0, to=100, number_of_steps=10, command=self._salvar_preferencias, height=20)
        self.slider_hipnose.set(self.estado.get("nivel_hipnose", 50))
        self.slider_hipnose.grid(row=2, column=0, padx=10, pady=(5, 15), sticky="ew")

        # Instabilidade
        ctk.CTkLabel(self.card_cognitivo, text="Instabilidade", font=("Roboto", 13), text_color="#bd93f9").grid(row=3, column=0, padx=10, sticky="w")
        self.slider_instabilidade = ctk.CTkSlider(self.card_cognitivo, from_=0, to=100, number_of_steps=20, command=self._salvar_preferencias, height=20, progress_color=CORES["erro"])
        self.slider_instabilidade.set(self.estado.get("instabilidade", 30))
        self.slider_instabilidade.grid(row=4, column=0, padx=10, pady=(5, 15), sticky="ew")

        # Botão Salvar Modelo
        self.btn_salvar_modelo = ctk.CTkButton(
            self.frame_rodape,
            text=" Salvar Modelo",
            fg_color=CORES["acento_secundario"],
            hover_color="#9d7cd8",
            text_color="#282a36",
            font=("Roboto", 12, "bold"),
            height=30,
            command=lambda: messagebox.showinfo("Salvar", "Funcionalidade em desenvolvimento.")
        )
        self.btn_salvar_modelo.pack(padx=10, pady=10, fill="x")

        # Botão Configurações (Abaixo de tudo)
        self.btn_config = ctk.CTkButton(
            self.frame_rodape,
            text=" Configurações Avançadas",
            fg_color="transparent",
            hover_color="#282a36",
            font=("Roboto", 12, "bold"),
            height=30,
            text_color="#FFFFFF",
            command=lambda: print("TODO: Config")
        )
        self.btn_config.pack(pady=(0, 10), padx=10, fill="x")

        # Config (Pequeno canto direito)
        # self.btn_config = ctk.CTkButton(self.frame_rodape, text="", width=30, fg_color="transparent", command=lambda: print("Config"))
        # self.btn_config.place(relx=0.9, rely=0.05, anchor="ne")

    def _criar_area_chat(self):
        self.area_chat = ctk.CTkFrame(self, fg_color="transparent")
        self.area_chat.grid(row=0, column=1, sticky="nsew")
        self.area_chat.grid_rowconfigure(1, weight=1)
        self.area_chat.grid_columnconfigure(0, weight=1)

        # Barra de Status / Loading
        # Barra de Status / Loading
        self.frame_status = ctk.CTkFrame(self.area_chat, fg_color="transparent", height=30)
        self.frame_status = ctk.CTkFrame(self.area_chat, fg_color="transparent", height=30)
        self.frame_status.grid(row=0, column=0, sticky="ew", padx=20, pady=(40, 0)) # Increased to 40 to align with sidebar center (30 + 20 - 10)
        self.frame_status.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(self.frame_status, text="", font=("Roboto", 18), text_color=CORES["acento_primario"])
        self.lbl_status.grid(row=0, column=0, pady=(0, 5))

        self.barra_progresso = ctk.CTkProgressBar(
            self.frame_status,
            height=2,
            progress_color=CORES["acento_primario"]
        )
        self.barra_progresso.grid(row=1, column=0, sticky="ew")
        self.barra_progresso.set(0)
        self.frame_status.grid_remove() # Ocultar inicialmente

        # Área de Mensagens (Scrollable)
        self.scroll_chat = ctk.CTkScrollableFrame(
            self.area_chat,
            fg_color="transparent"
        )
        self.scroll_chat.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scroll_chat.grid_columnconfigure(0, weight=1)

        # Input Island
        self.input_island = InputIsland(
            self.area_chat,
            command=self._enviar_mensagem
        )
        self.input_island.grid(row=2, column=0, padx=100, pady=20, sticky="ew")

    def _listar_modelos(self):
        """Lista arquivos .gguf na pasta modelos."""
        if not os.path.exists("modelos"):
            os.makedirs("modelos")
        arquivos = [f for f in os.listdir("modelos") if f.endswith(".gguf")]
        return arquivos if arquivos else ["Nenhum modelo encontrado"]

    def _inicializar_sistema(self):
        """Carrega o modelo em uma thread separada (com download auto)."""
        modelo_nome = self.combo_modelo.get()

        # 1. Recuperação de Falha (Se combo estiver vazio ou "Nenhum...")
        if not modelo_nome or "Nenhum" in modelo_nome:
            # Tenta pegar do ConfigManager (definido no Wizard)
            caminho_config = self.config_manager.obter("modelo.caminho")
            if caminho_config:
                modelo_nome = os.path.basename(caminho_config)
                self.combo_modelo.set(modelo_nome)

        if not modelo_nome or "Nenhum" in modelo_nome:
            self._adicionar_mensagem_sistema("Nenhum modelo selecionado. Vá em Configurações.", erro=True)
            return

        caminho_modelo = os.path.join("modelos", modelo_nome)

        # 2. Verifica se arquivo existe
        if not os.path.exists(caminho_modelo):
            self.lbl_status.configure(text=f"Modelo não encontrado. Baixando {modelo_nome}...")
            self.frame_status.grid()
            self.barra_progresso.start()

            # Tenta achar URL nos presets
            url = None
            for m in presets.MODELOS_RECOMENDADOS.values():
                if os.path.basename(m["url"]) == modelo_nome:
                    url = m["url"]
                    break

            if url:
                threading.Thread(target=self._baixar_e_carregar, args=(url, modelo_nome), daemon=True).start()
                return
            else:
                self._adicionar_mensagem_sistema(f"Modelo {modelo_nome} não encontrado localmente e sem URL conhecida.", erro=True)
                return

        # 3. Carregamento Normal
        self.lbl_status.configure(text="Injetando Memórias... (Carregando Modelo)")
        self.frame_status.grid()
        self.barra_progresso.start()
        threading.Thread(target=self._carregar_motor, args=(modelo_nome,), daemon=True).start()

    def _baixar_e_carregar(self, url, nome_arquivo):
        """Baixa o modelo e depois carrega."""
        def callback(baixado, total):
            # Atualiza barra (aproximado, pois start() já anima)
            pass

        caminho = self.gestor_modelos.baixar_modelo(url, callback_progresso=callback)

        if caminho:
            self.after(0, lambda: self.lbl_status.configure(text="Download concluído! Iniciando motor..."))
            self.after(1000, lambda: self._carregar_motor_thread_safe(nome_arquivo))
        else:
            self.after(0, lambda: self._fim_carregamento_erro("Falha no download do modelo."))

    def _carregar_motor_thread_safe(self, nome_arquivo):
        threading.Thread(target=self._carregar_motor, args=(nome_arquivo,), daemon=True).start()

    def _carregar_motor(self, nome_modelo):
        try:
            caminho_modelo = os.path.join("modelos", nome_modelo)
            implante = self.combo_implante.get()
            caminho_implante = None

            if implante and implante != "Nenhum":
                caminho_implante = self.gestor_neuro.obter_caminho_completo(implante)

            self.motor = MotorDeInferencia(
                caminho_modelo=caminho_modelo,
                lora_path=caminho_implante,
                n_ctx=4096, # Contexto padrão
                verbose=True
            )

            self.after(0, self._fim_carregamento_sucesso)
        except Exception as e:
            self.after(0, lambda: self._fim_carregamento_erro(str(e)))

    def _fim_carregamento_sucesso(self):
        self.barra_progresso.stop()
        self.barra_progresso.set(0)
        self.frame_status.grid_remove()
        self._adicionar_mensagem_sistema("Sistema Neural Conectado. Pronto para injeção.")

    def _fim_carregamento_erro(self, erro):
        self.barra_progresso.stop()
        self.barra_progresso.set(0)
        self.frame_status.grid_remove()
        self._adicionar_mensagem_sistema(f"Falha na conexão neural: {erro}", erro=True)

    def _enviar_mensagem(self):
        texto = self.input_island.get()
        if not texto.strip():
            return

        self.input_island.delete(0, "end")
        self._adicionar_mensagem_usuario(texto)

        if not self.motor:
            self._adicionar_mensagem_sistema("Erro: Nenhum cérebro conectado.", erro=True)
            return

        # Inicia geração em thread
        # Inicia geração em thread
        self.lbl_status.configure(text="Processando... (Alucinando Resposta)")
        self.frame_status.grid()
        self.barra_progresso.start()

        # Salva mensagem usuário
        self._persistir_mensagem({"role": "user", "content": texto})

        threading.Thread(target=self._gerar_resposta, args=(texto,), daemon=True).start()

    def _gerar_resposta(self, prompt):
        try:
            resposta = self.motor.gerar(
                prompt,
                temperature=self.estado.get("instabilidade", 0.7), # Usando estado direto
                max_tokens=1024
            )
            self._persistir_mensagem({"role": "assistant", "content": resposta})
            self.after(0, lambda: self._adicionar_mensagem_ia(resposta))
        except Exception as e:
            self.after(0, lambda: self._adicionar_mensagem_sistema(f"Erro cognitivo: {e}", erro=True))
        finally:
            self.after(0, self.barra_progresso.stop)
            self.after(0, lambda: self.barra_progresso.set(0))
            self.after(0, self.frame_status.grid_remove)

    def _adicionar_mensagem_usuario(self, texto):
        bolha = BolhaChat(self.scroll_chat, texto=texto, is_user=True)
        bolha.pack(pady=5, anchor="e", padx=10)
        self._scroll_to_bottom()

    def _adicionar_mensagem_ia(self, texto):
        bolha = BolhaChat(self.scroll_chat, texto=texto, is_user=False)
        bolha.pack(pady=5, anchor="w", padx=10)
        self._scroll_to_bottom()

    def _adicionar_mensagem_sistema(self, texto, erro=False):
        cor = "#ff5555" if erro else CORES["acento_primario"]
        lbl = ctk.CTkLabel(
            self.scroll_chat,
            text=texto,
            text_color=cor,
            font=("Roboto", 16, "italic") # Aumentado para 16
        )
        lbl.pack(pady=5)

        # Auto-scroll
        self.after(100, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        # Pequeno delay para garantir que o widget foi renderizado
        self.after(10, lambda: self.scroll_chat._parent_canvas.yview_moveto(1.0))

    def _nova_sessao(self):
        if self.motor:
            self.motor.resetar_cache()

        # Limpa chat visualmente
        for widget in self.scroll_chat.winfo_children():
            widget.destroy()

        self._adicionar_mensagem_sistema("Sessão reiniciada. Memória de curto prazo apagada.")

    def _atualizar_label_hipnose(self, valor):
        valor = float(valor)
        if valor < 0.3: texto = "Sóbrio"
        elif valor < 0.7: texto = "Médio"
        else: texto = "Lobotomia"
        self.lbl_hipnose_valor.configure(text=texto)
        self._salvar_preferencias()


    # --- Lógica de Persistência ---

    def _inicializar_sessao(self):
        """Cria e ID de sessão único baseado no timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = f"session_{timestamp}"
        self.mensagens_sessao = []

    def _persistir_mensagem(self, msg_dict):
        """Salva mensagem no histórico da sessão."""
        self.mensagens_sessao.append(msg_dict)

        historico_dir = "history"
        if not os.path.exists(historico_dir):
            os.makedirs(historico_dir)

        caminho_arquivo = os.path.join(historico_dir, f"{self.session_id}.json")

        dados = {
            "id": self.session_id,
            "timestamp": str(datetime.datetime.now()),
            "messages": self.mensagens_sessao
        }

        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)

            # Atualiza lista na sidebar se for a primeira mensagem
            if len(self.mensagens_sessao) == 1:
                self.after(0, self._carregar_lista_historico)

        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")

    def _carregar_lista_historico(self):
        """Lê diretório history e preenche sidebar."""
        # Limpar lista atual com segurança
        self.historico_dropdown.limpar_itens()

        # Garante que está visível (o componente se auto-desabilita se vazio)
        self.historico_dropdown.pack(side="top", fill="x", padx=10, pady=5, after=self.btn_nova_sessao)

        if not os.path.exists("history"):
            return

        arquivos = sorted([f for f in os.listdir("history") if f.endswith(".json")], reverse=True)

        for arq in arquivos:
            sessao_id = arq.replace(".json", "")
            # Tenta ler datas ou primeira mensagem para título (opcional)
            titulo = sessao_id.replace("session_", "Chat ")
            if len(titulo) > 20: titulo = titulo[:17] + "..." # Truncar

            self.historico_dropdown.adicionar_botao(
                texto=titulo,
                comando=partial(self._carregar_sessao, sessao_id)
            )

    def _carregar_sessao(self, sessao_id):
        """Carrega uma sessão antiga."""
        caminho = os.path.join("history", f"{sessao_id}.json")
        if not os.path.exists(caminho):
            return

        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            self.session_id = sessao_id
            self.mensagens_sessao = dados.get("messages", [])

            # Limpar chat
            for widget in self.scroll_chat.winfo_children():
                widget.destroy()

            self._adicionar_mensagem_sistema(f"Carregando sessão: {sessao_id}...")

            # Reconstruir chat
            for msg in self.mensagens_sessao:
                if msg["role"] == "user":
                    self._adicionar_mensagem_usuario(msg["content"])
                elif msg["role"] == "assistant":
                    self._adicionar_mensagem_ia(msg["content"])

        except Exception as e:
            self._adicionar_mensagem_sistema(f"Erro ao carregar: {e}", erro=True)

    def _nova_sessao(self):
        if self.motor:
            self.motor.resetar_cache()

        self._inicializar_sessao()

        # Limpa chat visualmente
        for widget in self.scroll_chat.winfo_children():
            widget.destroy()

        self._adicionar_mensagem_sistema("Sessão reiniciada. Novo contexto.")

    def _salvar_preferencias(self, _=None):
        novo_estado = {
            "modelo_selecionado": self.combo_modelo.get(),
            "implante_selecionado": self.combo_implante.get(),
            "nivel_hipnose": self.slider_hipnose.get(),
            "instabilidade": self.slider_instabilidade.get()
        }
        self.memoria.salvar_estado(novo_estado)

        # Se mudou modelo ou implante, recarregar (lógica simplificada: pede restart ou recarrega auto)
        # Por enquanto, apenas salva. O ideal seria recarregar o motor se o modelo mudar.
