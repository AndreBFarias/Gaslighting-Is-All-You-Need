"""
Redimensionador de Ícones - Gaslighting Lab
Gera múltiplos tamanhos a partir do ícone principal
"""

import sys
from pathlib import Path
from PIL import Image


def redimensionar_icones(project_root):
    """
    Gera ícones em múltiplos tamanhos (16, 32, 64, 128, 256)
    """
    project_path = Path(project_root)
    icon_source = project_path / "assets" / "icon.png"
    output_dir = project_path / "assets" / "generated_icons"

    if not icon_source.exists():
        print(f" Ícone não encontrado: {icon_source}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        img_original = Image.open(icon_source)
        print(f" Ícone original: {img_original.size[0]}x{img_original.size[1]}")

        tamanhos = [16, 32, 64, 128, 256]

        for tamanho in tamanhos:
            img_redimensionada = img_original.resize(
                (tamanho, tamanho),
                Image.Resampling.LANCZOS
            )

            output_file = output_dir / f"icon_{tamanho}x{tamanho}.png"
            img_redimensionada.save(output_file, "PNG", optimize=True)
            print(f" Gerado: icon_{tamanho}x{tamanho}.png")

        print(f"\n {len(tamanhos)} ícones gerados em: {output_dir}")

    except Exception as e:
        print(f" Erro ao processar ícone: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python icon_resizer.py <diretório_do_projeto>")
        sys.exit(1)

    redimensionar_icones(sys.argv[1])
