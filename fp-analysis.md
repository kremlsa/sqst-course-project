# FP/FN Analysis — Решения по замечаниям SonarQube

Проект: `vulnerable-app` | Версия: `1.0`

---

## Задокументированные решения

### 1. MD5 в hash_password_secure() — Won't Fix

| Поле | Значение |
|------|----------|
| Правило | `python:S4790` / Security Hotspot |
| Файл | `vulnerable-app/app.py` |
| Решение | **Won't Fix** |
| Обоснование | Учебный пример "безопасного" варианта для сравнения. В production не используется. |
| Дата | 2026-01 |

### 2. Hard-coded credentials в init_db() — Won't Fix

| Поле | Значение |
|------|----------|
| Правило | `python:S2068` |
| Файл | `vulnerable-app/app.py` |
| Решение | **Won't Fix** |
| Обоснование | Тестовые данные намеренны для демонстрации CWE-798. Только учебное окружение. |
| Дата | 2026-01 |

### 3. Command Injection в /ping — Confirmed

| Поле | Значение |
|------|----------|
| Правило | `python:S4721` |
| Файл | `vulnerable-app/app.py` |
| Решение | **Confirmed (intentional)** |
| Обоснование | Намеренная уязвимость CWE-78 для демонстрации. Backlog: заменить subprocess на icmplib. |
| Дата | 2026-01 |

---

## Правило использования NOSONAR

**Хорошо:**
```python
result = dangerous_fn()  # NOSONAR: учебный пример CWE-78, не попадает в production
```

**Плохо:**
```python
result = dangerous_fn()  # NOSONAR
```

**Запрещено**: NOSONAR без обоснования.
