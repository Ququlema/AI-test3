"""
ТЕСТОВЫЙ ФАЙЛ С НАМЕРЕННЫМИ ОШИБКАМИ
Для проверки работы AI Review
Содержит 25+ различных типов ошибок и анти-паттернов
"""

import os
import sys
import json
from typing import List, Dict, Optional
import requests
import sqlite3
from datetime import datetime
import re

# ============================================
# 1. БЕЗОПАСНОСТЬ
# ============================================

# 🔴 Критично: Хранение секретов в коде
API_KEY = "sk-live-1234567890abcdef"
PASSWORD = "admin123"
DB_PASSWORD = "root:password@localhost"

# 🔴 Критично: SQL-инъекция
def get_user_data(user_id: str):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # ⚠️ Уязвимость SQL-инъекции
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)  # Опасный вызов!
    return cursor.fetchall()

# 🔴 Критично: Выполнение shell команд из пользовательского ввода
def run_command(user_input: str):
    # ⚠️ Командно-инъекционная уязвимость
    os.system(f"ls {user_input}")  # Очень опасно!
    os.popen(f"echo {user_input}")  # Тоже опасно

# 🔴 Критично: Невалидированные редиректы
def redirect_user(url_param: str):
    import webbrowser
    # ⚠️ Открытие произвольных URL
    webbrowser.open(url_param)

# ============================================
# 2. ПРОИЗВОДИТЕЛЬНОСТЬ
# ============================================

# 🟡 Предупреждение: N+1 проблема в цикле
def get_users_with_posts():
    users = ["user1", "user2", "user3"]
    all_posts = []
    
    # ⚠️ N+1 запросов
    for user in users:
        # Предположим, что это делает запрос к БД
        posts = [f"post_{i}" for i in range(10)]  # Имитация запроса
        all_posts.extend(posts)
    
    return all_posts

# 🟡 Предупреждение: Квадратичная сложность
def find_duplicates(items: List[str]) -> List[str]:
    duplicates = []
    # ⚠️ O(n²) сложность
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                duplicates.append(items[i])
    return list(set(duplicates))

# 🟡 Предупреждение: Бесконечный цикл
def process_data(data: List[int]):
    i = 0
    # ⚠️ Потенциально бесконечный цикл
    while i < len(data):
        # Забыли i += 1
        result = data[i] * 2
        print(result)
        # i += 1  # Забытая инкрементация

# 🟡 Предупреждение: Неэффективная конкатенация строк
def build_html_string(items: List[str]) -> str:
    html = "<ul>"
    # ⚠️ Конкатенация в цикле - O(n²)
    for item in items:
        html += f"<li>{item}</li>"
    html += "</ul>"
    return html

# ============================================
# 3. ОШИБКИ И ИСКЛЮЧЕНИЯ
# ============================================

# 🔴 Критично: Проглатывание исключений
def divide_numbers(a: float, b: float) -> Optional[float]:
    try:
        return a / b
    except:
        # ⚠️ Проглатываем все исключения
        pass  # Ужасная практика!
    return None

# 🔴 Критично: Слишком широкий except
def read_file(filename: str):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:  # ⚠️ Слишком широко
        print(f"Ошибка: {e}")
        return None

# 🟡 Предупреждение: Не проверяем None
def get_user_name(user_id: int) -> str:
    users = {1: "Alice", 2: "Bob"}
    name = users.get(user_id)  # Может вернуть None
    # ⚠️ Не проверяем на None перед вызовом метода
    return name.upper()  # AttributeError если name is None

# 🟡 Предупреждение: Неинициализированная переменная
def calculate_stats(numbers: List[float]):
    # ⚠️ Не всегда инициализируется
    if len(numbers) > 0:
        total = sum(numbers)
    # total может быть не определен!
    average = total / len(numbers)  # UnboundLocalError
    return average

# ============================================
# 4. КАЧЕСТВО КОДА И ЧИТАЕМОСТЬ
# ============================================

