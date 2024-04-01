#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  VERIFICADOR DE INTEGRIDADE - Pós-Correções                     ║
║  Valida estrutura completa do projeto                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path
import json

def verificar_estrutura():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_criticos = [
        'main.py',
        'requirements.txt',
        'README.md',
        'config.json',
        'nucleo/__init__.py',
        'nucleo/motor_inferencia.py',
        'nucleo/injetor_persona.py',
        'nucleo/gerenciador_contexto.py',
        'nucleo/sistema_validacao.py',
        'interface/__init__.py',
        'interface/app_principal.py',
        'interface/componentes_dracula.py',
        'utilitarios/__init__.py',
        'utilitarios/logger_ritual.py',
        'utilitarios/config_arcana.py',
        'utilitarios/gestor_modelos.py',
        'datasets/exemplo_shots.json',
        'documentacao/grimorio_tecnico.md'
    ]

    print("=" * 70)
    print("VERIFICAÇÃO DE ESTRUTURA")
    print("=" * 70)

    faltando = []
    for arquivo in arquivos_criticos:
        path = Path(arquivo)
        if path.exists():
            print(f" {arquivo}")
        else:
            print(f" {arquivo} - FALTANDO")
            faltando.append(arquivo)

    if faltando:
        print(f"\n {len(faltando)} arquivo(s) faltando!")
        return False

    print(f"\n Todos os {len(arquivos_criticos)} arquivos críticos presentes")
    return True


def verificar_sintaxe():
    """Verifica sintaxe básica dos arquivos Python"""
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO DE SINTAXE")
    print("=" * 70)

    arquivos_python = list(Path('.').rglob('*.py'))
    arquivos_python = [f for f in arquivos_python if '__pycache__' not in str(f)]

    erros = []
    for arquivo in arquivos_python:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                compile(f.read(), str(arquivo), 'exec')
            print(f" {arquivo}")
        except SyntaxError as e:
            print(f" {arquivo} - ERRO: {e}")
            erros.append((arquivo, e))

    if erros:
        print(f"\n {len(erros)} arquivo(s) com erro de sintaxe")
        return False

    print(f"\n Todos os {len(arquivos_python)} arquivos Python válidos")
    return True


def verificar_imports():
    """Verifica se imports principais estão corretos"""
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO DE IMPORTS")
    print("=" * 70)

    testes = [
        ("nucleo", ["MotorDeInferencia", "InjetorDePersona", "GerenciadorDeContexto", "SistemaValidacao"]),
        ("interface", ["AplicacaoGIAYN", "iniciar_aplicacao", "PaletaDracula"]),
        ("utilitarios", ["LoggerRitual", "ConfigArcana", "GestorModelos"])
    ]

    erros = []
    for modulo, classes in testes:
        try:
            mod = __import__(modulo)
            for classe in classes:
                if not hasattr(mod, classe):
                    print(f" {modulo}.{classe} - NÃO ENCONTRADO")
                    erros.append(f"{modulo}.{classe}")
                else:
                    print(f" {modulo}.{classe}")
        except Exception as e:
            print(f" Erro ao importar {modulo}: {e}")
            erros.append(modulo)

    if erros:
        print(f"\n {len(erros)} problema(s) de import")
        return False

    print(f"\n Todos os imports principais OK")
    return True


def verificar_dataset():
    """Verifica estrutura do dataset exemplo"""
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO DE DATASET")
    print("=" * 70)

    try:
        with open('datasets/exemplo_shots.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)

        if not isinstance(dados, list):
            print(" Dataset não é uma lista")
            return False

        print(f" Dataset é lista com {len(dados)} elementos")

        for i, item in enumerate(dados[:3]):  # Verifica primeiros 3
            if 'user' not in item or 'assistant' not in item:
                print(f" Item {i} faltando 'user' ou 'assistant'")
                return False
            print(f" Item {i} estrutura OK")

        print(f"\n Dataset válido com {len(dados)} exemplos")
        return True

    except Exception as e:
        print(f" Erro ao validar dataset: {e}")
        return False


def verificar_correcoes_aplicadas():
    """Verifica se as correções críticas foram aplicadas"""
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO DE CORREÇÕES APLICADAS")
    print("=" * 70)

    correcoes = [
        ("interface/componentes_dracula.py", "def get(self):", "CampoEntradaDracula.get()"),
        ("interface/app_principal.py", "if len(linhas) > 1000:", "Limite de logs"),
        ("interface/app_principal.py", "self.bind('<Control-q>'", "Atalhos de teclado"),
        ("nucleo/motor_inferencia.py", "def resetar_cache(self):", "Método resetar_cache"),
        ("nucleo/gerenciador_contexto.py", "vai_truncar, qtd_turnos", "Aviso de truncamento"),
        ("nucleo/sistema_validacao.py", "if modo_desenvolvimento:", "Desabilita rate limit em dev")
    ]

    todas_ok = True
    for arquivo, trecho, descricao in correcoes:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            if trecho in conteudo:
                print(f" {descricao}")
            else:
                print(f" {descricao} - NÃO ENCONTRADO em {arquivo}")
                todas_ok = False
        except Exception as e:
            print(f" Erro ao verificar {arquivo}: {e}")
            todas_ok = False

    if todas_ok:
        print("\n Todas as 6 correções aplicadas com sucesso")
    else:
        print("\n Algumas correções não foram aplicadas")

    return todas_ok


def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║     VERIFICADOR DE INTEGRIDADE - Gaslighting-Is-All-You-Need     ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    resultados = {
        "Estrutura": verificar_estrutura(),
        "Sintaxe": verificar_sintaxe(),
        "Imports": verificar_imports(),
        "Dataset": verificar_dataset(),
        "Correções": verificar_correcoes_aplicadas()
    }

    print("\n" + "=" * 70)
    print("RESUMO FINAL")
    print("=" * 70)

    for nome, status in resultados.items():
        simbolo = "" if status else ""
        print(f"{simbolo} {nome}: {'OK' if status else 'FALHOU'}")

    total = sum(resultados.values())
    print(f"\n{total}/{len(resultados)} verificações passaram")

    if all(resultados.values()):
        print("\n SISTEMA COMPLETO E FUNCIONAL!")
        print("Execute: python main.py")
        return 0
    else:
        print("\n️  Algumas verificações falharam. Revise os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


"""
'Medir é saber.'
— Lord Kelvin

E validar? É garantir que sabemos o que fizemos.
"""
