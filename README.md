# Урок 1: Введение в SonarQube и его роль в безопасности

## Что добавлено в этом уроке

| Файл | Описание |
|------|---------|
| `docker-compose.yml` | Docker Compose конфигурация для запуска SonarQube |
| `setup-check.sh` | Скрипт проверки предварительных требований |
| `sonar-project.properties` | Конфигурация проекта для SonarQube |
| `vulnerable-app/app.py` | Основной Python файл уязвимого приложения |

## Структура проекта

```
github_project/
├── docker-compose.yml
├── setup-check.sh
├── sonar-project.properties
└── vulnerable-app/
    └── app.py
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

## Эволюция проекта

| Урок | Название | Новые файлы |
|------|----------|------------|
| 1 | Введение в SonarQube и его роль в безопасности | docker-compose.yml, setup-check.sh, sonar-project.properties, vulnerable-app/app.py |

## Требования

- **Docker** и Docker Compose
- **Оперативная память**: минимум 4GB, рекомендуется 8GB
- **Свободное место на диске**: минимум 5GB
- **Порт 9000** должен быть свободен для SonarQube

## Описание компонентов

### docker-compose.yml
Конфигурация для запуска SonarQube сервера с PostgreSQL базой данных.

### setup-check.sh
Скрипт проверяет наличие Docker, доступность портов и требуемые ресурсы.

### sonar-project.properties
Параметры проекта для сканирования, включая язык, исключения и прочие настройки.

### vulnerable-app/app.py
Простое Python приложение с намеренными уязвимостями для демонстрации возможностей SonarQube.