# 🔵 Совет: Слишком сложная функция
def process_user_data(user_data: Dict, config: Dict, options: Dict, 
                      callback=None, validate: bool = True) -> Dict:
    """
    ⚠️ Функция делает слишком много всего
    Нарушение Single Responsibility Principle
    """
    # Валидация
    if validate:
        if not user_data.get('name'):
            raise ValueError("No name")
        if not user_data.get('email'):
            raise ValueError("No email")
    
    # Обработка
    processed = {}
    processed['name'] = user_data['name'].upper()
    processed['email'] = user_data['email'].lower()
    
    # Форматирование
    if config.get('add_timestamp'):
        processed['timestamp'] = datetime.now().isoformat()
    
    # Дополнительная логика
    if options.get('log_to_file'):
        with open('log.txt', 'a') as f:
            f.write(json.dumps(processed))
    
    # Колбэк
    if callback:
        callback(processed)
    
    # Возврат
    return processed

# 🔵 Совет: Магические числа
def calculate_discount(price: float) -> float:
    # ⚠️ Что такое 0.9 и 0.8?
    if price > 100:
        return price * 0.9  # Магическое число
    else:
        return price * 0.8  # Магическое число

# 🔵 Совет: Дублирование кода
def validate_email_v1(email: str) -> bool:
    # ⚠️ Дублирование с validate_email_v2
    if "@" in email and "." in email.split("@")[1]:
        return True
    return False

def validate_email_v2(email: str) -> bool:
    # ⚠️ Почти такой же код как в validate_email_v1
    if "@" in email and "." in email.split("@")[1]:
        return True
    return False

# 🔵 Совет: Слишком длинная строка
def create_very_long_string():
    # ⚠️ Слишком длинная строка (PEP8: max 79 символов)
    long_string = "Это очень длинная строка которая нарушает PEP8 рекомендации по длине строки и делает код менее читаемым особенно когда приходится скроллить горизонтально чтобы увидеть всю строку целиком что очень неудобно для разработчиков"
    return long_string

# 🔵 Совет: Неиспользуемый код
def unused_function():
    """Эта функция никогда не вызывается"""
    return "dead code"

unused_variable = "Я нигде не используюсь"  # ⚠️ Неиспользуемая переменная

# ============================================
# 5. ТИПИЗАЦИЯ И type hints
# ============================================

# 🔵 Совет: Отсутствие type hints
def process_data_no_types(data):  # ⚠️ Нет аннотаций типов
    result = []
    for item in data:
        result.append(str(item))
    return result

# 🔵 Совет: Неправильные type hints
def add_numbers(a: "число", b: "еще число") -> "результат":  # ⚠️ Строки вместо типов
    return a + b

# 🔵 Совет: Any вместо конкретного типа
from typing import Any

def handle_data(data: Any) -> Any:  # ⚠️ Слишком общие типы
    return data * 2

# ============================================
# 6. АНТИПАТТЕРНЫ И ПЛОХИЕ ПРАКТИКИ
# ============================================

# 🔵 Совет: God object
class UserManager:
    """⚠️ Нарушение Single Responsibility Principle"""
    
    def __init__(self):
        self.users = []
        self.db_connection = None
        self.email_service = None
        self.logger = None
        self.config = {}
    
    def connect_to_db(self):
        # Логика БД
        pass
    
    def send_email(self):
        # Логика email
        pass
    
    def validate_user(self):
        # Валидация
        pass
    
    def generate_report(self):
        # Отчеты
        pass
    
    def backup_data(self):
        # Бэкапы
        pass
    
    # ... и еще 20 методов

# 🔵 Совет: Излишняя сложность
def is_even_number(num: int) -> bool:
    """
    ⚠️ Излишне сложная реализация простой проверки
    """
    binary = bin(num)
    last_bit = binary[-1]
    
    if last_bit == '0':
        if num % 2 == 0:
            return True
        else:
            return False
    else:
        if num % 2 != 0:
            return False
        else:
            return True
    
    # Вместо просто: return num % 2 == 0

# 🔵 Совет: Жесткие зависимости
class PaymentProcessor:
    def __init__(self):
        # ⚠️ Жесткая зависимость
        self.gateway = PayPalGateway()  # Напрямую создаем зависимость
    
    def process(self, amount: float):
        return self.gateway.charge(amount)

