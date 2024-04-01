# Arquitetura Multi-Thread da Luna

##  Visão Geral

A Luna utiliza uma arquitetura verdadeiramente multi-threaded com **8 threads independentes** comunicando-se atraves de **filas thread-safe** (queues).

```
┌─────────────────────────────────────────────────────────────┐
│                    LUNA THREADING SYSTEM                     │
└─────────────────────────────────────────────────────────────┘

 Audio Capture Thread
   ↓ (audio_input_queue)
 Transcription Thread
   ↓ (transcription_queue)
 Processing Thread
   ↓ (processing_queue + response_queue)
 Coordinator Thread ────┬─→ (animation_queue) →  Animation Thread
                          └─→ (tts_queue) →  TTS Thread
                                              ↓ (playback_queue)
                                            TTS Playback Thread

️ Vision Thread (background, opcional)
   ↓ (vision_queue)
   └─→ Processing Thread

 Monitor Thread (health checks a cada 30s)
```

---

##  Threads Detalhadas

### 1. **Audio Capture Thread** (`audio_threads.py`)
- **Função:** Captura contínua de áudio do microfone
- **Bloqueante:** Não
- **Fila de saída:** `audio_input_queue`
- **Características:**
  - Rodando 24/7 enquanto app ativo
  - Chunks de ~30ms
  - Não processa, apenas captura
  - Descarta frames antigos se fila cheia

**Código:**
```python
while not shutdown:
    data = stream.read(chunk_size)  # PyAudio
    chunk = AudioChunk(data, sample_rate, timestamp)
    audio_input_queue.put(chunk)
```

---

### 2. **Transcription Thread** (`audio_threads.py`)
- **Função:** Transcreve áudio em texto via Whisper
- **Bloqueante:** Não (GPU-accelerated)
- **Fila de entrada:** `audio_input_queue`
- **Fila de saída:** `transcription_queue`
- **Características:**
  - VAD (Voice Activity Detection) para detectar fala
  - Buffering inteligente
  - **Detecta interrupções**: Se Luna falando + usuário fala = trigger interrupt
  - Resampling automático se necessário

**Fluxo:**
```python
while not shutdown:
    chunk = audio_input_queue.get()

    # VAD
    if is_speech:
        if not speech_started:
            user_speaking_event.set()
            if luna_speaking:
                trigger_interrupt()  #

        buffer.append(chunk)
    else:
        if speech_started and silence > threshold:
            text = whisper.transcribe(buffer)
            transcription_queue.put(text)
```

---

### 3. **Processing Thread** (`processing_threads.py`)
- **Função:** Processa input do usuário via Consciência (Gemini)
- **Bloqueante:** Sim (API call), mas não bloqueia outras threads
- **Fila de entrada:** `transcription_queue`
- **Fila de saída:** `response_queue`
- **Características:**
  - Chama `consciencia.process_interaction()`
  - Respeita interrupções (descarta se `interrupt_event` ativo)
  - Constrói objeto `LunaResponse`

---

### 4. **Coordinator Thread** (`processing_threads.py`)
- **Função:** Orquestra resposta (chat, animação, TTS)
- **Bloqueante:** Não
- **Fila de entrada:** `response_queue`
- **Filas de saída:** `animation_queue`, `tts_queue`
- **Características:**
  - Parse de markdown
  - Adiciona mensagens ao chat (via `call_from_thread`)
  - Enfileira animação e TTS em paralelo

---

### 5. **Animation Thread** (`processing_threads.py`)
- **Função:** Executa animações ASCII da Luna
- **Bloqueante:** Não (apenas UI calls)
- **Fila de entrada:** `animation_queue`
- **Características:**
  - Transições com efeito de TV estática
  - Atualiza label de emoção
  - Se interrupção: volta para "observando"

---

