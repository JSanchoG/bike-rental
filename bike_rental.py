import json
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

FILE_RENTALS_PATH = "data/rentals.json"
CURRENCY = "PLN"
FILE_INVOICE_TEMPLATE_PATH = "assets/invoice.html"

load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

if not os.path.exists("data"):
    os.makedirs("data")

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

def generate_daily_report():
    '''
    Generuje raport dzienny
    '''
    today = datetime.now().strftime("%Y-%m-%d") # YYYY-mm-dd
    today_unix = int(datetime.now().timestamp())
    file_name = f"daily_report_{today}.json"
    file_path = f"data/{file_name}"

    if os.path.exists(file_path):
        counter = 1
        while os.path.exists(file_path):
            file_path = f"data/daily_report_{today}_{counter}.json"
            counter += 1

        file_path = f"data/daily_report_{today}_{counter}.json"
    
    rentals_file = FILE_RENTALS_PATH

    if os.path.exists(rentals_file):
        with open(rentals_file, 'r') as file:
            rentals = json.load(file)
    else:
        print(f"Brak danych wynajmów w {FILE_RENTALS_PATH}")
        rentals = []
    
    daily_report = {
        "time": {
            "formatted": today, # YYYY-mm-dd
            "unix": today_unix # UNIX Date
        },
        "rentals": rentals
    }
    
    with open(file_path, 'w') as file:
        json.dump(daily_report, file, indent=4)

    print(f"Raport dzienny zapisany jako {file_path}")

def send_rental_invoice_email(customer_email:str, rental_details:dict):
    '''
    Wysyła e-mail z fakturą
    '''
    # def load_html_template(file_path):
    #     with open(file_path, 'r', encoding='utf-8') as f:
    #         return f.read()
    # html_template = load_html_template(FILE_INVOICE_TEMPLATE_PATH)
    with open(FILE_INVOICE_TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        html_template = file.read()

    html_content = html_template.replace("%top-text%", "")
    # html_content = html_template.replace("%top-text%", "Faktura #69<br />")
    html_content = html_content.replace("%logo%", 'https://raw.githubusercontent.com/JSanchoG/bike-rental/refs/heads/main/assets/logo.png')
    html_content = html_content.replace("%client_date%", rental_details['time']['formatted'])
    unix_timestamp = rental_details['time']['unix']
    dt_object = datetime.utcfromtimestamp(unix_timestamp)
    new_dt_object = dt_object.replace(day=dt_object.day + 30)
    dueDate = new_dt_object.strftime('%d-%m-%Y')
    html_content = html_content.replace("%client_due%", dueDate)
    html_content = html_content.replace("%client_name%", rental_details['customer_name'])
    html_content = html_content.replace("%client_email%", customer_email)
    html_content = html_content.replace("%client_time%", f"{str(rental_details['rental_duration'])} godz.")
    html_content = html_content.replace("%client_price%", f"{rental_details['cost']} {CURRENCY}")
    html_content = html_content.replace("%client_price_total%", f"{rental_details['cost']} {CURRENCY}")

    msg = MIMEMultipart()
    msg["From"] = f"Jakub Gożuk PW"
    msg["To"] = customer_email
    msg["Subject"] = "Faktura za wynajem roweru"

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(os.getenv("EMAIL_SENDER"), customer_email, msg.as_string())
            print(f"\033[92mE-mail with the invoice has been sent to: {customer_email}\033[0m")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")