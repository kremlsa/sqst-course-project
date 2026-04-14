"""
vulnerable-app/app.py — Учебное веб-приложение с намеренными уязвимостями
==========================================================================
Курс OTUS DevSecOps: SonarQube от А до Я (Урок 1)
Демонстрация типичных проблем безопасности в веб-приложении

ВНИМАНИЕ: Этот код содержит НАМЕРЕННЫЕ уязвимости для учебных целей.
НЕ используйте этот код в production-окружении!

Уязвимости в этом файле делятся на две категории:

1) Детектируемые SonarQube Community Edition:
   — Hard-coded credentials (CWE-798) → S2068, S6418 → VULNERABILITY
   — Binding 0.0.0.0 (S8392) → VULNERABILITY
   — Weak cryptography MD5/SHA1 (CWE-328) → S4790 → SECURITY HOTSPOT
   — Insecure random (CWE-330) → S2245 → SECURITY HOTSPOT
   — Debug mode (CWE-489) → S4507 → SECURITY HOTSPOT
   — CORS * (CWE-942) → S5122 → SECURITY HOTSPOT
   — Hardcoded IPs (S1313) → SECURITY HOTSPOT
   — SQL formatting / f-string в запросах (S2077) → SECURITY HOTSPOT

2) НЕ детектируемые CE (требуется Enterprise Edition с taint analysis):
   — SQL Injection (CWE-89) → S3649 (Enterprise)
   — Command Injection (CWE-78) → S2076 (Enterprise)
   — Path Traversal (CWE-22) → S2083 (Enterprise)

   CE не может отследить поток данных от пользовательского ввода до опасной
   операции (taint analysis). Поэтому эти уязвимости оставлены в коде для
   ручного анализа и объяснения ограничений CE на занятии.
"""

import os
import sqlite3
import subprocess
import hashlib
import random
import string
from flask import Flask, request, jsonify

app = Flask(__name__)

# =============================================================================
# УЯЗВИМОСТЬ 1: Hard-coded credentials (CWE-798)
# SonarQube CE детектирует через правила S2068 и S6418
# Тип: VULNERABILITY, Серьёзность: BLOCKER / MAJOR
#
# ЧТО НАХОДИТ CE: строки с "password", "secret", "token" в присвоении
# ПОЧЕМУ ОПАСНО: секреты в коде попадают в git-историю и доступны всем
# =============================================================================
DB_PASSWORD = "admin123"                          # S2068: пароль в коде
SECRET_KEY = "mysecretkey12345"                   # S6418: секретный ключ
API_TOKEN = "tok_prod_abc123xyz789def456"         # S6418: API-токен
DATABASE_URL = "postgresql://admin:P@ssw0rd@db:5432/prod"  # S6418: креды в URL
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # S6418

# =============================================================================
# УЯЗВИМОСТЬ 2: Hardcoded IP addresses (CWE-200)
# SonarQube CE: S1313 — "Using hardcoded IP addresses is security-sensitive"
# Тип: SECURITY HOTSPOT
#
# ЧТО НАХОДИТ CE: любые строковые литералы в формате IPv4/IPv6
# ПОЧЕМУ ОПАСНО: раскрытие внутренней инфраструктуры, сложность при миграции
# =============================================================================
ALLOWED_HOST = "192.168.1.100"                    # S1313: захардкоженный IP
BACKUP_SERVER = "10.0.0.55"                       # S1313: захардкоженный IP


def get_db_connection():
    """Создаёт подключение к SQLite базе данных."""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализирует базу данных с тестовыми данными."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)
    conn.execute("INSERT OR IGNORE INTO users VALUES (1,'admin','admin123','admin')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2,'alice','pass456','user')")
    conn.commit()
    conn.close()


