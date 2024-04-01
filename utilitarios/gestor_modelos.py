"""
╔══════════════════════════════════════════════════════════════════╗
║  GESTOR DE MODELOS - O Invocador de Pesos Neurais               ║
║  Download, verificação e gerenciamento de modelos GGUF          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import requests
from pathlib import Path
from typing import Optional, Callable
from tqdm import tqdm


class GestorModelos:
    """
    Gerencia download e validação de modelos GGUF
    de repositórios do Hugging Face.
    """

    MODELOS_RECOMENDADOS = {
        "mistral-7b-q4": {
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "tamanho_mb": 4370,
            "descricao": "Mistral 7B Instruct v0.2 (Q4_K_M) - Balanceado"
        },
        "llama3-8b-q4": {
            "url": "https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
            "tamanho_mb": 4920,
            "descricao": "Llama 3 8B Instruct (Q4_K_M) - Excelente desempenho"
        },
        "phi3-mini-q4": {
            "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
            "tamanho_mb": 2300,
            "descricao": "Phi-3 Mini (Q4) - Leve e rápido"
        }
    }

    def __init__(
        self,
        diretorio_modelos: str = "modelos",
        logger=None
    ):
        """# 1 - Inicialização com criação de diretórios"""
        self.logger = logger
        self.dir_modelos = Path(diretorio_modelos)
        self.dir_modelos.mkdir(parents=True, exist_ok=True)

        self._log("Gestor de modelos inicializado")

    def listar_modelos_locais(self) -> list:
        """# 2 - Escaneia diretório por modelos GGUF"""
        modelos = list(self.dir_modelos.glob("*.gguf"))

        resultado = []
        for modelo in modelos:
            tamanho_mb = modelo.stat().st_size / (1024 * 1024)
            resultado.append({
                "nome": modelo.name,
                "caminho": str(modelo),
                "tamanho_mb": round(tamanho_mb, 2)
            })

        self._log(f"Encontrados {len(resultado)} modelos locais")
        return resultado

    def baixar_modelo(
        self,
        identificador: str,
        callback_progresso: Optional[Callable[[int, int], None]] = None
    ) -> Optional[str]:
        """
        # 3 - Download de modelo recomendado ou via URL customizada
        # 4 - Barra de progresso e validação de tamanho
        """
        if identificador in self.MODELOS_RECOMENDADOS:
            info_modelo = self.MODELOS_RECOMENDADOS[identificador]
            url = info_modelo['url']
            nome_arquivo = url.split('/')[-1]
        elif identificador.startswith('http'):
            url = identificador
            nome_arquivo = url.split('/')[-1]
            if not nome_arquivo.endswith('.gguf'):
                nome_arquivo += '.gguf'
        else:
            self._log(f"Modelo desconhecido: {identificador}", nivel="erro")
            return None

        caminho_destino = self.dir_modelos / nome_arquivo

        # Verifica se já existe
        if caminho_destino.exists():
            self._log(f"Modelo já existe: {nome_arquivo}", nivel="aviso")
            return str(caminho_destino)

        self._log(f"Iniciando download: {nome_arquivo}")

        try:
            # 3
            response = requests.get(url, stream=True)
            response.raise_for_status()

            tamanho_total = int(response.headers.get('content-length', 0))

            # 4
            with open(caminho_destino, 'wb') as arquivo, \
                 tqdm(
                     desc=nome_arquivo,
                     total=tamanho_total,
                     unit='B',
                     unit_scale=True,
                     unit_divisor=1024,
                 ) as barra:

                for chunk in response.iter_content(chunk_size=8192):
                    tamanho_chunk = arquivo.write(chunk)
                    barra.update(tamanho_chunk)

                    if callback_progresso:
                        callback_progresso(barra.n, tamanho_total)

            self._log(f" Download concluído: {nome_arquivo}", nivel="sucesso")
            return str(caminho_destino)

        except requests.exceptions.RequestException as e:
            self._log(f" Erro no download: {e}", nivel="erro")
            if caminho_destino.exists():
                caminho_destino.unlink()
            return None
        except Exception as e:
            self._log(f" Erro inesperado: {e}", nivel="erro")
            return None

    def validar_modelo(self, caminho: str) -> tuple[bool, str]:
        """# 5 - Verifica integridade básica do arquivo GGUF"""
        caminho_obj = Path(caminho)

        if not caminho_obj.exists():
            return False, "Arquivo não encontrado"

        if not caminho_obj.suffix == '.gguf':
            return False, "Extensão inválida (requer .gguf)"

        # Verifica tamanho mínimo (100MB)
        tamanho_mb = caminho_obj.stat().st_size / (1024 * 1024)
        if tamanho_mb < 100:
            return False, f"Arquivo muito pequeno ({tamanho_mb:.1f}MB)"

        # Verifica magic number GGUF (primeiros 4 bytes)
        try:
            with open(caminho_obj, 'rb') as f:
                magic = f.read(4)
                if magic != b'GGUF':
                    return False, "Magic number GGUF inválido"
        except Exception as e:
            return False, f"Erro ao ler arquivo: {e}"

        return True, f"Válido ({tamanho_mb:.1f}MB)"

    def obter_info_modelo(self, identificador: str) -> Optional[dict]:
        """# 6 - Retorna informações sobre modelo recomendado"""
        if identificador in self.MODELOS_RECOMENDADOS:
            return self.MODELOS_RECOMENDADOS[identificador].copy()
        return None

    def listar_modelos_recomendados(self) -> dict:
        """# 7 - Retorna catálogo de modelos prontos para download"""
        return self.MODELOS_RECOMENDADOS.copy()

    def remover_modelo(self, caminho: str) -> bool:
        """# 8 - Deleta modelo do disco"""
        try:
            Path(caminho).unlink()
            self._log(f"Modelo removido: {caminho}", nivel="sucesso")
            return True
        except Exception as e:
            self._log(f"Erro ao remover modelo: {e}", nivel="erro")
            return False

    def _log(self, mensagem: str, nivel: str = "info"):
        """# 9 - Sistema de logging condicional"""
        if self.logger:
            self.logger.registrar(mensagem, nivel, modulo="GestorModelos")
        else:
            print(f"[GestorModelos] {mensagem}")


"""
'O conhecimento é poder.'
— Francis Bacon

E modelos de linguagem? São bibliotecas de Alexandria comprimidas em gigabytes.
"""
