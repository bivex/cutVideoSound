#!/bin/bash

# cut-video-sound.sh
# Удаляет аудиодорожку из видеофайла (macOS)
# Требуется: ffmpeg

set -e

usage() {
    echo "Использование: $0 <входной_файл> [выходной_файл]"
    echo ""
    echo "Примеры:"
    echo "  $0 input.mp4"
    echo "  $0 input.mov output.mp4"
    exit 1
}

# Проверка аргументов
if [ $# -lt 1 ]; then
    usage
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.*}_no_audio.${INPUT_FILE##*.}}"

# Проверка существования входного файла
if [ ! -f "$INPUT_FILE" ]; then
    echo "Ошибка: Файл '$INPUT_FILE' не найден"
    exit 1
fi

# Проверка наличия ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Ошибка: ffmpeg не установлен"
    echo ""
    echo "Установите ffmpeg через Homebrew:"
    echo "  brew install ffmpeg"
    exit 1
fi

echo "Обработка: $INPUT_FILE"
echo "Результат:  $OUTPUT_FILE"
echo ""

# Удаление аудиодорожки с помощью ffmpeg
ffmpeg -i "$INPUT_FILE" -c:v copy -an "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Готово! Видеофайл без звука сохранён: $OUTPUT_FILE"
else
    echo ""
    echo "❌ Произошла ошибка при обработке"
    exit 1
fi
