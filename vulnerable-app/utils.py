"""
vulnerable-app/utils.py — Утилиты с дополнительными уязвимостями
================================================================
Курс OTUS DevSecOps: SonarQube от А до Я (Урок 1)

Дополнительные уязвимости, детектируемые SonarQube Community Edition:
  — XXE: xml.etree без защиты (S2755 → VULNERABILITY в CE!)
  — File permissions: chmod 0o777 (S2612 → VULNERABILITY в CE!)
  — Weak crypto: доп. примеры MD5/SHA1 (S4790 → HOTSPOT)
  — Insecure temp files: /tmp usage (S5443 → HOTSPOT)
  — Hard-coded credentials: доп. примеры (S2068/S6418 → VULNERABILITY)
  — Insecure random: доп. примеры (S2245 → HOTSPOT)

  НЕ детектируемые CE (для ручного анализа):
  — Insecure deserialization: pickle.loads (S5135 — Enterprise only)
  — SSRF: urllib без валидации (Enterprise only)
"""

import os
import pickle
import hashlib
import random
import urllib.request
from xml.etree import ElementTree


# =============================================================================
# XML External Entity — XXE (CWE-611)
# SonarQube CE: S2755 — "XML parsers should not be vulnerable to XXE attacks"
# Тип: VULNERABILITY (BLOCKER!)
# =============================================================================
def parse_config(xml_string: str) -> dict:
    """
    НЕБЕЗОПАСНО: парсинг XML без защиты от XXE.
    БЕЗОПАСНО: использовать defusedxml.ElementTree
    """
    root = ElementTree.fromstring(xml_string)  # S2755: XXE
    config = {}
    for child in root:
        config[child.tag] = child.text
    return config


# =============================================================================
# Insecure File Permissions (CWE-732)
# SonarQube CE: S2612 — "File permissions should not be world-accessible"
# Тип: VULNERABILITY (MAJOR)
# =============================================================================
def save_config(config_data: str, path: str):
    """НЕБЕЗОПАСНО: 0o777 = все могут читать, писать и выполнять."""
    with open(path, "w") as f:
        f.write(config_data)
    os.chmod(path, 0o777)  # S2612: world-accessible


# =============================================================================
# Weak Cryptography — дополнительные примеры (CWE-328)
# SonarQube CE: S4790 — SECURITY HOTSPOT
# =============================================================================
def verify_integrity(data: bytes, expected_hash: str) -> bool:
    """НЕБЕЗОПАСНО: MD5 для проверки целостности данных."""
    computed = hashlib.md5(data).hexdigest()  # S4790
    return computed == expected_hash


def compute_checksum(filepath: str) -> str:
    """НЕБЕЗОПАСНО: SHA1 для контрольной суммы файла."""
    sha1 = hashlib.sha1()  # S4790
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha1.update(chunk)
    return sha1.hexdigest()


# =============================================================================
# Insecure Temporary Files (CWE-377)
# SonarQube CE: S5443 — "Using publicly writable directories"
# Тип: SECURITY HOTSPOT
# =============================================================================
def create_temp_report(content: str) -> str:
    """НЕБЕЗОПАСНО: предсказуемое имя файла в /tmp."""
    filepath = "/tmp/report_" + str(random.randint(1000, 9999)) + ".txt"  # S5443
    with open(filepath, "w") as f:
        f.write(content)
    return filepath


def write_log(message: str):
    """НЕБЕЗОПАСНО: запись логов в общедоступную директорию."""
    with open("/tmp/app.log", "a") as f:  # S5443
        f.write(message + "\n")


# =============================================================================
# Hard-coded credentials — дополнительные примеры (CWE-798)
# SonarQube CE: S2068, S6418 — VULNERABILITY
# =============================================================================
SMTP_PASSWORD = "email_pass_123"          # S2068: пароль SMTP
REDIS_AUTH = "redis_secret_token"         # S6418: пароль Redis
ENCRYPTION_KEY = "AES256_KEY_DO_NOT_SHARE_a1b2c3d4e5f6"  # S6418: ключ


def send_notification(recipient: str, message: str):
    """Имитация отправки уведомления с захардкоженными кредами."""
    smtp_config = {
        "host": "smtp.company.com",
        "port": 587,
        "username": "alerts@company.com",
        "password": SMTP_PASSWORD,
    }
    return {"sent_to": recipient, "config": smtp_config}


# =============================================================================
# Insecure Random — дополнительные примеры (CWE-330)
# SonarQube CE: S2245 — SECURITY HOTSPOT
# =============================================================================
def generate_api_key() -> str:
    """НЕБЕЗОПАСНО: random для генерации API-ключей."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "ak_" + "".join(random.choice(chars) for _ in range(40))  # S2245


def generate_otp() -> str:
    """НЕБЕЗОПАСНО: random для одноразовых паролей."""
    return str(random.randint(100000, 999999))  # S2245


# =============================================================================
# Insecure Deserialization (CWE-502) — pickle.loads
# CE НЕ детектирует (S5135 требует Enterprise taint analysis)
# Оставлен для ручного анализа и сравнения с Semgrep/Bandit
# =============================================================================
def load_user_session(data: bytes) -> dict:
    """НЕБЕЗОПАСНО: pickle может выполнять произвольный код."""
    return pickle.loads(data)


# =============================================================================
# SSRF Potential (CWE-918)
# CE НЕ детектирует (нет taint analysis для urllib)
# Оставлен для ручного анализа
# =============================================================================
def fetch_url(url: str) -> str:
    """НЕБЕЗОПАСНО: запрос по произвольному URL без валидации."""
    response = urllib.request.urlopen(url)
    return response.read().decode()
