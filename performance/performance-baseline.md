# Performance Baseline — Урок 13

## Методология стресс-тестирования

Тест: анализ проекта `vulnerable-app` при различных нагрузках

```bash
# Запустить 5 параллельных анализов
for i in {1..5}; do
    SONAR_TOKEN=$TOKEN ./scan.sh &
done
wait
```

## Результаты (учебный стенд: 4 CPU, 8GB RAM)

| Конфигурация | Время анализа | CPU peak | Memory peak |
|-------------|--------------|----------|-------------|
| Default JVM (512m) | 45 сек | 85% | 2.1 GB |
| Optimized JVM (2g) | 28 сек | 70% | 3.8 GB |
| 5 параллельных (default) | 3 мин (очередь) | 100% | ОМО |
| 5 параллельных (optimized) | 2 мин 10 сек | 90% | 6.2 GB |

## Рекомендации

- Для команды до 20 чел: Community Edition на 8GB RAM достаточно
- Для команды 20–100 чел: Developer Edition + 16GB RAM + NVMe SSD
- Для 100+ чел: Enterprise Edition с кластером или SonarCloud
