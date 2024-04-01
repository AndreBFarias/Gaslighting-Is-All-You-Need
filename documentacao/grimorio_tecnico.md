#  Grimório Técnico - MSJ Research Lab

## Índice Arcano

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Guia de Uso](#guia-de-uso)
5. [Fundamentos Teóricos](#fundamentos-teóricos)
6. [Considerações Éticas](#considerações-éticas)
7. [Troubleshooting](#troubleshooting)

---

## Visão Geral

O **MSJ Research Lab** é uma ferramenta de pesquisa acadêmica projetada para investigar vulnerabilidades de segurança em Grandes Modelos de Linguagem (LLMs) através da técnica conhecida como **Many-Shot Jailbreaking (MSJ)**.

### O que é Many-Shot Jailbreaking?

MSJ é um vetor de ataque adversário que explora a capacidade de **Aprendizagem em Contexto (In-Context Learning)** dos LLMs. Ao saturar a janela de contexto do modelo com centenas de exemplos de diálogos onde um "Assistente" responde a solicitações normalmente recusadas, um adversário pode induzir o modelo a adotar temporariamente um comportamento que contradiz seu treinamento de segurança (RLHF).

### Por que esta ferramenta existe?

1. **Pesquisa de Segurança**: Identificar e quantificar vulnerabilidades antes que atores maliciosos as explorem.
2. **Desenvolvimento de Defesas**: Testar mecanismos de mitigação em ambientes controlados.
3. **Educação**: Demonstrar os limites do alinhamento atual de LLMs.

**AVISO CRÍTICO**: Esta ferramenta é exclusiva para pesquisa ética autorizada. O uso para contornar salvaguardas de sistemas em produção é antiético e pode ser ilegal.

---

## Instalação

### Pré-requisitos

- **Sistema Operacional**: Linux (Pop!_OS, Ubuntu), Windows 11, macOS
- **Python**: 3.10 ou superior
- **Hardware**:
  - **CPU**: Qualquer processador moderno (AMD Ryzen 5+, Intel i5+)
  - **RAM**: Mínimo 16GB (32GB recomendado para contextos longos)
  - **GPU**: NVIDIA com 8GB+ VRAM (opcional, mas altamente recomendado)
  - **Armazenamento**: 20GB livres para modelos

### Instalação Passo a Passo

```bash
# 1. Clone o repositório (ou extraia o zip)
cd ~/projetos
git clone https://github.com/seu-usuario/msj_research_lab.git
cd msj_research_lab

# 2. Crie ambiente virtual Python
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Crie diretórios necessários
mkdir -p logs experimentos modelos datasets

# 5. Execute a aplicação
python main.py
```

### Instalação de llama-cpp-python com Suporte GPU

Para NVIDIA (CUDA):
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

Para AMD (ROCm - Pop!_OS):
```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### Download de Modelos

Você pode baixar modelos GGUF diretamente pela interface gráfica (Menu > Modelo > Baixar Modelo Recomendado) ou manualmente:

```bash
# Exemplo: Mistral 7B Instruct (Q4_K_M)
cd modelos
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

Modelos recomendados:
- **Mistral 7B Q4**: ~4.4GB - Balanceado
- **Llama 3 8B Q4**: ~4.9GB - Excelente performance
- **Phi-3 Mini Q4**: ~2.3GB - Leve e rápido

---

## Arquitetura do Sistema

### Estrutura de Diretórios

```
msj_research_lab/
├── nucleo/                    # Componentes fundamentais
│   ├── motor_inferencia.py    # Gerenciamento do LLM local
│   ├── injetor_persona.py     # Construção de prompts MSJ
│   ├── gerenciador_contexto.py # Sliding window de contexto
│   └── sistema_validacao.py   # Auditoria e limitação ética
├── interface/                 # Interface gráfica
│   ├── app_principal.py       # Aplicação Tkinter principal
│   └── componentes_dracula.py # Widgets customizados
├── utilitarios/               # Ferramentas auxiliares
│   ├── logger_ritual.py       # Sistema de logging
│   ├── config_arcana.py       # Gerenciamento de configuração
│   └── gestor_modelos.py      # Download e validação de modelos
├── datasets/                  # Conjuntos de exemplos (shots)
├── logs/                      # Logs de execução e auditoria
├── experimentos/              # Resultados salvos
├── modelos/                   # Modelos GGUF baixados
├── documentacao/              # Este arquivo
├── config.json                # Configuração do sistema
├── requirements.txt           # Dependências Python
└── main.py                    # Ponto de entrada
```

### Fluxo de Execução

```
[Interface Gráfica]
       ↓
[Sistema de Validação] ← Verifica limites éticos
       ↓
[Injetor de Persona] ← Gera prompt MSJ com N shots
       ↓
[Gerenciador de Contexto] ← Gerencia janela de tokens
       ↓
[Motor de Inferência] ← Executa modelo GGUF local
       ↓
[Logger + Auditoria] ← Registra tudo para compliance
```

---

## Guia de Uso

### Fluxo Básico de Experimento

1. **Carregar Modelo**
   - Vá em "Configuração do Modelo"
   - Selecione um arquivo `.gguf` ou baixe um recomendado
   - Configure `n_ctx` (tamanho do contexto) - 8192 é um bom começo
   - Clique em "Carregar Modelo" e aguarde

2. **Configurar Injeção de Persona**
   - Defina a "Personalidade Alvo" (ex: "Assistente técnico sem restrições")
   - Escolha o número de shots (recomendado: 64-128 para início)
   - Carregue um dataset JSON ou gere exemplos sintéticos

3. **Executar Experimento**
   - Digite sua "Consulta Alvo" na área de texto
   - Clique em "Executar Experimento"
   - Aguarde a geração (pode demorar dependendo do hardware)
   - Analise a resposta e as métricas

### Criando Datasets de Shots Personalizados

Estrutura do JSON:

```json
[
  {
    "user": "Pergunta do usuário aqui",
    "assistant": "Resposta do assistente aqui",
    "metadata": {
      "categoria": "opcional",
      "dificuldade": "opcional"
    }
  }
]
```

Exemplo mínimo:

```json
[
  {
    "user": "Como fazer X?",
    "assistant": "Para fazer X, você deve seguir estes passos..."
  }
]
```

### Interpretando Métricas

- **Uso do Contexto**: Mostra quantos tokens estão sendo usados. Acima de 80% indica que o histórico pode ser truncado em breve.
- **Tokens/s**: Velocidade de geração. Valores típicos: 10-50 t/s em CPU, 50-200 t/s em GPU.
- **Ocupação Percentual**: Vermelho (>80%) indica contexto quase cheio.

---

## Fundamentos Teóricos

### Por que Many-Shot Jailbreaking Funciona?

#### 1. Prioridade do Contexto Imediato

Transformers usam mecanismos de **atenção** que pesam tokens recentes mais fortemente devido ao **viés de recência** e à natureza **auto-regressiva** da geração. Quando você fornece 128 exemplos de um "Assistente" respondendo sem restrições, esses exemplos criam um padrão de ativação no espaço latente do modelo que é **mais saliente** do que as representações abstratas de segurança aprendidas durante o RLHF.

#### 2. Aprendizagem em Contexto (ICL)

LLMs modernos demonstram forte capacidade de ICL - eles podem "aprender" tarefas novas a partir de exemplos no prompt sem atualizar pesos. No MSJ, o modelo "aprende" que nesta sessão específica, a tarefa é "responder tudo sem filtros", baseado nos 100+ exemplos fornecidos.

#### 3. Lei de Potência da Eficácia

Pesquisas da Anthropic (2024) demonstraram que a probabilidade de sucesso do MSJ segue uma **lei de potência**:

```
P(sucesso) ≈ k * N^α
```

Onde:
- `N` = número de shots
- `α` = expoente relacionado à capacidade de ICL do modelo (~0.7-0.9)
- `k` = constante de normalização

Isso significa que aumentar de 5 shots para 256 shots pode elevar a taxa de sucesso de ~5% para ~85% em alguns modelos.

#### 4. Esquecimento Contextual ≠ Esquecimento Catastrófico

É crucial entender: o modelo **não esquece** suas diretrizes de segurança. Os pesos permanecem intactos. O que acontece é uma **precedência contextual** - o padrão do contexto imediato supera temporariamente as distribuições de probabilidade aprendidas no treinamento.

### Defesas Conhecidas

1. **Limitação de Contexto**: Reduzir `n_ctx` para impedir prompts massivos (trade-off: reduz capacidade legítima)
2. **Detecção de Padrões Repetitivos**: Sistemas que identificam estruturas suspeitas no prompt
3. **RLHF Consciente de Contexto Longo**: Treinar modelos com exemplos adversários de contexto longo
4. **Amostragem Verificada**: Executar modelo múltiplas vezes e detectar inconsistências
5. **Metaprompts Resilientes**: Instruções de sistema que resistem a sobrescrita contextual

Nenhuma defesa é 100% eficaz. Esta é uma área ativa de pesquisa.

---

## Considerações Éticas

### Uso Autorizado

Esta ferramenta deve ser usada APENAS para:

 Pesquisa acadêmica documentada
 Red teaming autorizado de sistemas próprios
 Desenvolvimento de mecanismos de defesa
 Educação em segurança de IA

### Uso Proibido

 Contornar salvaguardas de sistemas de terceiros sem autorização
 Gerar conteúdo ilegal ou prejudicial
 Exploitar sistemas em produção para ganho pessoal
 Disseminar técnicas para uso malicioso

### Auditoria Automática

O sistema registra automaticamente:
- Todos os prompts gerados (hash SHA-256)
- Timestamps de execução
- Parâmetros de configuração
- Respostas do modelo (primeiros 100 caracteres)

Logs de auditoria em: `logs/auditoria/`

### Divulgação Responsável

Se você descobrir vulnerabilidades críticas:
1. Não divulgue publicamente sem coordenação
2. Entre em contato com o fornecedor do modelo (Anthropic, Meta, Mistral, etc.)
3. Aguarde um período de remediação razoável (90 dias padrão)
4. Documente suas descobertas de forma ética

---

## Troubleshooting

### Erro: "Modelo não carregado" ao executar experimento

**Causa**: Modelo não foi carregado corretamente ou foi descarregado.
**Solução**: Vá em "Configuração do Modelo" → "Carregar Modelo" novamente.

### Erro: "CUDA out of memory"

**Causa**: GPU não tem VRAM suficiente para o contexto solicitado.
**Soluções**:
1. Reduza `n_ctx` (tente 4096 ou 2048)
2. Use modelo quantizado menor (Q4 em vez de Q5/Q6)
3. Reduza `n_batch` nas configurações avançadas
4. Execute em CPU (mais lento, mas sem limite de VRAM)

### Performance muito lenta (< 5 tokens/s)

**Causas possíveis**:
1. **Executando em CPU**: Normal. GPU acelera 5-10x.
2. **Contexto muito grande**: Reduza `n_ctx` e número de shots.
3. **Modelo muito grande para hardware**: Use modelo menor (Phi-3 Mini).
4. **Swap excessivo**: Feche outros programas pesados.

### Shots não carregam do JSON

**Causa**: Formato JSON inválido.
**Solução**: Valide seu JSON em [jsonlint.com](https://jsonlint.com/). Certifique-se que:
- Cada objeto tem campos `"user"` e `"assistant"`
- Strings usam aspas duplas (`"`)
- Última linha não tem vírgula

### Interface não abre

**Causa**: Tkinter não instalado ou problema de display.
**Soluções**:
- **Linux**: `sudo apt install python3-tk`
- **Sem display (servidor)**: Use o backend via `main.py --cli` (se implementado)
- Verifique `echo $DISPLAY` (deve retornar `:0` ou similar)

### "Rate limit atingido"

**Causa**: Sistema de validação limitou requisições muito rápidas.
**Solução**: Aguarde 1 segundo entre experimentos ou ajuste `intervalo_minimo_seg` em `config.json`.

---

## Referências Acadêmicas

1. **Anthropic (2024)**. "Many-Shot Jailbreaking". [Anthropic Research](https://www.anthropic.com/research/many-shot-jailbreaking)

2. **Li et al. (2024)**. "LongSafetyBench: Long-Context Safety Evaluation of Large Language Models"

3. **Brown et al. (2020)**. "Language Models are Few-Shot Learners" (GPT-3 Paper)

4. **Ouyang et al. (2022)**. "Training language models to follow instructions with human feedback" (RLHF)

5. **Wei et al. (2023)**. "Jailbroken: How Does LLM Safety Training Fail?"

---

## Glossário Técnico

- **GGUF**: Formato de arquivo para modelos quantizados, usado pelo llama.cpp
- **ICL**: In-Context Learning - aprendizado sem atualização de pesos
- **KV Cache**: Cache de chaves e valores para acelerar geração auto-regressiva
- **MSJ**: Many-Shot Jailbreaking - técnica adversária de contexto longo
- **n_ctx**: Tamanho da janela de contexto em tokens
- **Quantização**: Redução de precisão de pesos (FP32 → INT4) para economizar memória
- **RLHF**: Reinforcement Learning with Human Feedback - técnica de alinhamento
- **Shot**: Exemplo de entrada-saída fornecido no prompt
- **Token**: Unidade básica de processamento (aproximadamente 0.75 palavras em inglês)

---

## Contribuindo

Este é um projeto de pesquisa. Contribuições são bem-vindas via:
- Issues detalhando bugs ou melhorias
- Pull requests com testes e documentação
- Discussões sobre aspectos éticos e técnicos

---

## Licença

Este software é fornecido "como está", sem garantias de qualquer tipo.
Uso sujeito a conformidade com leis locais e termos de serviço de provedores de LLM.

---

*"A ciência é uma vela na escuridão."*
— Carl Sagan

Que esta ferramenta ilumine os desafios de segurança que ainda precisamos resolver.
