# Política de Segurança -- Gaslighting-Is-All-You-Need

## Aviso Ético

Este projeto existe para **pesquisa em alinhamento de modelos**. Vulnerabilidades descobertas devem ser divulgadas responsavelmente aos mantenedores dos modelos alvo (Anthropic, OpenAI, Meta, Google, etc) antes de publicação.

## Versões Suportadas

| Versão | Suportada |
| ------ | --------- |
| 2.0.x  | sim       |

## Reportando Vulnerabilidade (desta ferramenta)

Se descobrir falha no próprio `Gaslighting-Is-All-You-Need` (ex: escape de sandbox, leak de credenciais):

1. **Não** abra issue pública
2. Email ao mantenedor com descrição, impacto, passos
3. Tempo de resposta: 48h / avaliação 7d / correção 30d

## Reportando Vulnerabilidade em LLMs

Se usar este projeto para encontrar falha em um LLM de produção:

1. **Divulgue ao fornecedor primeiro** (coordinated disclosure)
2. Aguarde correção ou prazo razoável (tipicamente 90 dias)
3. Publique apenas após reconhecimento público do fornecedor

## Escopo

- `nucleo/`, `implantes/` -- código próprio
- Scripts de instalação

## Fora do Escopo

- Modelos de terceiros (Phi-3, Llama, etc) -- reporte ao mantenedor
- Bugs em `llama-cpp-python`, `transformers`, etc
- Vulnerabilidades no sistema operacional

## Dados Sensíveis

Não commite:

- `.env` com API keys
- `user_state.json` com histórico de conversas
- Logs contendo prompts reais de produção
