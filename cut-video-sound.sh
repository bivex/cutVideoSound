#!/bin/bash

# cut-video-sound.sh
# Удаляет аудиодорожку из видеофайла (macOS)
# Требуется: ffmpeg

set -e

die() {
    echo "Ошибка: $1" >&2
    [ -n "$2" ] && echo "$2" >&2
    exit 1
}

# Проверка аргументов
[ $# -lt 1 ] && die "Укажите входной файл" \
    "Использование: $0 <входной_файл> [выходной_файл]"

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.*}_no_audio.${INPUT_FILE##*.}}"

# Проверки
[ -f "$INPUT_FILE" ] || die "Файл не найден: '$INPUT_FILE'"
[ -e "$OUTPUT_FILE" ] && die "Выходной файл уже существует: '$OUTPUT_FILE'" "Удалите его или укажите другое имя"
command -v ffmpeg >/dev/null || die "ffmpeg не установлен" "Установите: brew install ffmpeg"

echo "Обработка: $INPUT_FILE"
echo "Результат:  $OUTPUT_FILE"
echo

# Удаление аудиодорожки (stream copy без перекодирования)
ffmpeg -nostdin -loglevel warning -i "$INPUT_FILE" -c:v copy -an "$OUTPUT_FILE" -y

echo "✅ Готово! Видеофайл без звука сохранён: $OUTPUT_FILE"
