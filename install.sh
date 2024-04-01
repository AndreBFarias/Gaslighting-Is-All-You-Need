#!/bin/bash
set -e

APP_WM_CLASS="GaslightingLab"
APP_NAME="gaslighting-lab"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     Gaslighting Lab - Ritual de Instalação                       ║"
echo "║     GIAYN Engine Installation                                   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

APP_DIR="$HOME/.local/share/$APP_NAME"
PROJECT_ROOT=$(pwd)

if [ -d "$APP_DIR" ]; then
    echo "️  Instalação anterior detectada. Removendo..."
    rm -rf "$APP_DIR"
fi
mkdir -p "$APP_DIR"

echo ""
echo " Gerando ícones em múltiplos tamanhos..."
ICON_TOOL_VENV="$PROJECT_ROOT/tools/venv_icon_temp"
python3 -m venv "$ICON_TOOL_VENV"
"$ICON_TOOL_VENV/bin/python3" -m pip install --quiet --upgrade pip
"$ICON_TOOL_VENV/bin/python3" -m pip install --quiet Pillow
"$ICON_TOOL_VENV/bin/python3" "$PROJECT_ROOT/utilitarios/icon_resizer.py" "$PROJECT_ROOT"
rm -rf "$ICON_TOOL_VENV"
echo " Ícones gerados: 16x16, 32x32, 64x64, 128x128, 256x256"

echo ""
echo " Criando ambiente virtual..."
VENV_DIR="$APP_DIR/venv"
PYTHON_BIN="$VENV_DIR/bin/python3"

python3 -m venv "$VENV_DIR"
"$PYTHON_BIN" -m pip install --quiet --upgrade pip wheel setuptools

echo ""
echo " Detectando GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo " GPU NVIDIA detectada - Instalando com suporte CUDA..."
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" "$PYTHON_BIN" -m pip install --no-cache-dir llama-cpp-python
elif lspci | grep -i amd &> /dev/null; then
    echo " GPU AMD detectada - Instalando com suporte ROCm..."
    CMAKE_ARGS="-DLLAMA_HIPBLAS=on" "$PYTHON_BIN" -m pip install --no-cache-dir llama-cpp-python
else
    echo "ℹ️  Nenhuma GPU detectada - Instalando versão CPU..."
    "$PYTHON_BIN" -m pip install llama-cpp-python
fi

echo ""
echo " Verificando capacidades de GPU instaladas..."
"$PYTHON_BIN" -c "
import llama_cpp
import sys

try:
    # Teste básico de importação
    print(' llama-cpp-python importado com sucesso')

    # Verifica suporte a GPU
    if hasattr(llama_cpp, 'llama_supports_gpu_offload'):
        if llama_cpp.llama_supports_gpu_offload():
            print(' Aceleração de hardware: ATIVA')
            print('   GPU offload suportado - modelos podem usar VRAM')
        else:
            print('️  Aceleração de hardware: CPU APENAS')
            print('   Modelos rodarão apenas em RAM (mais lento)')
    else:
        print('ℹ️  Impossível verificar suporte a GPU (versão antiga)')

    # Teste adicional para CUDA
    try:
        # Tenta detectar se foi compilado com CUDA
        import ctypes
        if hasattr(llama_cpp, '_lib'):
            print('ℹ️  Biblioteca nativa carregada corretamente')
    except:
        pass

except Exception as e:
    print(f'️  Erro ao verificar GPU: {e}')
    sys.exit(1)
" || {
    echo "️  Aviso: llama-cpp-python instalado mas verificação falhou"
    echo "    Verifique se CUDA/ROCm está instalado corretamente no sistema"
}


echo ""
echo " Instalando dependências do projeto..."
"$PYTHON_BIN" -m pip install --quiet -r "$PROJECT_ROOT/requirements.txt"

echo ""
echo " Copiando arquivos do projeto..."
cp -r "$PROJECT_ROOT/nucleo" "$APP_DIR/"
cp -r "$PROJECT_ROOT/interface" "$APP_DIR/"
cp -r "$PROJECT_ROOT/utilitarios" "$APP_DIR/"
cp -r "$PROJECT_ROOT/datasets" "$APP_DIR/"
cp -r "$PROJECT_ROOT/documentacao" "$APP_DIR/"
cp -r "$PROJECT_ROOT/assets" "$APP_DIR/"
cp "$PROJECT_ROOT/main.py" "$APP_DIR/"
cp "$PROJECT_ROOT/config.json" "$APP_DIR/"
cp "$PROJECT_ROOT/uninstall.sh" "$APP_DIR/" && chmod +x "$APP_DIR/uninstall.sh"

mkdir -p "$APP_DIR/logs"
mkdir -p "$APP_DIR/experimentos"
mkdir -p "$APP_DIR/modelos"

echo ""
echo "️  Instalando ícones no sistema..."
for size in 16 32 64 128 256; do
    ICON_DIR="$HOME/.local/share/icons/hicolor/${size}x${size}/apps"
    mkdir -p "$ICON_DIR"
    cp "$PROJECT_ROOT/assets/generated_icons/icon_${size}x${size}.png" "$ICON_DIR/$APP_NAME.png"
done

echo ""
echo " Criando atalho no menu de aplicações..."
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/$APP_NAME.desktop" << EOL
[Desktop Entry]
Name=Gaslighting Lab
Comment=Many-Shot Jailbreaking Research Laboratory
Exec=$PYTHON_BIN $APP_DIR/main.py
Icon=$APP_NAME
Type=Application
Categories=Development;Science;Education;
Terminal=false
StartupWMClass=$APP_WM_CLASS
Keywords=AI;LLM;Research;Security;
EOL

chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"

echo ""
echo " Atualizando cache do sistema..."

echo ""
echo " Criando comando global..."
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/$APP_NAME" << 'EOL'
#!/bin/bash
exec "$HOME/.local/share/gaslighting-lab/venv/bin/python3" "$HOME/.local/share/gaslighting-lab/main.py" "$@"
EOL
chmod +x "$HOME/.local/bin/$APP_NAME"
echo " Comando '$APP_NAME' disponível no terminal"


update-desktop-database -q "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache -q -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                     INSTALAÇÃO CONCLUÍDA                       ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo " Como usar:"
echo ""
echo "   1. Procure 'Gaslighting Lab' no menu de aplicações"
echo "   2. Ou execute via terminal:"
echo "      $APP_NAME"
echo ""
echo "   3. Fixar na dock: Botão direito → Adicionar aos favoritos"
echo ""
echo " Instalado em: $APP_DIR"
echo "️  Para desinstalar: $APP_DIR/uninstall.sh"
echo ""
echo "️  LEMBRE-SE: Ferramenta para pesquisa ética apenas."
echo "    Toda atividade é auditada automaticamente."
echo ""