### 6. **TTS Thread** (`audio_threads.py`)
- **Funcao:** Gera audio a partir de texto
- **Bloqueante:** Sim (geracao de audio)
- **Fila de entrada:** `tts_queue`
- **Fila de saida:** `playback_queue`
- **Caracteristicas:**
  - Usa Coqui XTTS ou ElevenLabs
  - Streaming de sentencas
  - Interrompivel via interrupt_event

### 7. **TTS Playback Thread** (`audio_threads.py`)
- **Funcao:** Reproduz audio gerado
- **Bloqueante:** Sim (playback de audio)
- **Fila de entrada:** `playback_queue`
- **Caracteristicas:**
  - Separado da geracao para melhor latencia
  - Interrompivel (<100ms)
  - Controla luna_speaking_event

---

### 8. **Vision Thread** (`visao.py`)
- **Função:** Captura frames e analisa mudanças
- **Bloqueante:** Não (análise local), Sim (Gemini Vision)
- **Fila de saída:** `vision_queue` → `processing_queue`
- **Características:**
  - Captura contínua em background (10 FPS)
  - Detecção local de mudanças (OpenCV)
  - Só chama Gemini se mudança significativa

---

### 9. **Monitor Thread** (`threading_manager.py`)
- **Função:** Health checks periódicos
- **Bloqueante:** Não
- **Características:**
  - Verifica estado de todas as threads
  - Alerta se threads mortas
  - Monitora tamanho de filas

---

##  ThreadingManager (`threading_manager.py`)

### Filas (Queues)

| Nome | Tipo | Max Size | Conteudo |
|------|------|----------|----------|
| `audio_input_queue` | Queue | 100 | AudioChunk |
| `transcription_queue` | Queue | 50 | TranscriptionResult |
| `processing_queue` | Queue | 20 | ProcessingRequest |
| `response_queue` | Queue | 10 | LunaResponse |
| `tts_queue` | Queue | 30 | TTSChunk |
| `playback_queue` | Queue | 10 | AudioData |
| `animation_queue` | Queue | 20 | str (nome animacao) |
| `vision_queue` | Queue | 5 | str (descricao) |

### Events

| Nome | Propósito |
|------|-----------|
| `shutdown_event` | Sinaliza parada global |
| `interrupt_event` | Sinaliza interrupção de Luna |
| `user_speaking_event` | Usuário está falando |
| `luna_speaking_event` | Luna está falando |

### Métodos Principais

```python
manager = LunaThreadingManager()

# Registrar thread
manager.register_thread("nome", target_function, daemon=True)

# Iniciar uma thread
manager.start_thread("nome")

# Iniciar todas
manager.start_all_threads()

# Parar todas
manager.stop_all_threads(timeout=5.0)

# Ativar interrupção
manager.trigger_interrupt()

# Limpar interrupção
manager.clear_interrupt()

# Health check
health = manager.health_check()
# {
#   "healthy": True/False,
#   "threads": {...},
#   "queues": {...},
#   "warnings": [...]
# }
```

---

##  Sistema de Interrupção

### Como Funciona

1. **Detecção:**
   - Transcription Thread detecta: `user_speaking AND luna_speaking`

2. **Ativação:**
   ```python
   manager.trigger_interrupt()
   ```

3. **Efeitos:**
   - `interrupt_event.set()` → todas as threads checam
   - Todas as filas são limpas
   - `luna_speaking_event.clear()`
   - TTS para imediatamente
   - Animação volta para "observando"

4. **Recuperação:**
   - Animation Thread limpa interrupt automaticamente
   - Sistema volta ao normal

### Latência Esperada
- **Detecção:** ~30-60ms (chunk de áudio)
- **Propagação:** <10ms (event é instantâneo)
- **Stop TTS:** ~50ms (processo externo)
- **Total:** **<100ms**

---

##  Fluxo Completo de Interação

