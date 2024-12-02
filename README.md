# System Wynajmu Rowerów

Aplikacja bike_rental.py to system wynajmu rowerów, umożliwiający wynajmowanie rowerów, obliczanie kosztów, zapisywanie danych do plików JSON, generowanie raportów dziennych, anulowanie wynajmu oraz wysyłanie faktur e-mail.

---

## Wymagane biblioteki
> [!IMPORTANT]
> Aplikacja wymaga biblioteki `python-dotenv` do przekazywania danych logowania.
> ```bash
> pip install python-dotenv
> ```

Plik `.env` z danymi konfiguracyjnymi:
```env
EMAIL_SENDER=<your_google_mail>
EMAIL_PASSWORD=<hasło_aplikacji_google>
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

## Struktura plików
Katalogi `data/` oraz `data/daily_reports/` tworzą się od razu po wywołaniu programu, plik `data/rentals.json` tworzy się po wywołaniu funkcji `save_rental()`.
```
bike_rental/
├── bike_rental.py
├── data/
│   └── rentals.json
│   └── daily_reports/
└── .env
```

## Funkcje programu
1. `rent_bike()`: Dodaje wynajem roweru, używa funkcji `save_rental()` do zapisu.
```py
def rent_bike(customer_name, rental_duration)

rent_bike("Jan Kowalski", 2)
```

2. `calculate_cost()`: Oblicza koszt wynajmu, używane bezpośrednio w funkcjach wynajmowania. Zmienna `rental_duration` oznacza liczbę godzin.<br>Pierwsza godzina kosztuje 10 zł, każda następna to 5 zł.
```py
def calculate_cost(rental_duration)

calculate_cost(4)
```

3. `save_rental()`: Zapisuje dane wynajmu do pliku JSON. Wykonywane w funkcji `rent_bike()` do zapisu w pliku `data/rentals.json`, który można zmienić pod zmienną globalną `FILE_RENTALS_PATH`. Na wejściu funkcji powinien znaleźć się objekt słownikowy.
```py
def save_rental(rental)

rental_duration = 2
rentalObject = {
    "customer_name": "Jan Kowalski",
    "rental_duration": rental_duration,
    "cost": calculate_cost(rental_duration),
    "time": {
        "formatted": datetime.now().strftime("%d.%m.%Y"), # dd.mm.YYYY
        "unix": int(datetime.now().timestamp()) # UNIX Date
    }
}
save_rental(rentalObject)
```

4. `load_rentals()`: Wczytuje wynajmu z pliku JSON `data/rentals.json`, który można zmienić pod zmienną globalną `FILE_RENTALS_PATH`.
```py
def load_rentals()

print(load_rentals())
```

5. `cancel_rental()`: Usuwa wynajem w pliku JSON zdefiniowanym pod zmienną globalną `FILE_RENTALS_PATH`, domyślnie `data/rentals.json`. Usuwanie klienta odbywa się przez nazwę, jeśli klient nie istnieje - zostanie zwrócona wiadomość.
```py
def cancel_rental(customer_name)

cancel_rental("Jan Kowalski")
```

6. `send_rental_invoice_email()`: Wysyła e-mail z fakturą korzystając z serwisu Gmail, funkcja posiada walidację e-maila.
<br>Szablon faktury znajduje się w pliku HTML `assets/invoice.html` ze zmiennymi:
> `%top-text%` - Opcjonalny tekst nad datą
> <br>`%logo%` - URL do logo na fakturze (domyślnie 898x106px)
> <br>`%client_date%` - data wynajęcia roweru
> <br>`%client_due%` - termin płatności faktury, domyślnie 30 dni
> <br>`%client_name%` - nazwa klienta
> <br>`%client_email%` - e-mail klienta
> <br>`%client_time%` - czas trwania wynajmu
> <br>`%client_price%` - cena za usługę
> <br>`%client_price_total%` - całkowity koszt
```py
def send_rental_invoice_email(customer_email, rental_details)

obj = {
    "customer_name": "Testowy Klient",
    "rental_duration": 48,
    "cost": 245,
    "time": {
        "formatted": "02.12.2024",
        "unix": 1733094018
    }
}
send_rental_invoice_email("example@gmail.com", obj)
```
Przykładowa faktura:
![image](https://raw.githubusercontent.com/JSanchoG/bike-rental/refs/heads/main/assets/invoice-example.png)

7. `generate_daily_report()`: Generuje raport dzienny w katalogu `data/daily_reports/` o nazwie `daily_report_<data>.json` lub `daily_report_<data>_<licznik>.json` w zależności, czy w tym dniu został już utworzony raport. Data w formacie YYYY-mm-dd.<br>Funkcja przekopiowuje plik pod zmienną `FILE_RENTALS_PATH`, domyślnie `data/rentals.json` do raportu wraz z datą utworzenia raportu w formatach YYYY-mm-dd i UNIX.
```py
def generate_daily_report()

generate_daily_report()
generate_daily_report()
generate_daily_report()

# Wykonanie funkcji trzykrotnie (na dzień 2 grudnia 2024) utworzy 3 następujące pliki:
# daily_report_2024-12-02.json
# daily_report_2024-12-02_2.json
# daily_report_2024-12-02_3.json
```
Przykład raportu:
```json
{
    "time": {
        "formatted": "2024-12-02", <-- Data wygenerowania raportu
        "unix": 1733160513
    },
    "rentals": [] <-- zawartość pliku data/rentals.json
}
```