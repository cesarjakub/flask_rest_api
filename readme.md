# Název Vaší Aplikace

## Popis

Tato webová aplikace je napsaná v jazyce Python s využitím frameworku Flask. Poskytuje REST API pro správu blogových příspěvků. Aplikace obsahuje frontend, kde existuje předem vytvořený uživatel s rolí admin. Přihlášením se jako admin máte možnost aktualizovat a mazat příspěvky. Běžný uživatel může pouze vytvářet nové příspěvky.

## Web

Web běží na ubuntu serveru na portu 5000 [http://138.68.93.217:5000/](http://138.68.93.217:5000/)

## Instalace

1. Stáhněte repozitář do svého lokálního prostoru.
2. Nainstalujte potřebné závislosti pomocí příkazu `pip install -r requirements.txt`.
3. Vytvořte soubor `.env` a nastavte potřebné proměnné prostředí, například `TOKEN`, `DB_NAME`, `DB_HOST`, `DB_USER`.
4. Spusťte aplikaci pomocí příkazu `python app.py`.

## Použití po instalaci

1. Přejděte na hlavní stránku aplikace na adrese [http://localhost:5000/](http://localhost:5000/).
2. Pokud již máte účet, přihlaste se. V opačném případě se zaregistrujte.
3. Po přihlášení jako admin můžete upravovat a mazat existující příspěvky. Běžný uživatel může vytvářet nové příspěvky.

## API Routes

- **GET /api/blog/**
  - Získá všechny příspěvky z blogu.

- **GET /api/blog/{id}**
  - Získá konkrétní příspěvek na základě ID.

- **POST /api/blog/**
  - Vložení příspěvku do databáze

- **DELETE /api/blog/{id}**
  - Smaže příspěvek na základě ID.

- **PATCH /api/blog/{id}**
  - Aktualizuje příspěvek na základě ID.

## HTML Routes

- **GET /**
  - Hlavní stránka s výpisem všech příspěvků.

- **POST /**
  - Přidá nový příspěvek (přihlášený uživatel).

- **GET /login**
  - Stránka pro přihlášení.

- **POST /login**
  - Přihlásí uživatele.

- **GET /admin**
  - Stránka s administrátorským rozhraním (pouze pro admina).

- **POST /admin**
  - Provádí akce v administrátorském rozhraní (mazání, aktualizace).

- **GET /register**
  - Stránka pro registraci nového uživatele.

- **POST /register**
  - Zpracování registrace nového uživatele.

- **GET /logout**
  - Odhlásí uživatele.

## Chybové kódy

- **404 Not Found**
  - Stránka nenalezena.

## Autor

Jakub César 
