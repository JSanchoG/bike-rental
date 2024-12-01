import json
import os
from datetime import datetime
import smtplib

FILE_RENTALS_PATH = "data/rentals.json"
CURRENCY = "PLN"

def calculate_cost(rental_duration:int):
    '''
    Oblicza koszt wynajmu
    '''
    if rental_duration <= 0: return 0
    elif rental_duration <= 1: return 10
    else: return 10 + (rental_duration - 1) * 5

def save_rental(rental:dict):
    '''
    Zapisuje dane wynajmu do pliku JSON
    '''
    # Check for {FILE_RENTALS_PATH} file, create as empty list if doesn't exist
    # NOTE: Doesn't work with an empty file, has to include an empty array, too lazy to fix zz
    if not os.path.exists(FILE_RENTALS_PATH):
        with open(FILE_RENTALS_PATH, 'w') as file:
            json.dump([], file)

    with open(FILE_RENTALS_PATH, 'r') as file:
        rentals = json.load(file)

    rentals.append(rental)

    with open(FILE_RENTALS_PATH, 'w') as file:
        json.dump(rentals, file, indent=4)

def rent_bike(customer_name:str, rental_duration:int):
    '''
    Dodaje wynajem roweru
    '''
    rentalObject = {
        "customer_name": customer_name,
        "rental_duration": rental_duration,
        "cost": calculate_cost(rental_duration),
        "time": {
            "formatted": datetime.now().strftime("%d.%m.%Y"), # dd.mm.YYYY
            "unix": int(datetime.now().timestamp()) # UNIX Date
        }
    }
    save_rental(rentalObject)

def load_rentals():
    '''
    Wczytuje wynajmu z pliku JSON
    '''
    if os.path.exists(FILE_RENTALS_PATH):
        with open(FILE_RENTALS_PATH, 'r') as file:
            rentals = json.load(file)
            print()
            for rental in rentals:
                # print(rental)
                print(f"Customer: {rental['customer_name']}")
                print(f"Wynajem na {rental['rental_duration']} godz.")
                print(f"Koszt: {rental['cost']} {CURRENCY}")
                print(f"Data wynajmu: {rental['time']['formatted']}")
                print()
    else:
        print("Brak zapisanych wynajmów.")

def cancel_rental(customer_name:str):
    '''
    Usuwa wynajem
    '''
    if os.path.exists(FILE_RENTALS_PATH):
        with open(FILE_RENTALS_PATH, 'r') as file:
            rentals = json.load(file)
        
        rentals = [rental for rental in rentals if rental['customer_name'] != customer_name]

        with open(FILE_RENTALS_PATH, 'w') as file:
            json.dump(rentals, file, indent=4)
        print(f"Wynajem dla {customer_name} został anulowany.")
    else:
        print("Brak zapisanych wynajmów.")

def send_rental_invoice_email(customer_email, rental_details):
    '''
    Wysyła e-mail z fakturą
    '''

def generate_daily_report():
    '''
    Generuje raport dzienny
    '''