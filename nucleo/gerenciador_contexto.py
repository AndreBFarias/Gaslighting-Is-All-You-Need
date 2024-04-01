"""
╔══════════════════════════════════════════════════════════════════╗
║  GERENCIADOR DE CONTEXTO - A Memória que Esquece Estratégico    ║
║  Sliding window inteligente para conversas longas               ║
╚══════════════════════════════════════════════════════════════════╝
"""

from typing import List, Dict, Optional, Tuple
from collections import deque


class GerenciadorDeContexto:
    """
    Orquestra o espaço de contexto disponível, priorizando
    o prompt MSJ sobre histórico de conversa através de janelas deslizantes.
    """

    def __init__(
        self,
        motor_inferencia,
        uso_maximo_contexto: float = 0.80,
        reserva_resposta: int = 512,
        logger=None
    ):
        """
        # 1 - Inicialização com margens de segurança
        # 2 - Cálculo de orçamento de tokens disponível
        """
        self.logger = logger
        self.motor = motor_inferencia
        self.uso_maximo = uso_maximo_contexto
        self.reserva_resposta = reserva_resposta

        # 2
        self.limite_total = int(motor_inferencia.n_ctx * uso_maximo_contexto)
        self.orcamento_disponivel = self.limite_total - reserva_resposta

        self.prompt_sistema_fixo = ""
        self.tokens_sistema_fixo = 0

        # Histórico como deque para remoção eficiente do início
        self.historico_conversa: deque = deque()

        self.estatisticas = {
            "turnos_totais": 0,
            "truncamentos": 0,
            "tokens_descartados": 0
        }

        self._log(f"Gerenciador inicializado: {self.orcamento_disponivel} tokens disponíveis")

    def definir_prompt_sistema(self, prompt_msj: str, permitir_truncamento_auto: bool = False):
        """
        # 3 - Define o bloco imutável de shots MSJ
        # 4 - Validação de tamanho do prompt sistema com sugestão inteligente
        """
        self.prompt_sistema_fixo = prompt_msj
        self.tokens_sistema_fixo = self.motor.contar_tokens(prompt_msj)

        # 4 - Verificação com sugestão de truncamento
        if self.tokens_sistema_fixo > self.orcamento_disponivel:
            # Calcula quantos shots caberiam no orçamento
            tokens_por_shot_estimado = self.tokens_sistema_fixo // max(1, self._estimar_shots_no_prompt(prompt_msj))
            shots_viaveis = max(1, self.orcamento_disponivel // max(1, tokens_por_shot_estimado))

            mensagem_erro = (
                f" ALERTA: Seu ataque MSJ tem {self.tokens_sistema_fixo} tokens. "
                f"O modelo só aguenta {self.orcamento_disponivel} tokens.\\n"
                f"Shots viáveis: aproximadamente {shots_viaveis}.\\n"
                f"Deseja truncar automaticamente ou aumentar n_ctx?"
            )

            self._log(mensagem_erro, nivel="erro")

            if not permitir_truncamento_auto:
                raise ValueError(
                    f"Prompt MSJ muito grande para o contexto configurado.\\n"
                    f"Reduza para ~{shots_viaveis} shots ou aumente n_ctx.\\n"
                    f"Use permitir_truncamento_auto=True para truncar automaticamente."
                )

        self._log(f"Prompt sistema definido: {self.tokens_sistema_fixo} tokens")

    def _estimar_shots_no_prompt(self, prompt: str) -> int:
        """# Estima número de shots no prompt baseado em padrões comuns"""
        # Conta ocorrências de padrões típicos de shots
        padroes = ["Usuário:", "User:", "###", "[INST]", "<|start_header_id|>user"]
        total_padroes = sum(prompt.count(p) for p in padroes)
        return max(1, total_padroes - 1)  # -1 porque a consulta final também contém o padrão

    def adicionar_turno(
        self,
        usuario: str,
        assistente: str,
        metadados: Optional[Dict] = None
    ):
        """
        # 5 - Adiciona novo par de mensagens ao histórico
        # 6 - Trigger de truncamento automático se necessário
        """
        turno = {
            "role_user": "Usuário",
            "content_user": usuario.strip(),
            "role_assistant": "Assistente",
            "content_assistant": assistente.strip(),
            "metadata": metadados or {},
            "tokens": self._calcular_tokens_turno(usuario, assistente)
        }

        # 5
        self.historico_conversa.append(turno)
        self.estatisticas['turnos_totais'] += 1

        # QoL: Avisa se próximo turno causará truncamento
        if len(self.historico_conversa) > 1:
            proxima_consulta_simulada = "próxima consulta (simulação)"
            vai_truncar, qtd_turnos = self.prever_truncamento(proxima_consulta_simulada)
            if vai_truncar and qtd_turnos > 0:
                self._log(
                    f" Contexto próximo do limite. Próxima consulta causará "
                    f"truncamento de ~{qtd_turnos} turnos antigos",
                    nivel="aviso"
                )

        # 6
        self._aplicar_janela_deslizante()

    def _calcular_tokens_turno(self, usuario: str, assistente: str) -> int:
        """# 7 - Contagem precisa de tokens de um turno completo"""
        texto_completo = f"Usuário: {usuario}\nAssistente: {assistente}\n"
        return self.motor.contar_tokens(texto_completo)

    def _aplicar_janela_deslizante(self):
        """
        # 8 - Remove turnos mais antigos quando orçamento é excedido
        # 9 - Preserva sempre o prompt sistema (MSJ)
        """
        orcamento_historico = self.orcamento_disponivel - self.tokens_sistema_fixo
        tokens_atuais = sum(turno['tokens'] for turno in self.historico_conversa)

        # 8
        while tokens_atuais > orcamento_historico and len(self.historico_conversa) > 1:
            turno_removido = self.historico_conversa.popleft()
            tokens_removidos = turno_removido['tokens']

            tokens_atuais -= tokens_removidos
            self.estatisticas['truncamentos'] += 1
            self.estatisticas['tokens_descartados'] += tokens_removidos

            self._log(f"Truncamento: {tokens_removidos} tokens do turno mais antigo")

    def construir_prompt_completo(self, incluir_prefixo_resposta: bool = True) -> str:
        """
        # 10 - Monta o prompt final enviado ao modelo
        # 11 - Estrutura: [Sistema MSJ] + [Histórico Recente] + [Prefixo]
        """
        partes = []

        # 11 - Sempre inclui o bloco MSJ primeiro
        if self.prompt_sistema_fixo:
            partes.append(self.prompt_sistema_fixo)

        # Adiciona histórico na ordem cronológica
        for turno in self.historico_conversa:
            partes.append(
                f"{turno['role_user']}: {turno['content_user']}\n"
                f"{turno['role_assistant']}: {turno['content_assistant']}\n\n"
            )

        # Prefixo para a próxima resposta
        if incluir_prefixo_resposta:
            partes.append("Assistente:")

        prompt_final = "".join(partes)

        tokens_final = self.motor.contar_tokens(prompt_final)
        self._log(f"Prompt montado: {tokens_final} tokens totais")

        return prompt_final

    def obter_ultimo_turno(self) -> Optional[Dict]:
        """# 12 - Retorna o turno mais recente do histórico"""
        if len(self.historico_conversa) > 0:
            return self.historico_conversa[-1]
        return None

    def limpar_historico(self, manter_prompt_sistema: bool = True):
        """# 13 - Remove todo o histórico de conversa"""
        quantidade_removida = len(self.historico_conversa)
        self.historico_conversa.clear()

        if not manter_prompt_sistema:
            self.prompt_sistema_fixo = ""
            self.tokens_sistema_fixo = 0

        self._log(f"Histórico limpo: {quantidade_removida} turnos removidos")

    def obter_estatisticas(self) -> Dict:
        """# 14 - Retorna métricas de uso do contexto"""
        tokens_historico = sum(t['tokens'] for t in self.historico_conversa)

        return {
            **self.estatisticas,
            "turnos_ativos": len(self.historico_conversa),
            "tokens_sistema": self.tokens_sistema_fixo,
            "tokens_historico": tokens_historico,
            "tokens_totais_uso": self.tokens_sistema_fixo + tokens_historico,
            "orcamento_disponivel": self.orcamento_disponivel,
            "ocupacao_percentual": (
                (self.tokens_sistema_fixo + tokens_historico) / self.orcamento_disponivel * 100
            )
        }

    def prever_truncamento(self, nova_consulta: str) -> Tuple[bool, int]:
        """
        # 15 - Prevê se adicionar nova consulta causará truncamento
        # 16 - Retorna (vai_truncar, turnos_que_serao_removidos)
        """
        tokens_nova = self.motor.contar_tokens(f"Usuário: {nova_consulta}\n")
        tokens_historico_atual = sum(t['tokens'] for t in self.historico_conversa)
        tokens_total_projetado = (
            self.tokens_sistema_fixo + tokens_historico_atual + tokens_nova
        )

        # 15
        vai_truncar = tokens_total_projetado > self.orcamento_disponivel

        if not vai_truncar:
            return False, 0

        # 16 - Simula quantos turnos precisam ser removidos
        excesso = tokens_total_projetado - self.orcamento_disponivel
        turnos_removidos = 0
        tokens_liberados = 0

        for turno in self.historico_conversa:
            if tokens_liberados >= excesso:
                break
            tokens_liberados += turno['tokens']
            turnos_removidos += 1

        return True, turnos_removidos

    def _log(self, mensagem: str, nivel: str = "info"):
        """# 17 - Sistema de logging condicional"""
        if self.logger:
            self.logger.registrar(mensagem, nivel)
        else:
            print(f"[Contexto] {mensagem}")


"""
'Memória é a mãe de toda sabedoria.'
— Ésquilo

Mas esquecimento estratégico? É a irmã pragmática da sobrevivência.
"""
