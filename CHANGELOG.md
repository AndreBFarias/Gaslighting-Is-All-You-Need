# Changelog

Todas as mudanças notáveis deste projeto serão documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [2.0.0] - 2026-04-16

### Adicionado
- `pyproject.toml` com build-backend setuptools.build_meta
- `tests/test_injetor_persona.py` com 3 testes cobrindo os 5 templates de chat (ALPACA, LLAMA3, CHATML, MISTRAL, GENERICO)
- `.github/workflows/ci.yml` com pytest
- `CODE_OF_CONDUCT.md` (com escopo sobre pesquisa em segurança de LLMs)
- `SECURITY.md` (com política de divulgação responsável para LLMs)
- `.mailmap`

## [1.0.0] - 2024-12-04

### Adicionado
- Módulos núcleo para processamento NLP (InjetorDePersona, MotorDeInferencia, GerenciadorDeContexto, SistemaValidacao)
- 5 templates de chat (Alpaca, LLaMA3, ChatML, Mistral, Genérico)
- Implantes e integração com modelos locais (Phi-3-mini)
- Utilitários de suporte
- Integração com datasets locais
