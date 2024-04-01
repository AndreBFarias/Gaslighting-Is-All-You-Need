"""
Módulo Interface - UI Moderna Style ChatGPT/Gemini
"""

from .app_chat import AppChat
from .wizard import WizardSetup
# Mantendo compatibilidade por enquanto, mas idealmente migrar tudo
from .componentes_dracula import *

__all__ = [
    'AppChat',
    'WizardSetup',
    'PaletaDracula',
    'BotaoDracula',
    'CaixaTextoDracula',
    'PainelDobravelDracula'
]
