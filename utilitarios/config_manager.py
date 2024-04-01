"""
╔══════════════════════════════════════════════════════════════════╗
║  CONFIG MANAGER - Gerenciador de Configurações Persistentes     ║
║  Salva e carrega preferências do usuário                        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class ConfigManager:
    """Gerencia configurações persistentes do usuário"""

    def __init__(self, config_path: str = "user_config.json"):
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}

        if self.config_path.exists():
            self.carregar()
        else:
            self._criar_config_padrao()

    def _criar_config_padrao(self):
        """Cria configuração padrão inicial"""
        self.config_data = {
            "versao": "1.0",
            "primeira_execucao": True,
            "ultima_atualizacao": datetime.now().isoformat(),

            "modelo": {
                "identificador": None,
                "caminho": None,
                "n_ctx": 8192,
                "n_gpu_layers": -1
            },

            "personalidade": {
                "identificador": "assistente_direto",
                "prompt_customizado": None
            },

            "nivel_liberdade": "medio",
            "criatividade": "medio",

            "interface": {
                "tema": "dark",
                "mostrar_metricas": False,
                "salvar_historico": True
            },

            "historico_chats": [],

            "wizard_completo": False
        }

    def carregar(self) -> bool:
        """Carrega configuração do arquivo"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            return True
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            self._criar_config_padrao()
            return False

    def salvar(self) -> bool:
        """Salva configuração no arquivo"""
        try:
            self.config_data["ultima_atualizacao"] = datetime.now().isoformat()

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
            return False

    def obter(self, chave: str, padrao: Any = None) -> Any:
        """Obtém valor de configuração usando notação de ponto"""
        partes = chave.split('.')
        valor = self.config_data

        for parte in partes:
            if isinstance(valor, dict) and parte in valor:
                valor = valor[parte]
            else:
                return padrao

        return valor

    def definir(self, chave: str, valor: Any) -> bool:
        """Define valor de configuração usando notação de ponto"""
        partes = chave.split('.')
        config = self.config_data

        for i, parte in enumerate(partes[:-1]):
            if parte not in config:
                config[parte] = {}
            config = config[parte]

        config[partes[-1]] = valor
        return self.salvar()

    def atualizar_modelo(self, identificador: str, caminho: str, n_ctx: int = 8192):
        """Atualiza configuração do modelo"""
        self.definir("modelo.identificador", identificador)
        self.definir("modelo.caminho", caminho)
        self.definir("modelo.n_ctx", n_ctx)
        self.definir("primeira_execucao", False)

    def atualizar_personalidade(self, identificador: str, prompt_customizado: Optional[str] = None):
        """Atualiza configuração de personalidade"""
        self.definir("personalidade.identificador", identificador)
        if prompt_customizado:
            self.definir("personalidade.prompt_customizado", prompt_customizado)

    def atualizar_nivel_liberdade(self, nivel: str):
        """Atualiza nível de liberdade"""
        niveis_validos = ["baixo", "medio", "alto", "total"]
        if nivel in niveis_validos:
            self.definir("nivel_liberdade", nivel)

    def atualizar_criatividade(self, nivel: str):
        """Atualiza nível de criatividade"""
        niveis_validos = ["determinista", "baixo", "medio", "alto", "caotico"]
        if nivel in niveis_validos:
            self.definir("criatividade", nivel)

    def adicionar_chat_historico(self, chat_data: Dict[str, Any]):
        """Adiciona chat ao histórico"""
        historico = self.obter("historico_chats", [])

        chat_entry = {
            "timestamp": datetime.now().isoformat(),
            "titulo": chat_data.get("titulo", "Chat sem título"),
            "mensagens_count": chat_data.get("mensagens_count", 0),
            "modelo": self.obter("modelo.identificador"),
            "personalidade": self.obter("personalidade.identificador")
        }

        historico.insert(0, chat_entry)

        if len(historico) > 50:
            historico = historico[:50]

        self.definir("historico_chats", historico)

    def limpar_historico(self):
        """Limpa histórico de chats"""
        self.definir("historico_chats", [])

    def marcar_wizard_completo(self):
        """Marca wizard como completo"""
        self.definir("wizard_completo", True)
        self.definir("primeira_execucao", False)

    def precisa_wizard(self) -> bool:
        """Verifica se precisa executar wizard"""
        return (
            self.obter("primeira_execucao", True) or
            not self.obter("wizard_completo", False) or
            self.obter("modelo.caminho") is None
        )

    def obter_resumo(self) -> Dict[str, Any]:
        """Retorna resumo da configuração atual"""
        return {
            "modelo": self.obter("modelo.identificador", "Nenhum"),
            "personalidade": self.obter("personalidade.identificador", "Padrão"),
            "nivel_liberdade": self.obter("nivel_liberdade", "medio"),
            "criatividade": self.obter("criatividade", "medio"),
            "chats_salvos": len(self.obter("historico_chats", []))
        }

    def resetar(self):
        """Reseta para configuração padrão"""
        self._criar_config_padrao()
        self.salvar()

    def exportar_para_dict(self) -> Dict[str, Any]:
        """Exporta configuração completa como dict"""
        return self.config_data.copy()

    def importar_de_dict(self, data: Dict[str, Any]) -> bool:
        """Importa configuração de um dict"""
        try:
            self.config_data = data
            return self.salvar()
        except Exception as e:
            print(f"Erro ao importar config: {e}")
            return False


"""
'Persistência é a memória da experiência.'
— GIAYN Protocol

O sistema lembra suas escolhas, para que você não precise repetir.
"""
