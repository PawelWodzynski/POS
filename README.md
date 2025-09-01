# 🛒 Symulacja Systemu POS


[![Demo POS](https://img.youtube.com/vi/9xaptPJ-xBw/0.jpg)](https://www.youtube.com/watch?v=9xaptPJ-xBw)


Ten projekt jest **symulacją systemu Point of Sale (POS)**.  
Zawiera backend i frontend napisane w **Pythonie** oraz **HTML/JavaScript**, a dane przechowywane są w **PostgreSQL**.  
Całość uruchamiana jest w kontenerach za pomocą **Docker Compose**.

---

## ✨ Funkcjonalności

- ✅ Backend (Python/Flask) i frontend (HTML/JS).  
- ✅ Baza danych **PostgreSQL** z inicjalnym schematem (`db/schema.sql`).  
- ✅ Integracja z **FakeStore API** jako źródłem danych o produktach i kategoriach.  
- ✅ Możliwość:  
  - sprzedaży produktów z FakeStore API,  
  - filtrowania produktów wg kategorii lub nazwy,  
  - dodawania własnych produktów,  
  - aktualizacji stanów magazynowych poprzez dostawy.  
- ✅ Panel logowania (dane testowe):  
Login: admin
Hasło: admin
- ✅ Operacje wykonywane są na danych w **localStorage** zarządzanym przez JavaScript po otrzymywaniu odpowiedzi z symulowanych endpointów.  

---

## 🚀 Uruchomienie projektu

### Wymagania wstępne
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)

### Kroki

1. Sklonuj repozytorium:  
 ```bash
 git clone https://github.com/PawelWodzynski/POS.git
 cd POS
Uruchom kontenery:
docker-compose up
Otwórz aplikację w przeglądarce:
👉 http://localhost:51953
📂 Struktura projektu
POS/
├── app.py              # Główny punkt wejścia aplikacji
├── controllers/        # Kontrolery backendu (endpointy API)
├── models/             # Modele bazy danych
├── repositories/       # Warstwa dostępu do danych
├── services/           # Logika biznesowa
├── static/js/          # Skrypty frontendowe (UI + localStorage)
├── templates/          # Szablony HTML
├── db/
│   └── schema.sql      # Schemat bazy danych PostgreSQL
├── docker-compose.yml  # Konfiguracja Docker Compose
└── Dockerfile          # Instrukcje budowy obrazu
📜 Licencja
Projekt jest udostępniony na licencji MIT.