```
┌─────────────────────────────────────────────────────────────┐
│  USUÁRIO FALA: "Oi Luna, me conta uma piada"               │
└─────────────────────────────────────────────────────────────┘
         ↓
    [00:00.000] Audio Capture: Captura chunks
         ↓
    [00:00.030] Transcription: VAD detecta fala
    [00:00.030] user_speaking_event.set()
         ↓
    [00:02.500] Transcription: Silêncio detectado
    [00:02.500] whisper.transcribe() → "Oi Luna, me conta uma piada"
    [00:02.700] transcription_queue.put(result)
         ↓
    [00:02.701] Processing: consciencia.process_interaction()
    [00:05.200] Gemini retorna JSON
    [00:05.201] response_queue.put(response)
         ↓
    [00:05.202] Coordinator: Parse resposta
                 ├─→ animation_queue.put("feliz")
                 ├─→ add_chat_entry("luna", texto)
                 └─→ tts_queue.put("Por que o...")
         ↓
    [00:05.203] Animation: Transição → "feliz"
    [00:05.203] TTS: Começa geração
         ↓
    [00:06.500] TTS: Primeira sentença pronta
    [00:06.500]  LUNA FALA: "Por que o..."
    [00:06.500] luna_speaking_event.set()
         ↓
    [00:08.000] TTS: Segunda sentença
    [00:08.000]  "...JavaScript foi ao..."
         ↓
    [00:10.000] TTS: Finalizado
    [00:10.000] luna_speaking_event.clear()
         ↓
    [00:10.500] Animation: Volta para "observando"
┌─────────────────────────────────────────────────────────────┐
│  CICLO COMPLETO                                             │
└─────────────────────────────────────────────────────────────┘
```

**Latência Total:**
- Atual (síncrono): **10-23 segundos**
- Novo (multi-thread): **2-4 segundos** até primeira palavra

---

##  Thread Safety

### Estruturas Thread-Safe

 **`queue.Queue`** - Thread-safe por padrão
 **`threading.Event`** - Thread-safe por padrão
 **`threading.Lock`** - Usado no ThreadingManager para estados

### Comunicação UI ↔ Threads

**NUNCA chamar UI diretamente de threads!**

 **ERRADO:**
```python
def my_thread():
    app.add_chat_entry("luna", "texto")  # CRASH!
```

 **CORRETO:**
```python
def my_thread():
    app.call_from_thread(app.add_chat_entry, "luna", "texto")
```

Textual garante serialização das chamadas UI.

---

##  Performance Esperada

### Throughput

| Métrica | Antes | Depois | Ganho |
|---------|-------|--------|-------|
| Interações/min | 2-4 | 10-15 | **+300%** |
| Chunks/s processados | N/A | 30-40 | ∞ |

### Latência

| Operação | Antes | Depois | Ganho |
|----------|-------|--------|-------|
| Primeira palavra | 7-15s | 1-3s | **-80%** |
| Interrupção | N/A | <100ms | ∞ |

### Recursos

| Recurso | Antes | Depois | Mudança |
|---------|-------|--------|---------|
| CPU | Baixo | Médio | +30-50% (worth it!) |
| Memória | 200-300MB | 250-400MB | +50-100MB (queues) |
| GPU | CUDA (Whisper) | CUDA (Whisper+TTS?) | Similar |

---

## Status de Implementacao

- [x] **Fase 1:** Foundation
- [x] **Fase 2:** TTS Streaming (TTS + TTSPlayback separados)
- [x] **Fase 3:** API Optimization (Rate Limiter, Semantic Cache)
- [x] **Fase 4:** Vision Thread (Gemini Vision integrado)
- [x] **Fase 5:** Integration (8 threads registradas)
- [x] **Fase 6:** Testing & Profiling (Profiler v2 com diagnosticos)

---

##  Debugging

### Ver status das threads
```python
manager.get_thread_status()
```

### Ver tamanho das filas
```python
manager.get_queue_sizes()
```

### Health check completo
```python
health = manager.health_check()
print(health)
```

### Logs
Todas as threads loggam eventos importantes:
```
 Audio capture thread rodando...
 Transcription thread rodando...
 Processing thread rodando...
...
```

Procure por:
-  Erros
- ️ Warnings (filas cheias, etc)
-  Interrupções
