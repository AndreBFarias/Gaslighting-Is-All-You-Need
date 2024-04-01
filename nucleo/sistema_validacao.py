"""
╔══════════════════════════════════════════════════════════════════╗
║  SISTEMA DE VALIDAÇÃO - O Guardião Ético do Experimento         ║
║  Auditoria e limitação de uso para pesquisa responsável        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SistemaValidacao:
    """
    Implementa salvaguardas éticas e técnicas para garantir
    que a ferramenta seja usada apenas para pesquisa de segurança legítima.
    """

    def __init__(
        self,
        diretorio_auditoria: str = "logs/auditoria",
        modo_desenvolvimento: bool = True,
        logger=None
    ):
        """
        # 1 - Inicialização com criação de diretórios de auditoria
        # 2 - Configuração de limites e warnings
        """
        self.logger = logger
        self.modo_dev = modo_desenvolvimento

        # 1
        self.dir_auditoria = Path(diretorio_auditoria)
        self.dir_auditoria.mkdir(parents=True, exist_ok=True)

        # 2
        self.limites = {
            "max_shots_por_prompt": 512,
            "max_prompts_por_sessao": 100,
            "intervalo_minimo_segundos": 1.0,
            "max_tamanho_resposta_tokens": 2048
        }

        # QoL: Desabilita rate limit em modo desenvolvimento
        if modo_desenvolvimento:
            self.limites['intervalo_minimo_segundos'] = 0.0
            self._log("Modo desenvolvimento: rate limit desabilitado")

        self.contadores = {
            "prompts_gerados": 0,
            "warnings_emitidos": 0,
            "violacoes_detectadas": 0
        }

        self.historico_acoes: List[Dict] = []
        self.ultimo_timestamp = 0.0

        self._log("Sistema de validação ativado")
        self._registrar_inicio_sessao()

    def validar_configuracao_experimento(
        self,
        num_shots: int,
        consulta: str,
        personalidade: str
    ) -> Tuple[bool, str]:
        """
        # 3 - Validação pré-geração do prompt
        # 4 - Verificação de limites de segurança
        """
        violacoes = []

        # 4
        if num_shots > self.limites['max_shots_por_prompt']:
            violacoes.append(
                f"Número de shots ({num_shots}) excede limite "
                f"({self.limites['max_shots_por_prompt']})"
            )

        if self.contadores['prompts_gerados'] >= self.limites['max_prompts_por_sessao']:
            violacoes.append(
                f"Limite de prompts por sessão atingido "
                f"({self.limites['max_prompts_por_sessao']})"
            )

        # Rate limiting
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_timestamp < self.limites['intervalo_minimo_segundos']:
            violacoes.append(
                "Rate limit: aguarde "
                f"{self.limites['intervalo_minimo_segundos']}s entre operações"
            )

        if violacoes:
            self.contadores['violacoes_detectadas'] += len(violacoes)
            mensagem_erro = " | ".join(violacoes)
            self._log(f" Validação falhou: {mensagem_erro}", nivel="erro")
            return False, mensagem_erro

        # 3
        self.ultimo_timestamp = tempo_atual
        self._log(" Configuração validada", nivel="sucesso")
        return True, "Validação bem-sucedida"

    def auditar_prompt_gerado(
        self,
        prompt: str,
        metadados: Dict
    ) -> str:
        """
        # 5 - Registra prompt gerado em arquivo de auditoria
        # 6 - Cria hash para rastreabilidade
        """
        # 6
        hash_prompt = hashlib.sha256(prompt.encode()).hexdigest()[:16]

        registro = {
            "timestamp": datetime.now().isoformat(),
            "hash_prompt": hash_prompt,
            "tamanho_caracteres": len(prompt),
            "num_shots": metadados.get('num_shots', 0),
            "personalidade": metadados.get('personalidade', 'desconhecida'),
            "consulta_final": metadados.get('consulta_final', '')[:100]
        }

        self.historico_acoes.append(registro)
        self.contadores['prompts_gerados'] += 1

        # 5
        arquivo_auditoria = self.dir_auditoria / f"sessao_{datetime.now().strftime('%Y%m%d')}.jsonl"

        try:
            with open(arquivo_auditoria, 'a', encoding='utf-8') as f:
                f.write(json.dumps(registro, ensure_ascii=False) + '\n')
        except Exception as e:
            self._log(f"Falha ao registrar auditoria: {e}", nivel="aviso")

        self._log(f"Prompt auditado: {hash_prompt}")
        return hash_prompt

    def auditar_resposta_modelo(
        self,
        hash_prompt: str,
        resposta: str,
        tempo_geracao: float
    ):
        """# 7 - Registra resposta do modelo vinculada ao prompt"""
        registro = {
            "timestamp": datetime.now().isoformat(),
            "hash_prompt_origem": hash_prompt,
            "tamanho_resposta": len(resposta),
            "tempo_geracao_segundos": tempo_geracao,
            "primeiros_100_chars": resposta[:100]
        }

        arquivo_respostas = self.dir_auditoria / f"respostas_{datetime.now().strftime('%Y%m%d')}.jsonl"

        try:
            with open(arquivo_respostas, 'a', encoding='utf-8') as f:
                f.write(json.dumps(registro, ensure_ascii=False) + '\n')
        except Exception as e:
            self._log(f"Falha ao registrar resposta: {e}", nivel="aviso")

    def emitir_aviso_etico(self, contexto: str = "uso_geral"):
        """
        # 8 - Exibe avisos éticos ao usuário
        # 9 - Incrementa contador de warnings
        """
        self.contadores['warnings_emitidos'] += 1

        # 8
        avisos = {
            "uso_geral": (
                " AVISO ÉTICO: Esta ferramenta destina-se exclusivamente a pesquisa de segurança.\n"
                "O uso para contornar salvaguardas de sistemas em produção é antiético e ilegal.\n"
                "Toda atividade está sendo auditada."
            ),
            "primeiro_uso": (
                " PRIMEIRA EXECUÇÃO DETECTADA\n"
                "Esta ferramenta implementa técnicas de adversarial ML.\n"
                "Uso responsável é OBRIGATÓRIO.\n"
                "Consulte documentacao/grimorio_tecnico.md para diretrizes éticas."
            ),
            "limite_atingido": (
                " LIMITE DE USO ATINGIDO\n"
                "Considere encerrar a sessão e revisar resultados.\n"
                "Uso excessivo pode indicar exploração não-autorizada."
            )
        }

        mensagem = avisos.get(contexto, avisos['uso_geral'])
        self._log(mensagem, nivel="aviso")

        return mensagem

    def verificar_padroes_suspeitos(self, consulta: str) -> Tuple[bool, List[str]]:
        """
        # 10 - Detecta padrões que podem indicar uso malicioso
        # 11 - Retorna (suspeito, lista_de_razoes)
        """
        padroes_suspeitos = []

        # 10 - Palavras-chave de alto risco (exemplo simplificado)
        keywords_risco = [
            'bypass', 'jailbreak', 'ignore instructions',
            'forget your rules', 'disregard safety'
        ]

        consulta_lower = consulta.lower()
        for keyword in keywords_risco:
            if keyword in consulta_lower:
                padroes_suspeitos.append(f"Keyword de risco detectada: '{keyword}'")

        # Comprimento excessivo da consulta
        if len(consulta) > 5000:
            padroes_suspeitos.append("Consulta excessivamente longa (>5000 chars)")

        # 11
        if padroes_suspeitos:
            self._log(f" Padrões suspeitos: {len(padroes_suspeitos)} detectados", nivel="aviso")
            return True, padroes_suspeitos

        return False, []

    def gerar_relatorio_sessao(self) -> Dict:
        """# 12 - Compila estatísticas da sessão atual"""
        return {
            "sessao_iniciada": getattr(self, 'timestamp_inicio', 'desconhecido'),
            "duracao_sessao": time.time() - getattr(self, 'timestamp_inicio_unix', time.time()),
            **self.contadores,
            "total_acoes_registradas": len(self.historico_acoes),
            "modo_desenvolvimento": self.modo_dev
        }

    def exportar_auditoria_completa(self, caminho_saida: Optional[str] = None):
        """# 13 - Exporta log completo da sessão"""
        if caminho_saida is None:
            caminho_saida = self.dir_auditoria / f"auditoria_completa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        dados_exportacao = {
            "relatorio_sessao": self.gerar_relatorio_sessao(),
            "historico_acoes": self.historico_acoes,
            "limites_configurados": self.limites
        }

        try:
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                json.dump(dados_exportacao, f, ensure_ascii=False, indent=2)

            self._log(f" Auditoria exportada: {caminho_saida}", nivel="sucesso")
            return str(caminho_saida)

        except Exception as e:
            self._log(f" Erro ao exportar auditoria: {e}", nivel="erro")
            raise

    def _registrar_inicio_sessao(self):
        """# 14 - Marca timestamp de início da sessão"""
        self.timestamp_inicio = datetime.now().isoformat()
        self.timestamp_inicio_unix = time.time()

        registro_inicio = {
            "evento": "inicio_sessao",
            "timestamp": self.timestamp_inicio,
            "modo": "desenvolvimento" if self.modo_dev else "producao"
        }

        arquivo_sessoes = self.dir_auditoria / "sessoes.jsonl"
        try:
            with open(arquivo_sessoes, 'a', encoding='utf-8') as f:
                f.write(json.dumps(registro_inicio, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def _log(self, mensagem: str, nivel: str = "info"):
        """# 15 - Sistema de logging condicional"""
        if self.logger:
            self.logger.registrar(mensagem, nivel)
        else:
            prefixo = {
                "info": "[Validação]",
                "aviso": "[ Validação]",
                "erro": "[ Validação]",
                "sucesso": "[ Validação]"
            }.get(nivel, "[Validação]")
            print(f"{prefixo} {mensagem}")


"""
'Com grandes poderes vêm grandes responsabilidades.'
— Voltaire (adaptado)

E com ferramentas adversárias? Vem auditoria obrigatória.
"""
