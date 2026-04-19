// frontend/app.js — Учебный frontend-модуль с намеренными уязвимостями
// Урок 8: Мультиязычный анализ в SonarQube

/**
 * УЯЗВИМОСТЬ: XSS через innerHTML (CWE-79)
 * SonarQube: "Sanitize this user input before using it in an HTML context"
 */
function renderUserProfile(username) {
    const container = document.getElementById("profile");
    // УЯЗВИМОСТЬ: прямая вставка пользовательского ввода (XSS)
    container.innerHTML = "<h1>Hello, " + username + "!</h1>"; // NOSONAR: учебный пример XSS (CWE-79)
}

/**
 * УЯЗВИМОСТЬ: eval() (CWE-95)
 * SonarQube: "Code should not be dynamically injected and executed"
 */
function calculateExpression(expr) {
    // УЯЗВИМОСТЬ: eval с пользовательскими данными
    return eval(expr); // WEAK: Code Injection через eval
}

/**
 * БЕЗОПАСНЫЙ вариант для сравнения
 */
function renderUserProfileSafe(username) {
    const container = document.getElementById("profile");
    const el = document.createElement("h1");
    el.textContent = "Hello, " + username + "!"; // Безопасно: textContent экранирует HTML
    container.appendChild(el);
}
