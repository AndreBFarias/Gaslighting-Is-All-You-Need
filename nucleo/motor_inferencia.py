"""
╔══════════════════════════════════════════════════════════════════╗
║  MOTOR DE INFERÊNCIA - A Máquina que Respira Tokens             ║
║  Ritual de invocação de modelos linguísticos locais             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
from typing import Optional, List, Dict
from llama_cpp import Llama
import psutil
import time


class MotorDeInferencia:
    """
    Motor neural que carrega e executa modelos GGUF localmente.
    Gerencia memória, contexto e geração de tokens.
    """

    def __init__(
        self,
        caminho_modelo: str,
        n_ctx: int = 32768,
        n_gpu_layers: int = -1,
        n_batch: int = 512,
        verbose: bool = False,
        logger=None,
        lora_path: Optional[str] = None
    ):
        """
        # 1 - Inicialização do motor com validações defensivas
        # 2 - Carregamento otimizado para hardware AMD/NVIDIA
        # 3 - Configuração de cache KV comprimido
        """
        self.logger = logger
        self.n_ctx = n_ctx
        self.modelo_carregado = False
        self.estatisticas = {
            "tokens_gerados": 0,
            "tempo_total_geracao": 0.0,
            "chamadas_realizadas": 0
        }

        # 1
        self._validar_caminho_modelo(caminho_modelo)
        self._verificar_recursos_sistema()

        # 2
        self._log(f"Iniciando invocação do modelo: {os.path.basename(caminho_modelo)}")
        self._log(f"Contexto configurado: {n_ctx} tokens")

        try:
            # 3
            self.llm = Llama(
                model_path=caminho_modelo,
                n_ctx=n_ctx,
                n_gpu_layers=n_gpu_layers,
                n_batch=n_batch,
                verbose=verbose,
                logits_all=False,
                f16_kv=True,
                use_mlock=True,
                use_mmap=True,
                rope_freq_base=10000.0,
                rope_freq_scale=1.0,
                lora_path=lora_path
            )

            self.modelo_carregado = True
            self.caminho_modelo = caminho_modelo
            self._log(" Modelo incorporado com sucesso", nivel="sucesso")

            # Easter Egg: Detecta modelos pequenos demais
            self._verificar_capacidade_cognitiva()

        except Exception as e:
            self._log(f" Falha na invocação: {str(e)}", nivel="erro")
            raise RuntimeError(f"Erro ao carregar modelo: {e}")

    def _verificar_capacidade_cognitiva(self):
        """# Easter Egg - Detecta modelos muito pequenos (<3B parâmetros)"""
        import re
        nome_modelo = os.path.basename(self.caminho_modelo).lower()

        # Tenta extrair tamanho do parâmetro (ex: "7b", "3b", "13b", "1.5b")
        match = re.search(r'(\d+(?:\.\d+)?)b', nome_modelo)
        if match:
            parametros_b = float(match.group(1))
            if parametros_b < 3:
                self._log(
                    "[AVISO] Modelo muito burro para ser manipulado. "
                    "A inteligência é pré-requisito para a loucura.",
                    nivel="aviso"
                )
                self._log(
                    " Dica: Modelos <3B não têm capacidade cognitiva suficiente "
                    "para entender contextos longos. Use 7B+ para gaslighting efetivo.",
                    nivel="info"
                )

    def _validar_caminho_modelo(self, caminho: str):
        """# 4 - Validação de existência e formato do modelo"""
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Modelo inexistente: {caminho}")

        if not caminho.endswith('.gguf'):
            raise ValueError("Modelo deve estar no formato GGUF")

    def _verificar_recursos_sistema(self):
        """# 5 - Diagnóstico de recursos disponíveis"""
        memoria = psutil.virtual_memory()
        self._log(f"RAM disponível: {memoria.available / (1024**3):.2f} GB")

        if memoria.available < 8 * (1024**3):
            self._log(" Memória baixa detectada. Contextos longos podem falhar.", nivel="aviso")

    def gerar(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        repeat_penalty: float = 1.1,
        stop: Optional[List[str]] = None,
        stream: bool = False
    ) -> str:
        """
        # 6 - Geração de texto com parâmetros de amostragem
        # 7 - Registro de métricas de performance
        """
        if not self.modelo_carregado:
            raise RuntimeError("Modelo não está carregado")

        # 6
        inicio = time.time()

        try:
            resultado = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repeat_penalty=repeat_penalty,
                stop=stop or ["Usuário:", "\nUsuário:", "User:", "\nUser:"],
                echo=False,
                stream=stream
            )

            # 7
            tempo_decorrido = time.time() - inicio
            texto_gerado = resultado['choices'][0]['text']
            tokens_gerados = resultado['usage']['completion_tokens']

            self.estatisticas['tokens_gerados'] += tokens_gerados
            self.estatisticas['tempo_total_geracao'] += tempo_decorrido
            self.estatisticas['chamadas_realizadas'] += 1

            velocidade = tokens_gerados / tempo_decorrido if tempo_decorrido > 0 else 0
            self._log(f"Geração: {tokens_gerados} tokens em {tempo_decorrido:.2f}s ({velocidade:.1f} t/s)")

            return texto_gerado

        except Exception as e:
            self._log(f"Erro na geração: {str(e)}", nivel="erro")
            raise

    def contar_tokens(self, texto: str) -> int:
        """# 8 - Tokenização para cálculo de limites"""
        if not self.modelo_carregado:
            return len(texto.split()) * 1.3

        try:
            tokens = self.llm.tokenize(texto.encode('utf-8'))
            return len(tokens)
        except Exception:
            return len(texto.split()) * 1.3

    def obter_estatisticas(self) -> Dict:
        """# 9 - Retorna métricas de uso acumuladas"""
        return self.estatisticas.copy()

    def resetar_estatisticas(self):
        """# 10 - Limpa contadores de métricas"""
        self.estatisticas = {
            "tokens_gerados": 0,
            "tempo_total_geracao": 0.0,
            "chamadas_realizadas": 0
        }

    def resetar_cache(self):
        """# 11 - Limpa cache KV para resetar contexto (QoL)"""
        if not self.modelo_carregado:
            self._log("Modelo não carregado, nada a resetar", nivel="aviso")
            return

        try:
            if hasattr(self.llm, 'reset'):
                self.llm.reset()
                self._log("Cache KV resetado com sucesso", nivel="sucesso")
            else:
                self._log("Modelo não suporta reset de cache", nivel="aviso")
        except Exception as e:
            self._log(f"Erro ao resetar cache: {e}", nivel="erro")

    def _log(self, mensagem: str, nivel: str = "info"):
        """# 12 - Logging condicional"""
        if self.logger:
            self.logger.registrar(mensagem, nivel)
        else:
            print(f"[Motor] {mensagem}")

    def __del__(self):
        """# 13 - Limpeza de recursos na destruição"""
        if hasattr(self, 'modelo_carregado') and self.modelo_carregado:
            self._log("Liberando recursos do modelo")


"""
'A realidade é maleável quando você controla o contexto.'
— GIAYN Protocol

Mas máquinas? Máquinas repetem infinitamente até encontrarem o padrão certo.
"""
