import json
import os
from typing import Dict, Any

class MemoriaPersistente:
    """
    Gerencia a persistência do estado do usuário entre sessões.
    Salva configurações como modelo, implante, e parâmetros cognitivos.
    """
    def __init__(self, arquivo_estado: str = "user_state.json"):
        self.arquivo_estado = arquivo_estado
        self.estado_padrao = {
            "modelo_selecionado": "",
            "implante_selecionado": "Nenhum",
            "nivel_hipnose": 0.5,  # 0.0 a 1.0
            "instabilidade": 0.7   # Temperature
        }

    def carregar_estado(self) -> Dict[str, Any]:
        """Carrega o estado salvo ou retorna o padrão se não existir."""
        if not os.path.exists(self.arquivo_estado):
            return self.estado_padrao.copy()

        try:
            with open(self.arquivo_estado, 'r', encoding='utf-8') as f:
                estado = json.load(f)
                # Mescla com padrão para garantir que chaves novas existam
                estado_final = self.estado_padrao.copy()
                estado_final.update(estado)
                return estado_final
        except Exception as e:
            print(f"Erro ao carregar memória persistente: {e}")
            return self.estado_padrao.copy()

    def salvar_estado(self, estado: Dict[str, Any]):
        """Salva o estado atual no arquivo JSON."""
        try:
            with open(self.arquivo_estado, 'w', encoding='utf-8') as f:
                json.dump(estado, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar memória persistente: {e}")