class PayPalGateway:
    def charge(self, amount: float):
        return f"Charged {amount} via PayPal"

# 🔵 Совет: Нарушение YAGNI
def prepare_for_future_features():
    """
    ⚠️ Реализация функционала "на будущее"
    Нарушение YAGNI (You Ain't Gonna Need It)
    """
    # Эти методы никогда не понадобятся
    pass
    
def calculate_moon_phase():  # ⚠️ Не нужен в бизнес-приложении
    pass
    
def translate_to_klingon():  # ⚠️ Не нужен
    pass

# ============================================
# 7. БАГИ И ЛОГИЧЕСКИЕ ОШИБКИ
# ============================================

# 🔴 Критично: Off-by-one ошибка
def get_slice(items: List[str], start: int, end: int) -> List[str]:
    # ⚠️ Off-by-one: end индекс обычно exclusive
    return items[start:end + 1]  # Должно быть items[start:end]

# 🔴 Критично: Неправильное сравнение с плавающей точкой
def compare_floats(a: float, b: float) -> bool:
    # ⚠️ Нельзя точно сравнивать float
    return a == b  # Может не работать как ожидается

# 🟡 Предупреждение: Потенциальное деление на ноль
def calculate_average(numbers: List[int]) -> float:
    total = sum(numbers)
    # ⚠️ Не проверяем пустой список
    return total / len(numbers)  # ZeroDivisionError если numbers пустой

# 🟡 Предупреждение: Изменяемые аргументы по умолчанию
def add_to_list(item, items=[]):  # ⚠️ Изменяемый аргумент по умолчанию
    items.append(item)
    return items

# 🟡 Предупреждение: Проблемы с кодировкой
def read_file_with_encoding(filename: str) -> str:
    # ⚠️ Не указана кодировка
    with open(filename, 'r') as f:  # Могут быть проблемы с кодировкой
        return f.read()

# ============================================
# 8. СТИЛЬ И ФОРМАТИРОВАНИЕ (PEP8)
# ============================================

# 🔵 Совет: Несоответствие PEP8
def BadlyFormattedFunction (  ) :  # ⚠️ Неправильные пробелы
    x=5  # ⚠️ Нет пробелов вокруг оператора
    y =10
    z = x + y
    if(z>10):  # ⚠️ Лишние скобки и нет пробелов
        print("больше 10")
    else:
        print("меньше или равно 10")
    return z

# 🔵 Совет: Смешивание табуляций и пробелов
def tabs_and_spaces():
	# ⚠️ Табы (это плохо)
    # ⚠️ Пробелы (это хорошо)
    return "mixed"  # Приводит к проблемам

# 🔵 Совет: Слишком короткие имена
def fx(d):  # ⚠️ Непонятные имена
    r = 0
    for i in d:
        r += i
    return r

# ============================================
# 9. МЕМОРИ ЛИКИ И РЕСУРСЫ
# ============================================

# 🔴 Критично: Утечка файловых дескрипторов
def read_multiple_files(filenames: List[str]) -> List[str]:
    contents = []
    for filename in filenames:
        # ⚠️ Утечка дескриптора: файл не закрывается при исключении
        f = open(filename, 'r')
        contents.append(f.read())
        # f.close()  # Забыли закрыть файл
    return contents

# 🟡 Предупреждение: Циклические ссылки
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
    def set_next(self, node):
        self.next = node
        # ⚠️ Потенциальная циклическая ссылка
        if node:
            node.next = self  # Создаем цикл

# 🟡 Предупреждение: Большие объекты в памяти
def load_huge_dataset():
    # ⚠️ Загружаем все в память
    with open('huge_file.txt', 'r') as f:
        data = f.readlines()  # Читаем все строки сразу
    return data

# ============================================
# 10. СЕТЕВЫЕ И API ОШИБКИ
# ============================================

# 🔴 Критично: Нет таймаута на сетевые запросы
def fetch_data_no_timeout(url: str):
    # ⚠️ Нет таймаута - может висеть вечно
    response = requests.get(url)  # Без timeout!
    return response.json()

