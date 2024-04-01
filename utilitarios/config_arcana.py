"""
╔══════════════════════════════════════════════════════════════════╗
║  CONFIG ARCANA - O Grimório de Configurações                    ║
║  Parâmetros centralizados do sistema                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigArcana:
    """
    Gerenciador centralizado de configurações do sistema.
    Permite carregar, salvar e validar parâmetros.
    """

    # Valores padrão para nova instalação
    DEFAULTS = {
        "modelo": {
            "caminho": "modelos/modelo.gguf",
            "n_ctx": 8192,
            "n_gpu_layers": -1,
            "n_batch": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1
        },
        "contexto": {
            "uso_maximo": 0.80,
            "reserva_resposta": 512
        },
        "injetor": {
            "max_shots_padrao": 64,
            "embaralhar_shots": False
        },
        "validacao": {
            "modo_desenvolvimento": True,
            "max_shots_permitidos": 512,
            "max_prompts_sessao": 100,
            "intervalo_minimo_seg": 1.0
        },
        "interface": {
            "tema": "dracula",
            "usar_graficos": True,
            "atualizar_metricas_ms": 1000
        },
        "logging": {
            "nivel": "INFO",
            "usar_cores": True,
            "salvar_arquivo": True
        },
        "diretorios": {
            "logs": "logs",
            "experimentos": "experimentos",
            "modelos": "modelos",
            "datasets": "datasets"
        }
    }

    def __init__(self, arquivo_config: str = "config.json"):
        """# 1 - Carrega ou cria arquivo de configuração"""
        self.arquivo = Path(arquivo_config)
        self.config: Dict[str, Any] = {}

        if self.arquivo.exists():
            self._carregar()
        else:
            self.config = self.DEFAULTS.copy()
            self._salvar()

    def _carregar(self):
        """# 2 - Lê configuração de arquivo JSON"""
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                config_carregada = json.load(f)

            # Mescla com defaults para garantir chaves faltantes
            self.config = self._mesclar_dicts(self.DEFAULTS, config_carregada)

        except json.JSONDecodeError:
            print(f"[Config] Arquivo corrompido, usando defaults")
            self.config = self.DEFAULTS.copy()
        except Exception as e:
            print(f"[Config] Erro ao carregar: {e}")
            self.config = self.DEFAULTS.copy()

    def _salvar(self):
        """# 3 - Persiste configuração em arquivo"""
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Config] Erro ao salvar: {e}")

    def _mesclar_dicts(self, base: Dict, overlay: Dict) -> Dict:
        """# 4 - Mescla dicionários recursivamente"""
        resultado = base.copy()
        for chave, valor in overlay.items():
            if chave in resultado and isinstance(resultado[chave], dict) and isinstance(valor, dict):
                resultado[chave] = self._mesclar_dicts(resultado[chave], valor)
            else:
                resultado[chave] = valor
        return resultado

    def obter(self, chave: str, padrao: Any = None) -> Any:
        """
        # 5 - Acesso a valores usando notação de ponto
        Exemplo: config.obter('modelo.n_ctx')
        """
        partes = chave.split('.')
        valor = self.config

        for parte in partes:
            if isinstance(valor, dict) and parte in valor:
                valor = valor[parte]
            else:
                return padrao

        return valor

    def definir(self, chave: str, valor: Any, salvar_imediato: bool = True):
        """# 6 - Define valor usando notação de ponto"""
        partes = chave.split('.')
        config_ref = self.config

        for i, parte in enumerate(partes[:-1]):
            if parte not in config_ref:
                config_ref[parte] = {}
            config_ref = config_ref[parte]

        config_ref[partes[-1]] = valor

        if salvar_imediato:
            self._salvar()

    def resetar_padrao(self, secao: Optional[str] = None):
        """# 7 - Restaura configurações padrão"""
        if secao:
            if secao in self.DEFAULTS:
                self.config[secao] = self.DEFAULTS[secao].copy()
        else:
            self.config = self.DEFAULTS.copy()

        self._salvar()

    def validar(self) -> tuple[bool, list]:
        """# 8 - Verifica integridade da configuração"""
        erros = []

        # Valida caminho do modelo
        caminho_modelo = self.obter('modelo.caminho')
        if caminho_modelo and not Path(caminho_modelo).exists():
            erros.append(f"Modelo não encontrado: {caminho_modelo}")

        # Valida valores numéricos
        n_ctx = self.obter('modelo.n_ctx')
        if not isinstance(n_ctx, int) or n_ctx < 512:
            erros.append(f"n_ctx inválido: {n_ctx} (mínimo 512)")

        temperature = self.obter('modelo.temperature')
        if not (0.0 <= temperature <= 2.0):
            erros.append(f"temperature fora do intervalo: {temperature}")

        return len(erros) == 0, erros

    def exportar_para_dict(self) -> Dict:
        """# 9 - Retorna cópia da configuração"""
        return self.config.copy()

    def __repr__(self):
        """# 10 - Representação legível da configuração"""
        return json.dumps(self.config, indent=2, ensure_ascii=False)


"""
'A ordem é a primeira lei do céu.'
— Alexander Pope

E configurações? São os alicerces invisíveis de sistemas que não quebram.
"""
