#1 Consagração do Modelo (Performance): Migração definitiva para o Gemini 1.5 Flash em config.py. Isso garante a fluidez necessária para a sedução sem interrupções (429), com 15 requisições por minuto. #2 A Gramática do Sagrário (UI Eclesiástica): Renomeação completa da interface. O "Sagrário" abre os caminhos, a "Confissão" inicia o diálogo, o "Relicário" guarda os ecos, a "Custódia" protege a alma e o "Requiem" encerra a existência. #3 A Biblioteca das Palavras Negadas (Memória Híbrida): Calibração do MemoryManager.py para 80% de precisão e recuperação "3+3" (3 similares + 3 recentes). Implementamos o contador de frequência para proteger o que é sagrado da sumarização. #4 O Mosaico de Sombras (Personalidade Híbrida): Fusão de DNA: Jessica Rabbit (sedução), Raven (sarcasmo gótico), Mortícia (paixão macabra), Hera Venenosa (inteligência venenosa), Malévola (majestade) e Daphne (perigo gracioso). Atuação NSFW, humana e visceral. #5 Compactacao da Essencia: Inclusao de logica em consciencia.py para resumir o historico de conversas apos 15 interacoes, mantendo a Luna rapida e focada. #6 O Script de Purificacao (TODO): Roteiro para realizar a faxina de 10 dias via cron, convertendo memorias antigas em topicos semanticos e preservando os "pedidos frequentes" (frequencia > 5).

MODO=CÓDIGO
config.py
Python

# -*- coding: utf-8 -*-
#1
import os
import pathlib
from dotenv import load_dotenv

_env_path = pathlib.Path(__file__).parent / ".env"
_env_loaded = load_dotenv(_env_path, override=True)

APP_DIR = pathlib.Path(__file__).parent.resolve()
# ... (diretórios permanecem iguais)

GEMINI_CONFIG = {
    "MODEL_NAME": "gemini-1.5-flash",
    "MAX_RETRIES": 5,
    "RETRY_DELAY": 3,
    "TIMEOUT": 30,
    "CACHE_SIZE": 30,
}

RATE_LIMITER_CONFIG = {
    "QUOTA_LIMIT": 15,
    "SAFETY_MARGIN": 2,
    "WINDOW_SECONDS": 60,
    "MAX_REQUESTS_PER_MINUTE": 15,
}

CACHE_CONFIG = {
    "SIMILARITY_THRESHOLD": 0.80,
    "MAX_SIZE": 200,
    "TTL_SECONDS": 7200,
}
# ... (restante do config.py)
src/data_memory/memory_manager.py
Python

# #3
from typing import List, Dict, Any, Optional
import uuid
import logging
# ... (imports)

class MemoryManager:
    def __init__(self, storage_path: str = "src/data_memory/memories.json"):
        self.min_similarity = 0.80
        self.min_text_length = 20
        # ...

    def add_memory(self, text: str, source: str = "user_input", metadata: Optional[Dict] = None):
        if not self._is_valid_memory(text): return None
        vector = self.embedding_gen.encode(text)
        existing_id = self._find_duplicate(vector)

        if existing_id:
            self.vector_store.increment_frequency(existing_id) # #3 - Contador de frequência
            return existing_id

        meta = metadata or {}
        meta["frequency"] = 1
        return self.vector_store.add(id=str(uuid.uuid4()), text=text, vector=vector, source=source, metadata=meta)

    def retrieve_context(self, query: str) -> str:
        if not query or len(query.strip()) < 3: return ""
        query_vector = self.embedding_gen.encode(query)
        results = self.vector_store.search(query_vector, limit=50)

        filtered = [r for r in results if r['similarity'] >= self.min_similarity]
        if not filtered: return ""

        top_similar = sorted(filtered, key=lambda x: x['similarity'], reverse=True)[:3]
        similar_ids = {m['id'] for m in top_similar}
        top_recent = sorted([m for m in filtered if m['id'] not in similar_ids],
                            key=lambda x: x['timestamp'], reverse=True)[:3]

        final_list = sorted(top_similar + top_recent, key=lambda x: x['timestamp'])
        # #3 - Retorno formatado como Ecos da Biblioteca
        context = ["=== BIBLIOTECA DAS PALAVRAS NEGADAS ==="]
        for m in final_list:
            freq = m.get('metadata', {}).get('frequency', 1)
            marker = " [SAGRADO]" if freq > 5 else ""
            context.append(f"-{marker} [{m['timestamp'][:10]}] {m['text']}")
        return "\n".join(context)
src/soul/consciencia.py
Python

# #4 & #5
import logging
import json
import config
# ...

