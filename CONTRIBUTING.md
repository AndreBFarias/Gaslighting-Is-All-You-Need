# Contribuindo com Gaslighting-Is-All-You-Need

## Configuração do ambiente

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv && source venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure os modelos locais conforme documentação

## Fluxo de contribuição

1. Abra uma issue descrevendo a mudança proposta
2. Faça fork do repositório
3. Crie um branch: `git checkout -b fix/nome-da-correcao`
4. Implemente as mudanças
5. Abra um Pull Request referenciando a issue

## Padrões de código

- Python 3.10+
- Type hints obrigatórios
- Docstrings em PT-BR
- Logging via `logging` padrão (nunca `print()`)
- Formatação: seguir PEP 8

## Módulos

- `nucleo/`: lógica central de processamento
- `implantes/`: extensões e módulos plug-in
- `modelos/`: wrappers de modelos de linguagem
- `utilitarios/`: funções auxiliares compartilhadas

## Mensagens de commit

Formato: `tipo: descrição imperativa em PT-BR`

Tipos: `feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `chore`

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob GPLv3.
