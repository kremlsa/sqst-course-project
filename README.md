# Урок 7: Security Hotspots и митигация уязвимостей

## Что добавлено в этом уроке

| Файл | Описание |
|------|---------|
| `hotspot-review.md` | Документ с рекомендациями по анализу Security Hotspots |

## Структура проекта

```
github_project/
├── docker-compose.yml
├── Jenkinsfile
├── fp-analysis.md
├── hotspot-review.md
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
| 6 | False Positive / False Negative: системный подход | fp-analysis.md |
| 7 | Security Hotspots и митигация уязвимостей | hotspot-review.md |

## Требования

- **Docker** и Docker Compose
- **Оперативная память**: минимум 4GB, рекомендуется 8GB
- **Свободное место на диске**: минимум 5GB
- **Порт 9000** должен быть свободен для SonarQube

## Описание компонентов

### hotspot-review.md
Руководство по анализу Security Hotspots в SonarQube - участков кода, где разработчик должен вручную определить, является ли код уязвимым. Включает стратегии рецензирования, методы митигации и примеры исправления уязвимостей.
