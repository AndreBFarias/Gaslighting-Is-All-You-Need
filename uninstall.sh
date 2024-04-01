#!/bin/bash
set -e

APP_NAME="gaslighting-lab"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     Gaslighting Lab - Ritual de Desinstalação                    ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

APP_DIR="$HOME/.local/share/$APP_NAME"
DESKTOP_FILE="$HOME/.local/share/applications/$APP_NAME.desktop"

echo "️  Este script irá remover:"
echo "   • Aplicação ($APP_DIR)"
echo "   • Atalho do menu"
echo "   • Ícones do sistema"
echo "   • Ambiente virtual Python"
echo ""
echo "️  NÃO será removido:"
echo "   • Modelos baixados (se estiverem em $APP_DIR/modelos)"
echo "   • Logs e experimentos salvos"
echo ""

read -p "Deseja continuar? [s/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
    echo " Desinstalação cancelada"
    exit 0
fi

echo ""
echo "️  Removendo arquivos..."

if [ -d "$APP_DIR" ]; then
    echo "   → Removendo diretório da aplicação..."
    rm -rf "$APP_DIR"
    echo "    Aplicação removida"
else
    echo "   ℹ️  Diretório não encontrado (já removido?)"
fi

if [ -f "$DESKTOP_FILE" ]; then
    echo "   → Removendo atalho do menu..."
    rm "$DESKTOP_FILE"
    echo "    Atalho removido"
else
    echo "   ℹ️  Atalho não encontrado"
fi

echo "   → Removendo ícones do sistema..."
for size in 16 32 64 128 256; do
    ICON_FILE="$HOME/.local/share/icons/hicolor/${size}x${size}/apps/$APP_NAME.png"
    if [ -f "$ICON_FILE" ]; then
        rm "$ICON_FILE"
    fi
done
echo "    Ícones removidos"

echo ""
echo " Atualizando cache do sistema..."
update-desktop-database -q "$HOME/.local/share/applications" 2>/dev/null || true
gtk-update-icon-cache -q -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║          GASLIGHTING LAB REMOVIDO COM SUCESSO                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