# 🟡 Предупреждение: Не проверяем статус ответа
def fetch_user_data(user_id: int):
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url, timeout=5)
    # ⚠️ Не проверяем response.status_code
    return response.json()  # Может упасть с ошибкой

# 🟡 Предупреждение: Ретеи без экспоненциальной задержки
def call_api_with_bad_retry(url: str, max_retries: int = 3):
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            return response.json()
        except requests.exceptions.RequestException:
            # ⚠️ Нет задержки между ретеями (thundering herd)
            continue
    return None

# ============================================
# 11. МНОГОПОТОЧНОСТЬ И КОНКУРЕНЦИЯ
# ============================================

# 🔴 Критично: Race condition
import threading

counter = 0

def increment_counter():
    global counter
    # ⚠️ Race condition: не атомарная операция
    temp = counter
    # Между этими строками может влезть другой поток
    counter = temp + 1

# 🔴 Критично: Deadlock
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        # ⚠️ Может случиться deadlock
        with lock_b:
            print("Thread 1")

def thread_2():
    with lock_b:
        # ⚠️ Обратный порядок блокировок
        with lock_a:
            print("Thread 2")

# ============================================
# 12. ДЕПЛОЙ И КОНФИГУРАЦИЯ
# ============================================

# 🔵 Совет: Жестко закодированные пути
def read_config():
    # ⚠️ Абсолютный путь, не переносимо
    config_path = "/home/user/project/config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

# 🔵 Совет: Зависимость от окружения
def get_database_url():
    # ⚠️ Зависит от конкретного окружения
    if os.path.exists("/prod/"):
        return "mysql://prod-host/db"
    else:
        return "sqlite:///local.db"

# ============================================
# ТЕСТИРОВАНИЕ
# ============================================

def run_tests():
    """Запускаем все проблемные функции"""
    
    # Демонстрация ошибок
    
    # 1. SQL инъекция (не запускать на реальной БД!)
    # print(get_user_data("1 OR 1=1"))
    
    # 2. Деление на ноль
    try:
        print(divide_numbers(10, 0))
    except:
        pass
    
    # 3. Off-by-one
    items = ["a", "b", "c", "d"]
    print(get_slice(items, 1, 3))  # Ожидается ["b", "c"], получим ["b", "c", "d"]
    
    # 4. Изменяемый аргумент по умолчанию
    print(add_to_list(1))  # [1]
    print(add_to_list(2))  # Ожидается [2], получим [1, 2]
    
    # 5. Непроверенный None
    try:
        print(get_user_name(999))  # AttributeError
    except:
        pass
    
    # 6. Бесконечный цикл (закомментировано)
    # process_data([1, 2, 3])
    
    return "Tests completed (with many issues!)"

if __name__ == "__main__":
    print("🔍 Этот файл содержит МНОЖЕСТВО ошибок для тестирования AI Review")
    print("=" * 60)
    run_tests()
    
    # Выводим список всех проблем
    print("\n" + "=" * 60)
    print("📋 Список категорий ошибок в этом файле:")
    print("=" * 60)
    print("1.  🔴 Безопасность (SQL-инъекции, секреты в коде)")
    print("2.  🟡 Производительность (O(n²), N+1 запросы)")
    print("3.  🔴 Обработка ошибок (проглатывание исключений)")
    print("4.  🔵 Качество кода (сложные функции, дублирование)")
    print("5.  🔵 Типизация (отсутствие type hints)")
    print("6.  🔵 Антипаттерны (God object, YAGNI)")
    print("7.  🔴 Логические ошибки (off-by-one, деление на ноль)")
    print("8.  🔵 Стиль кода (нарушение PEP8)")
    print("9.  🔴 Утечки ресурсов (файлы, память)")
    print("10. 🔴 Сетевые ошибки (нет таймаутов, ретей)")
    print("11. 🔴 Многопоточность (race conditions, deadlock)")
    print("12. 🔵 Конфигурация (жесткие пути, окружение)")
    print("=" * 60)
    print(f"Всего категорий ошибок: 12")
    print(f"Примерное количество конкретных ошибок: 25+")
    print("=" * 60)