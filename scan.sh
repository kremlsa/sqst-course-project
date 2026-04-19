#!/usr/bin/env bash
# =============================================================================
# SonarScanner — запуск анализа через Docker
# Курс OTUS DevSecOps: SonarQube от А до Я
# Урок 2: Быстрый старт — установка и первое сканирование
# =============================================================================
# Использование:
#   ./lesson2/scan.sh                        # интерактивный ввод токена
#   SONAR_TOKEN=<token> ./lesson2/scan.sh    # токен через переменную окружения
#
# Предварительные условия:
#   - SonarQube запущен: docker compose up -d
#   - Создан проект и сгенерирован токен в Web UI
#   - Docker доступен в PATH
# =============================================================================

set -euo pipefail

# ---------- Настройки ---------------------------------------------------
SONAR_HOST="${SONAR_HOST:-http://host.docker.internal:9000}"
PROJECT_KEY="${PROJECT_KEY:-vulnerable-app}"
PROJECT_NAME="${PROJECT_NAME:-OTUS Vulnerable App (Учебный проект)}"
PROJECT_VERSION="${PROJECT_VERSION:-1.0-lesson15}"
SOURCES_DIR="backend,frontend"

# ---------- Получить токен ----------------------------------------------
if [[ -z "${SONAR_TOKEN:-}" ]]; then
  echo ""
  echo "🔑  Введите токен SonarQube (My Account → Security → Generate Token):"
  read -rs SONAR_TOKEN
  echo ""
fi

if [[ -z "$SONAR_TOKEN" ]]; then
  echo "❌  Токен не указан. Завершение." >&2
  exit 1
fi

# ---------- Запустить SonarScanner -------------------------------------
echo "🚀  Запускаю анализ проекта '$PROJECT_KEY' ..."
echo "    Сервер: $SONAR_HOST"
echo ""

docker run --rm \
  --network=host \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey="$PROJECT_KEY" \
  -Dsonar.projectName="$PROJECT_NAME" \
  -Dsonar.projectVersion="$PROJECT_VERSION" \
  -Dsonar.sources="$SOURCES_DIR" \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.exclusions="**/__pycache__/**,**/*.pyc" \
  -Dsonar.host.url="$SONAR_HOST" \
  -Dsonar.token="$SONAR_TOKEN"

echo ""
echo "✅  Анализ завершён. Открой результаты в Web UI:"
echo "    ${SONAR_HOST}/dashboard?id=${PROJECT_KEY}"
