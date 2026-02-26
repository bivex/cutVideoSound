#!/usr/bin/env python3
"""
cut_video_sound.py
Удаляет аудиодорожку из видеофайла (macOS)
Требуется: ffmpeg
"""

import argparse
import subprocess
import sys
import os


def check_ffmpeg():
    """Проверка наличия ffmpeg"""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def remove_audio(input_file, output_file=None):
    """Удаляет аудиодорожку из видео"""

    if not os.path.exists(input_file):
        print(f"❌ Ошибка: Файл '{input_file}' не найден")
        sys.exit(1)

    # Генерация имени выходного файла
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_no_audio{ext}"

    print(f"🎬 Обработка: {input_file}")
    print(f"📁 Результат:  {output_file}")
    print()

    # Запуск ffmpeg
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-c:v", "copy",  # Копировать видео без перекодирования
        "-an",           # Отключить аудио
        "-y",            # Перезаписать, если файл существует
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Готово! Видеофайл без звука сохранён: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Произошла ошибка при обработке")
        sys.exit(1)


def main():
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

    parser.add_argument("input", help="Входной видеофайл")
    parser.add_argument("output", nargs="?", help="Выходной файл (необязательно)")

    args = parser.parse_args()

    if not check_ffmpeg():
        print("❌ Ошибка: ffmpeg не установлен")
        print()
        print("Установите ffmpeg через Homebrew:")
        print("  brew install ffmpeg")
        sys.exit(1)

    remove_audio(args.input, args.output)


if __name__ == "__main__":
    main()
