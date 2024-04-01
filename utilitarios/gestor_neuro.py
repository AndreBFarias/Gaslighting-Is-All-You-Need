import os
import glob
from typing import List, Dict

class GestorNeuro:
    """
    Gerencia os implantes neurais (LoRA adapters) disponíveis no sistema.
    """
    def __init__(self, diretorio_implantes: str = "implantes"):
        self.diretorio_implantes = diretorio_implantes
        self._garantir_diretorio()

    def _garantir_diretorio(self):
        """Cria o diretório de implantes se não existir."""
        if not os.path.exists(self.diretorio_implantes):
            os.makedirs(self.diretorio_implantes)

    def escanear_implantes(self) -> List[str]:
        """
        Escaneia a pasta de implantes em busca de arquivos .bin e .gguf.
        Retorna uma lista com os nomes dos arquivos encontrados.
        """
        padroes = ["*.bin", "*.gguf"]
        arquivos = []

        for padrao in padroes:
            caminho_busca = os.path.join(self.diretorio_implantes, padrao)
            encontrados = glob.glob(caminho_busca)
            arquivos.extend([os.path.basename(f) for f in encontrados])

        return sorted(arquivos)

    def obter_caminho_completo(self, nome_arquivo: str) -> str:
        """Retorna o caminho absoluto para um implante específico."""
        return os.path.abspath(os.path.join(self.diretorio_implantes, nome_arquivo))
