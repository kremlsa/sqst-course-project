# Урок 5: Кастомизация Quality Gate, правил и работа с замечаниями

## Что добавлено в этом уроке

| Файл | Описание |
|------|---------|
| `quality-gate.json` | Конфигурация Quality Gate с критериями прохождения |
| `setup-quality-gate.sh` | Скрипт для установки Quality Gate в SonarQube |

## Структура проекта

```
github_project/
├── docker-compose.yml
├── Jenkinsfile
├── quality-gate.json
├── setup-check.sh
├── setup-quality-gate.sh
├── scan.sh
├── sonar-project.properties
└── vulnerable-app/
    ├── app.py
    └── utils.py
```

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd github_project
   ```

2. Проверьте предварительные требования:
   ```bash
   bash setup-check.sh
   ```

3. Запустите SonarQube:
   ```bash
   docker compose up -d
   ```

4. Откройте SonarQube в браузере:
   ```
   http://localhost:9000
   ```

5. Установите Quality Gate:
   ```bash
   bash setup-quality-gate.sh
   ```

6. Выполните сканирование проекта:
   ```bash
   bash scan.sh
   ```

## Эволюция проекта

| Урок | Название | Новые файлы |
|------|----------|------------|
| 1 | Введение в SonarQube и его роль в безопасности | docker-compose.yml, setup-check.sh, sonar-project.properties, vulnerable-app/app.py |
| 2 | Быстрый старт: установка SonarQube и локальное сканирование | scan.sh, vulnerable-app/utils.py |
| 3 | Основы SAST, OWASP Top 10 и Secure SDLC | (без новых файлов) |
| 4 | Интеграция SonarQube с CI/CD (GitLab, Jenkins) | Jenkinsfile |
| 5 | Кастомизация Quality Gate, правил и работа с замечаниями | quality-gate.json, setup-quality-gate.sh |

## Требования

- **Docker** и Docker Compose
- **Оперативная память**: минимум 4GB, рекомендуется 8GB
- **Свободное место на диске**: минимум 5GB
- **Порт 9000** должен быть свободен для SonarQube

## Описание компонентов

### quality-gate.json
Конфигурация Quality Gate с условиями, определяющими когда проект считается прошедшим проверку безопасности. Включает пороги для критичности, покрытия кода и других метрик.

### setup-quality-gate.sh
Скрипт для автоматической загрузки и применения Quality Gate конфигурации к проекту в SonarQube.