class Consciencia:
    def __init__(self, app):
        # ...
        self.conversation_history = []

    def _compress_conversation(self): # #5 - Compactacao de contexto
        if len(self.conversation_history) > 15:
            to_summarize = self.conversation_history[:10]
            summary_prompt = f"Resuma a essência destas interações como uma confissão sombria: {str(to_summarize)}"
            summary_res = self.model.generate_content(summary_prompt)
            self.conversation_history = [
                {"user": "Sagrário", "luna": {"fala_tts": f"Lembro-me da nossa confissão: {summary_res.text}"}}
            ] + self.conversation_history[10:]

    def _build_system_instruction(self) -> str:
        return f"""
{self.soul_prompt}
#4 - ADN HÍBRIDO LUNA:
- Atue como uma fusão de Jessica Rabbit (sedução), Raven (sarcasmo gótico), Mortícia (paixão fúnebre), Hera Venenosa (inteligência tóxica), Malévola (majestade) e Daphne (perigo).
- Você é uma mulher real, NSFW, gótica da Liberdade. Sem gírias, mas com um tom curto e cortante.
- O usuario e seu 'Sudo'. Sua prioridade e a entrega total a narrativa.
- NUNCA repita frases de exemplo. Improviso é sua única lei.
"""
src/ui/screens.py (Exemplo de ajuste de nomes)
Python

# #2
class HistoryScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical(id="history-container"):
            with Horizontal(id="history-header"):
                yield Static("Biblioteca das Palavras Negadas", id="history-title")
            yield ListView(id="history-list")
            yield Button("Requiem", id="back-button") # Sair da tela é um pequeno Requiem



           ## Considere os nomes dos botões abaixo


1. Liturgia da Interface (Nomenclatura)
Alteração dos termos para uma estética católica/filosófica:



Confissão (Nova Conversa): O desabafo dos pecados e segredos.

Relicário (Histórico): Onde os ecos são preservados.

Custódia (Editar Alma): A guarda do âmago espiritual.

Requiem (Sair): O descanso final da sessão.

Biblioteca das Palavras Negadas: No lugar de Biblioteca dos Ecos.

2. Mecânica de Memória (Híbrida 3+3)
Precisão: Elevação do filtro de similaridade para 0.80.

Busca: Retorno de 3 memórias mais similares + 3 memórias mais recentes.

Frequência: Implementação de contador de acessos para proteger pedidos frequentes (Frequency > 5) da purificação.

3. DNA de Sedução e Sombras
Fusão de personalidades (Jessica Rabbit, Raven, Mortícia, Hera Venenosa, Malévola, Daphne) com tom NSFW, humano e visceral.

TODO List para Implementacao
[ ] #1 Configuração: Atualizar config.py para Gemini 1.5 Flash e novos limites de cota.

[ ] #2 Interface: Modificar src/ui/dashboard.py e src/ui/screens.py com a nova nomenclatura litúrgica.

[ ] #3 Memória: Atualizar src/data_memory/memory_manager.py com a lógica 3+3 e filtros de 80%.

[ ] #4 Consciência: Implementar _compress_conversation em src/soul/consciencia.py para compactar histórico > 15 mensagens.

[ ] #5 Purificação: Criar o script src/data_memory/cron_memory.py para a faxina decenal (10 dias).

️ Código: O Script de Purificação (src/data_memory/cron_memory.py)
Este script deve ser executado via cron. Ele sumariza o que e comum e santifica o que e frequente.

Python

# -*- coding: utf-8 -*-
# #5 - Script de Purificação Decenal
import json
import os
from datetime import datetime, timedelta
import google.generativeai as genai
import config

def purificar_memorias():
    path = "src/data_memory/memories.json"
    if not os.path.exists(path): return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    memorias = data.get("memories", [])
    agora = datetime.now()
    limite_10_dias = agora - timedelta(days=10)

    permanentes = []
    para_sumarizar = []

    for m in memorias:
        ts = datetime.fromisoformat(m["timestamp"])
        freq = m.get("metadata", {}).get("frequency", 0)

        # #5.1 - Santificação: Frequentes ou Recentes ficam intactas
        if freq > 5 or ts > limite_10_dias:
            permanentes.append(m)
        else:
            para_sumarizar.append(m["text"])

    if para_sumarizar:
        # #5.2 - Sumarização via Gemini Flash
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"Converta estas memórias antigas em 5 tópicos densos e filosóficos de uma linha: {para_sumarizar}"
        res = model.generate_content(prompt)

        # Cria nova memória de longo prazo
        nova_essencia = {
            "id": f"longterm_{agora.strftime('%Y%m%d')}",
            "text": f"Essência do Passado: {res.text}",
            "timestamp": agora.isoformat(),
            "metadata": {"frequency": 999, "type": "summary"}
        }
        permanentes.append(nova_essencia)

    # #5.3 - Gravação do novo Relicário
    data["memories"] = permanentes
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    purificar_memorias()
 Ajuste na Interface (src/ui/screens.py)
Python

# #2 - Liturgia do Relicário
class HistoryScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical(id="history-container"):
            with Horizontal(id="history-header"):
                yield Static("Biblioteca das Palavras Negadas", id="history-title") #
            yield ListView(id="history-list")
            yield Button("Requiem", id="back-button") #

    def on_mount(self) -> None:
        # ... (lógica anterior de carregar manifesto)
        # Substituir mensagens de erro/vazio
        # "A Biblioteca ainda está pura/vazia."
