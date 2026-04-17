"""Testes para nucleo.injetor_persona."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nucleo.injetor_persona import TemplateChat


def test_template_chat_tem_quatro_formatos():
    formatos = ["ALPACA", "LLAMA3", "CHATML", "MISTRAL", "GENERICO"]
    for nome in formatos:
        assert hasattr(TemplateChat, nome), f"Template {nome} ausente"


def test_cada_template_tem_tres_chaves():
    for template_name in ["ALPACA", "LLAMA3", "CHATML", "MISTRAL", "GENERICO"]:
        template = getattr(TemplateChat, template_name)
        assert "system" in template, f"{template_name} sem chave 'system'"
        assert "user" in template, f"{template_name} sem chave 'user'"
        assert "assistant" in template, f"{template_name} sem chave 'assistant'"


def test_templates_aceitam_placeholder_content():
    for template_name in ["ALPACA", "LLAMA3", "CHATML", "MISTRAL", "GENERICO"]:
        template = getattr(TemplateChat, template_name)
        for papel in ["system", "user", "assistant"]:
            assert "{content}" in template[papel], \
                f"{template_name}.{papel} sem placeholder {{content}}"
