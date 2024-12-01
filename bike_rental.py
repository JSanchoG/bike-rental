import json
import os
from datetime import datetime
import smtplib

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

    file_path = "data/rentals.json"
    
    # Check for file_path file, create as empty list if doesn't exist
    # NOTE: Doesn't work with an empty file, has to include an empty array, too lazy to fix zz
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

    with open(file_path, 'r') as file:
        rentals = json.load(file)

    rentals.append(rental)

    with open(file_path, 'w') as file:
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

def cancel_rental(customer_name):
    '''
    Usuwa wynajem
    '''

def send_rental_invoice_email(customer_email, rental_details):
    '''
    Wysyła e-mail z fakturą
    '''

def generate_daily_report():
    '''
    Generuje raport dzienny
    '''