# =============================================================================
# УЯЗВИМОСТЬ 3: SQL Injection (CWE-89)
# SonarQube CE: S2077 — "Formatting SQL queries is security-sensitive"
#   → Тип: SECURITY HOTSPOT (CE видит паттерн, но не данные)
# SonarQube Enterprise: S3649 — полный taint analysis
#   → Тип: VULNERABILITY (Enterprise отслеживает данные от input до SQL)
#
# РАЗНИЦА CE vs Enterprise:
#   CE видит: «тут f-string в SQL — проверьте вручную»
#   Enterprise видит: «данные из request.form попадают в SQL без санитизации»
# =============================================================================
@app.route("/login", methods=["POST"])
def login():
    """
    Небезопасная аутентификация — уязвима к SQL Injection.

    Пример атаки: username = "admin' --"
    Запрос становится: SELECT * FROM users WHERE username='admin' --' AND ...
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db_connection()
    # УЯЗВИМОСТЬ: f-string конкатенация в SQL-запросе
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()  # SQL INJECTION!
    conn.close()

    if user:
        return jsonify({"status": "ok", "role": user["role"]})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route("/search", methods=["GET"])
def search_users():
    """Ещё один пример SQL-форматирования для наглядности."""
    term = request.args.get("q", "")
    conn = get_db_connection()
    # УЯЗВИМОСТЬ: конкатенация строк в SQL
    sql = "SELECT * FROM users WHERE username LIKE '%" + term + "%'"
    results = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(r) for r in results])


# =============================================================================
# УЯЗВИМОСТЬ 4: Command Injection (CWE-78)
# SonarQube CE: S4721 существует, но НЕ активирован в Sonar way по умолчанию
# SonarQube Enterprise: S2076 — taint analysis (не существует в CE)
#
# ДЕМО НА ЗАНЯТИИ: показать, что CE по умолчанию не ловит, но правило
# можно активировать вручную → это тема Урока 5 (кастомизация профилей)
# =============================================================================
@app.route("/ping", methods=["GET"])
def ping():
    """
    Небезопасный пинг — уязвим к Command Injection.

    Пример атаки: host = "8.8.8.8; cat /etc/passwd"
    """
    host = request.args.get("host", "localhost")
    # УЯЗВИМОСТЬ: shell=True + пользовательский ввод
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()


# =============================================================================
# УЯЗВИМОСТЬ 5: Path Traversal (CWE-22)
# SonarQube CE: НЕ детектирует (нет taint analysis)
# SonarQube Enterprise: S2083
#
# Оставлен для ручного анализа студентами и демонстрации ограничений CE
# =============================================================================
@app.route("/file", methods=["GET"])
def read_file():
    """
    Небезопасное чтение файлов — уязвимо к Path Traversal.

    Пример атаки: filename = "../../etc/passwd"
    """
    filename = request.args.get("filename", "readme.txt")
    base_dir = "/var/app/files"
    filepath = os.path.join(base_dir, filename)
    try:
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


# =============================================================================
# УЯЗВИМОСТЬ 6: Weak Cryptography (CWE-326 / CWE-328)
# SonarQube CE: S4790 — "Using weak hashing algorithms is security-sensitive"
# Тип: SECURITY HOTSPOT
#
# CE детектирует: hashlib.md5(), hashlib.sha1() — независимо от контекста
# =============================================================================
def hash_password(password: str) -> str:
    """
    Небезопасное хеширование — MD5 без соли.
    MD5 считается криптографически слабым с 1996 года.
    """
    return hashlib.md5(password.encode()).hexdigest()  # S4790: MD5


def hash_token(token: str) -> str:
    """SHA1 тоже считается криптографически слабым."""
    return hashlib.sha1(token.encode()).hexdigest()    # S4790: SHA1


# =============================================================================
# УЯЗВИМОСТЬ 7: Insecure Randomness (CWE-330)
# SonarQube CE: S2245 — "Using pseudorandom number generators (PRNGs)"
# Тип: SECURITY HOTSPOT
#
# CE детектирует: random.choice(), random.randint() и др. из модуля random
# ПОЧЕМУ ОПАСНО: random — предсказуемый ГПСЧ, не годится для криптографии
# =============================================================================
def generate_session_token() -> str:
    """Небезопасная генерация токенов — random вместо secrets."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(32))  # S2245


def generate_reset_code() -> str:
    """Небезопасный OTP — предсказуемый random."""
    return str(random.randint(100000, 999999))  # S2245


# =============================================================================
# УЯЗВИМОСТЬ 8: CORS Misconfiguration (CWE-942)
# SonarQube CE: S5122 — "Having a permissive CORS policy"
# Тип: SECURITY HOTSPOT
#
# CE детектирует: заголовок Access-Control-Allow-Origin: *
# ПОЧЕМУ ОПАСНО: любой домен может делать запросы к API → CSRF, утечка данных
# =============================================================================
@app.after_request
def add_cors_headers(response):
    """Небезопасная CORS-конфигурация — разрешает все домены."""
    response.headers["Access-Control-Allow-Origin"] = "*"              # S5122
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


# =============================================================================
# УЯЗВИМОСТЬ 9: Information Exposure через debug-эндпоинт (CWE-200)
# SonarQube CE: связано с S4507 (debug=True) — утечка секретов через открытый эндпоинт
# =============================================================================
@app.route("/debug", methods=["GET"])
def debug_info():
    """Утечка конфиденциальной информации через debug-эндпоинт."""
    return jsonify({
        "db_password": DB_PASSWORD,
        "secret_key": SECRET_KEY,
        "api_token": API_TOKEN,
        "env": dict(os.environ),
        "python_path": os.sys.path,
    })


# =============================================================================
# БЕЗОПАСНЫЕ АНАЛОГИ (для сравнения на занятии)
# =============================================================================
import secrets


def hash_password_secure(password: str) -> str:
    """
    БЕЗОПАСНЫЙ вариант: SHA-256 с солью.
    В реальном проекте используйте bcrypt или argon2.
    """
    salt = secrets.token_hex(16)
    return hashlib.sha256((salt + password).encode()).hexdigest() + ":" + salt


def generate_token_secure() -> str:
    """БЕЗОПАСНЫЙ вариант: secrets вместо random."""
    return secrets.token_urlsafe(32)


# Безопасный SQL: параметризованные запросы
# cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))

# Безопасный subprocess: без shell=True, список аргументов
# subprocess.run(["ping", "-c", "1", host], capture_output=True)


# =============================================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# =============================================================================
if __name__ == "__main__":
    init_db()
    # S4507: debug=True в production — раскрывает трассировки ошибок
    # S8392: host="0.0.0.0" — слушает на всех интерфейсах
    app.run(host="0.0.0.0", port=5000, debug=True)  # S8392 + S4507
