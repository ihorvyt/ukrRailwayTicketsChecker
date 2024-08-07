import httpx
import time
import requests
from colorama import Fore, Style, init
import pygame
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)

# Telegram bot configuration
TELEGRAM_TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

pygame.mixer.init()
pygame.mixer.music.load('notification.mp3')

# UZ API configuration
url = 'https://app.uz.gov.ua/api/v3/trips'

oneThousend = 1000  # Define oneThousend at the module level

params = {
    'station_from_id': '2200001',
    'station_to_id': '2218200',
    'with_transfers': '0',
    'date': '2024-08-13'
}

headers = {
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
    'X-User-Agent': 'UZ/2 Web/1 User/guest',
    'Accept-Language': 'uk-UA',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36',
    'Accept': 'application/json',
    'X-Client-Locale': 'uk',
    'X-Session-Id': 'd5962117-4538-4d0c-ac7c-9c6e3cbbd9d8',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://booking-new.uz.gov.ua',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://booking-new.uz.gov.ua/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=1, i'
}

def play_notification_sound():
    pygame.mixer.music.play()

def get_color_for_class(class_name):
    """Функція для вибору кольору на основі назви класу вагона"""
    colors = {
        'Люкс': Fore.CYAN,
        'Жіноче купе': Fore.MAGENTA,
        'Дитяче купе': Fore.BLUE,
        'Купе': Fore.GREEN,
        'Плацкарт': Fore.YELLOW,
        'Помилка': Fore.RED
    }
    return colors.get(class_name, Style.RESET_ALL)

