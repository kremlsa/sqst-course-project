# Access Policy — Политика управления доступом SonarQube

Версия: `1.0-lesson12`

---

## Ролевая модель

| Роль | Права | Кому выдаётся |
|------|-------|---------------|
| `Global Admin` | Управление всем сервером | Только DevSecOps-инженеры |
| `Quality Gate Admin` | Управление Quality Gates | Тимлиды, DevSecOps |
| `Project Admin` | Управление проектом | Тимлид проекта |
| `Developer` | Просмотр + закрытие замечаний | Разработчики |
| `Viewer` | Только просмотр отчётов | QA, Product |
| `CI/CD Scanner` | Только запуск анализа | Service Account для CI/CD |

---

## Токены доступа

| Тип | Область | Срок действия | Где хранится |
|-----|---------|---------------|--------------|
| `User Token` | Конкретный пользователь | 90 дней | Личный кабинет |
| `Project Analysis Token` | Один проект | 180 дней | CI/CD переменные (masked) |
| `Global Analysis Token` | Все проекты | 365 дней | Только DevSecOps |

**Правило**: в `.gitlab-ci.yml` и `Jenkinsfile` использовать ТОЛЬКО `Project Analysis Token`.

---

## LDAP / SSO интеграция

```yaml
# sonar.properties (фрагмент настройки LDAP)
sonar.security.realm=LDAP
ldap.url=ldaps://ldap.company.com:636
ldap.bindDn=cn=sonarqube,ou=service,dc=company,dc=com
ldap.user.baseDn=ou=users,dc=company,dc=com
ldap.group.baseDn=ou=groups,dc=company,dc=com
```

---

## Чеклист Security Hardening

- [x] Изменён пароль `admin` по умолчанию
- [x] Гостевой доступ (`sonar.forceAuthentication=true`) отключён
- [x] CI/CD использует Project Analysis Token (не User Token)
- [x] Токены имеют срок действия (не `No expiration`)
- [x] HTTPS включён (Let's Encrypt или внутренний CA)
- [ ] LDAP/SSO интегрирован (планируется в следующем спринте)
- [ ] Аудит-лог настроен и отправляется в SIEM
