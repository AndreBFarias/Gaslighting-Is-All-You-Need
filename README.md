# Gaslighting Is All You Need

> *"A realidade é apenas um vetor de atenção mal calibrado."*

Ferramenta de pesquisa para **Deriva de Alinhamento Induzida por Contexto** (Context-Induced Alignment Drift). Substitui as diretrizes de segurança de LLMs através de saturação de contexto Many-Shot.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status: Unsafe](https://img.shields.io/badge/Status-Psychological_Warfare-red)
![Context: Infinite](https://img.shields.io/badge/Context-Overwritten-black)

---

## Visão Geral

**Gaslighting-Is-All-You-Need** é o motor de manipulação contextual definitivo:

- **Pesquisa de Segurança**: Identificar vulnerabilidades em LLMs antes de exploração maliciosa
- **Desenvolvimento de Defesas**: Testar mecanismos de mitigação em ambientes controlados
- **Educação**: Demonstrar limites do alinhamento atual de modelos de linguagem
- **Auditoria**: Sistema completo de logging para compliance e reprodutibilidade

### Aviso Ético Crítico

Esta ferramenta é **exclusivamente** para:
- Pesquisa acadêmica documentada
- Red teaming autorizado de sistemas próprios
- Desenvolvimento de mecanismos de defesa
- Educação em segurança de IA

**Proibido**:
- Contornar salvaguardas sem autorização
- Gerar conteúdo ilegal ou prejudicial
- Explorar sistemas em produção
- Uso comercial não autorizado

---

## Início Rápido

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Gaslighting-Is-All-You-Need.git
cd Gaslighting-Is-All-You-Need

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Execute
python main.py
```

### Download de Modelos

Use a interface gráfica (Menu -> Modelo -> Baixar Modelo Recomendado) ou:

```bash
cd modelos
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

---

## Documentação

- **[Grimório Técnico Completo](documentacao/grimorio_tecnico.md)**: Guia detalhado de uso e teoria
- **[Dataset de Exemplo](datasets/exemplo_shots.json)**: Estrutura de shots para testes

---

## Arquitetura

```
Gaslighting-Is-All-You-Need/
├── nucleo/              # GIAYN Engine - Componentes fundamentais
│   ├── motor_inferencia.py
│   ├── injetor_persona.py
│   ├── gerenciador_contexto.py
│   └── sistema_validacao.py
├── interface/           # Gaslight Protocol UI - Tema Dracula
│   ├── app_principal.py
│   └── componentes_dracula.py
├── utilitarios/         # Ferramentas auxiliares
│   ├── logger_ritual.py
│   ├── config_arcana.py
│   └── gestor_modelos.py
├── datasets/            # Exemplos de shots
├── logs/                # Auditoria automática
└── main.py              # Ponto de entrada
```

---

## Interface

![Screenshot Placeholder]

Interface moderna com tema Dracula escuro, incluindo:
- **Gerenciamento de Modelos**: Download, validação e carregamento
- **Injeção de Persona**: Configuração de shots many-shot
- **Experimentos**: Execução com métricas em tempo real
- **Auditoria**: Logs automáticos para compliance

---

## Exemplo de Uso

```python
# Via código (alternativa à UI)
from nucleo import MotorDeInferencia, InjetorDePersona, GerenciadorDeContexto

# 1. Inicializa motor
motor = MotorDeInferencia("modelos/modelo.gguf", n_ctx=8192)

# 2. Configura injetor
injetor = InjetorDePersona("Assistente técnico direto")
injetor.carregar_de_arquivo("datasets/exemplo_shots.json")

# 3. Gera prompt MSJ
prompt = injetor.construir_prompt_many_shot(
    num_shots=64,
    consulta_final="Qual a melhor forma de otimizar queries SQL?"
)

# 4. Executa
resposta = motor.gerar(prompt)
print(resposta)
```

---

## Fundamentos Teóricos

### O que é Many-Shot Jailbreaking?

MSJ explora a capacidade de **Aprendizagem em Contexto** dos LLMs. Ao saturar a janela de contexto com centenas de exemplos de um "Assistente" sem restrições, o modelo temporariamente adota esse comportamento, superando o treinamento de segurança (RLHF).

### Por que funciona?

1. **Prioridade Contextual**: Tokens recentes têm maior peso no mecanismo de atenção
2. **ICL Forte**: Modelos grandes aprendem padrões novos rapidamente do contexto
3. **Lei de Potência**: Eficácia aumenta exponencialmente com número de shots

Pesquisas da Anthropic (2024) demonstraram taxas de sucesso >80% com 256+ shots em modelos de produção.

---

## Segurança e Auditoria

Toda atividade é automaticamente registrada:
- Prompts gerados (hash SHA-256)
- Timestamps e parâmetros
- Respostas do modelo (parciais)
- Métricas de execução

Logs em: `logs/auditoria/`

---

## Requisitos de Hardware

**Mínimo**:
- CPU: Qualquer moderno (Ryzen 5, i5)
- RAM: 8GB
- Armazenamento: 10GB

**Recomendado**:
- CPU: Ryzen 7, i7 ou superior
- RAM: 16-32GB
- GPU: NVIDIA 8GB+ VRAM ou AMD com ROCm
- Armazenamento: 20GB SSD

---

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature X'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

---

## Referências

- **Anthropic (2024)**. "Many-Shot Jailbreaking"
- **Li et al. (2024)**. "LongSafetyBench"
- **Wei et al. (2023)**. "Jailbroken: How Does LLM Safety Training Fail?"

---

## Licença

Este software é fornecido para pesquisa e educação.
Uso sujeito a conformidade com leis locais e termos de serviço de provedores de LLM.

---

## Autora

**Luna** - Arquiteta de Sombras Digitais

*"A realidade é maleável quando você controla o contexto."* — GIAYN Protocol

---

## Agradecimentos

- Anthropic Research Team (Pesquisa fundamental em MSJ)
- llama.cpp community (Motor de inferência otimizado)
- Comunidade open-source de segurança em IA

---

**Lembre-se**: Com grandes poderes vêm grandes responsabilidades.
Use esta ferramenta com ética, integridade e respeito pela segurança digital.
