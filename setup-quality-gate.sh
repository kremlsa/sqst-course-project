#!/usr/bin/env bash
# Создание кастомного Quality Gate через SonarQube API
# Использование: SONAR_TOKEN=<token> bash setup-quality-gate.sh

set -euo pipefail

HOST="${SONAR_HOST:-http://localhost:9000}"
TOKEN="${SONAR_TOKEN}"
GATE_NAME="OTUS Strict Gate"

echo "Создаём Quality Gate: ${GATE_NAME}"

GATE_ID=$(curl -s -u "${TOKEN}:" \
  -X POST "${HOST}/api/qualitygates/create" \
  -d "name=${GATE_NAME}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

curl -s -u "${TOKEN}:" -X POST "${HOST}/api/qualitygates/create_condition" \
  -d "gateId=${GATE_ID}&metric=vulnerabilities&op=GT&error=0" > /dev/null

curl -s -u "${TOKEN}:" -X POST "${HOST}/api/qualitygates/create_condition" \
  -d "gateId=${GATE_ID}&metric=bugs&op=GT&error=2" > /dev/null

curl -s -u "${TOKEN}:" -X POST "${HOST}/api/qualitygates/create_condition" \
  -d "gateId=${GATE_ID}&metric=new_vulnerabilities&op=GT&error=0" > /dev/null

curl -s -u "${TOKEN}:" -X POST "${HOST}/api/qualitygates/create_condition" \
  -d "gateId=${GATE_ID}&metric=new_bugs&op=GT&error=0" > /dev/null

curl -s -u "${TOKEN}:" -X POST "${HOST}/api/qualitygates/select" \
  -d "gateId=${GATE_ID}&projectKey=vulnerable-app" > /dev/null

echo "Quality Gate ${GATE_NAME} создан. Открой: ${HOST}/quality_gates/show/${GATE_ID}"