def format_message(data, oneThousend):
    """Функція для формування тексту повідомлення з даних"""
    messages = []
    messagesForTg = []
    messageFreeTickets = []
    if 'direct' in data:
        for trip in data['direct']:
            if 'train' in trip:
                train = trip['train']
                if 'wagon_classes' in train:
                    wagon_classes = train['wagon_classes']
                    for wagon_class in wagon_classes:
                        class_name = wagon_class.get('name', 'Unknown')
                        free_seats = wagon_class.get('free_seats', 'N/A')
                        color = get_color_for_class(class_name)
                        if (free_seats > 0):
                            messageFreeTickets.append(f"Поїзд: {train.get('number', 'Unknown')}, Клас: {color}{class_name}{Style.RESET_ALL}, Вільні місця: {free_seats}{Style.RESET_ALL}")
                        messagesForTg.append(f"Поїзд: {train.get('number', 'Unknown')}, Клас: {color}{class_name}{Style.RESET_ALL}, Вільні місця: {free_seats}{Style.RESET_ALL}")
                        messages.append(f"Поїзд: {train.get('number', 'Unknown')}, Клас: {class_name}, Вільні місця: {free_seats}")
                else:
                    messages.append("Немає інформації про класи вагонів.")
    else:
        messages.append("Немає прямих рейсів.")
    
    print('\n'.join(messagesForTg))
    if messageFreeTickets:
        print('\n-----------------------------------------')
    else:
        oneThousend -= 7
        print(oneThousend)
        print(
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠓⠄⠉⠻⣿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢉⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⠄⠄⠄⠄⠄⠄⠄⠄⡀⠄⠄⠄⠄⠄⠄⠄⡀⠄⡀⠄⠄⠄⠄⠄⠄⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠄⠄⠄⠃⠄⠄⠄⠄⢨⠄⠄⠄⢀⠠⠄⠄⠈⢂⢀⢀⠄⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⢀⠠⠄⡆⠄⠄⠂⠄⠃⠄⠄⠈⠄⠄⠄⠄⠠⢈⢂⠈⢄⢫⠄⠆⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⡄⠆⠄⡁⡆⡇⡇⡄⠄⠄⠄⢈⠄⠄⠄⢢⠄⠄⡀⢃⠘⡀⡖⠈⡀⡀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠄⠄⢰⠄⡐⣼⡇⡇⠿⣇⡇⠄⠄⡆⢸⠄⡀⠄⢸⡡⠄⠄⠄⢦⡇⢰⠄⠃⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⡻⡡⠄⠄⢀⣾⠃⣿⡇⡇⣇⣿⢤⠄⣆⡧⢿⠄⡆⠄⢸⠰⢡⠄⠄⢸⠁⣼⠄⣇⠉⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⡿⠟⠉⠄⠄⠐⠁⢸⢰⠄⠘⣻⠄⣿⡇⣇⡟⣿⢺⣰⡗⣧⣼⠄⡇⡆⢸⢰⢿⡆⠄⢸⡆⣿⡀⡿⡄⠂⠄⠄⠉⠙⠻⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠄⠄⠈⣼⠠⢀⢿⢰⣿⣠⣏⢀⣭⢾⠁⠃⣿⢻⡄⡇⡇⢈⢠⢸⡇⣡⣸⢿⣿⣷⣽⡄⠐⠄⠄⠄⠠⠄⢹⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⠄⠄⠈⢦⣐⢄⣀⡀⠄⠻⣡⡎⠄⢩⡷⣅⣿⣿⣸⢸⢀⠄⣿⣾⠃⣷⣿⣜⢸⣿⣷⡦⣏⣿⣿⣿⣿⣿⣦⣆⠄⡠⠁⠄⠄⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⠄⠄⠄⠈⣿⣷⣿⣿⣿⣾⣿⠃⠄⣼⠗⠁⣿⣸⣻⡸⢸⣄⣿⣽⢰⣿⡏⡯⣾⣿⣿⢨⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⠄⠄⠄⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⠄⠄⠄⠄⠘⣿⣿⣿⣿⣿⣿⣤⣴⡟⠄⠄⣿⣿⣿⣿⡾⣻⣿⣿⣿⣿⣿⣿⢹⢾⣏⣿⣿⣿⣿⣿⣿⣿⣿⡟⣡⡎⠄⠄⠄⢸⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⠄⠄⠄⠄⢤⡈⢿⣿⣿⣿⣿⣿⣿⣿⣶⣴⣿⣿⡿⠋⢠⣿⣿⣿⣟⣯⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠏⣴⡿⠄⠄⠄⠄⣾⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⡆⠄⠄⢀⠘⢿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣤⣼⣿⣿⠁⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣾⡿⠁⠄⣠⠄⢠⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣧⠄⠄⠄⠙⢦⣹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡿⠁⠄⠈⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⠄⠄⠄⢿⣶⣿⣷⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠿⢿⣿⣿⣿⣿⣿⣿⣿⠋⠄⠄⠄⣴⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⠄⠄⠄⠈⢿⣿⣿⣿⣿⣿⡿⠋⠹⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣴⠄⠸⣿⣿⣿⣿⠟⠁⣀⠄⠄⢰⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⡀⠄⠄⠄⠄⠻⣿⣿⣿⣿⡇⠄⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠄⠄⣿⣿⣿⣿⣿⡿⠃⠄⠄⢸⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣷⡀⠄⣀⣀⣴⣿⣿⣿⡿⠁⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⣿⣿⣿⣿⣿⠄⠄⠄⠄⣸⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⠇⠄⣿⣿⣿⣿⣿⡿⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠄⠄⢃⠙⢿⣿⣿⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⠄⠄⣿⣿⣿⣿⠟⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢆⢈⡄⢨⢿⣿⡇⠄⠄⢠⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⡇⠄⢿⣿⠟⠁⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⢀⠄⠻⠇⠄⠄⣸⣿⣿⣿⣿⣿⣿⣿\n" +
            "⣿⣿⣿⣿⣿⣿⣿⡀⢸⡿⠄⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡀⠄⠁⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿\n"
        )
        print(f'{Fore.RED}No tickets{Style.RESET_ALL}')

    return {
        'freeTickets': '\n'.join(messageFreeTickets),
        'allTickets': '\n'.join(messages),
        'oneThousend': oneThousend
    } 

def send_telegram_message(message):
    """Функція для надсилання повідомлень в Telegram"""
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()
        print('Повідомлення надіслано в Telegram.')
    except requests.RequestException as e:
        print(f"Помилка при надсиланні повідомлення в Telegram: {e}")

def check_tickets():
    global oneThousend  # Declare that we want to use the global oneThousend
    try:
        with httpx.Client(http2=True) as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            message = format_message(data, oneThousend)
            oneThousend = message['oneThousend']
            if message['freeTickets'] != '':
                play_notification_sound()
                send_telegram_message(message['freeTickets'])
        
    except httpx.RequestError as e:
        print(f"Запит завершився помилкою: {e}")
    except ValueError:
        print("Не вдалося декодувати JSON відповідь.")

# Запуск бота
while True:
    check_tickets()
    time.sleep(5)  # Changed wait time to 60 seconds