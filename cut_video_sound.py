#!/usr/bin/env python3
"""
cut_video_sound.py
Удаляет аудиодорожку из видеофайла (macOS)
Требуется: ffmpeg
"""

import argparse
import subprocess
import sys
from pathlib import Path

def die(msg: str, hint: str | None = None) -> None:
    """Выводит ошибку и завершает работу"""
    print(f"❌ Ошибка: {msg}", file=sys.stderr)
    if hint:
        print(hint, file=sys.stderr)
    sys.exit(1)

def remove_audio(input_path: Path, output_path: Path | None = None) -> None:
    """Удаляет аудиодорожку из видео"""

    if not input_path.exists():
        die(f"Файл не найден: '{input_path}'")

    # Генерация имени выходного файла
    if output_path is None:
        output_path = input_path.with_stem(f"{input_path.stem}_no_audio")

    if output_path.exists():
        die(f"Выходной файл уже существует: '{output_path}'",
            "Удалите его или укажите другое имя")

    print(f"🎬 Обработка: {input_path}")
    print(f"📁 Результат:  {output_path}\n")

    # Запуск ffmpeg (stream copy без перекодирования)
    try:
        subprocess.run(
            ["ffmpeg", "-nostdin", "-loglevel", "warning",
             "-i", str(input_path), "-c:v", "copy", "-an", "-y", str(output_path)],
            check=True,
            capture_output=True
        )
        print(f"✅ Готово! Видеофайл без звука сохранён: {output_path}")
    except subprocess.CalledProcessError:
        die("Произошла ошибка при обработке")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Удаляет аудиодорожку из видеофайла",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s input.mp4
  %(prog)s input.mov output.mp4

Установка ffmpeg на macOS:
  brew install ffmpeg
        """
    )

    parser.add_argument("input", type=Path, help="Входной видеофайл")
    parser.add_argument("output", type=Path, nargs="?", help="Выходной файл")

    args = parser.parse_args()

    # Проверка ffmpeg (быстрее через shutil.which)
    from shutil import which
    if not which("ffmpeg"):
        die("ffmpeg не установлен", "Установите: brew install ffmpeg")

    remove_audio(args.input, args.output)

if __name__ == "__main__":
    main()
