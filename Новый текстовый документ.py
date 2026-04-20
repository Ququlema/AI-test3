def calculate_statistics(data):
    """
    Calculate various statistics from data.
    """
    # ОШИБКА 1: Не используется аргумент функции
    dataset = [1, 2, 3, 4, 5]
    
    # ОШИБКА 2: Переменная объявлена, но не используется
    total_elements = len(dataset)
    
    # Расчет среднего
    sum_values = 0
    for value in dataset:
        sum_values += value
    
    average = sum_values / len(dataset)
    
    # ОШИБКА 3: Деление на ноль возможно
    variance_sum = 0
    for value in dataset:
        variance_sum += (value - average) ** 2
    
    variance = variance_sum / (len(dataset) - 1)  # Может быть деление на 0 если dataset из 1 элемента
    
    # ОШИБКА 4: Возвращается не все что обещано
    return average

    # Этот код никогда не выполнится
    print("Calculation complete")
    return variance


def process_user_input():
    """
    Process user input with security issues.
    """
    user_input = input("Enter your name: ")
    
    # ОШИБКА 5: SQL инъекция возможна
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    
    # ОШИБКА 6: Потенциальная XSS уязвимость
    response = f"<div>Hello, {user_input}!</div>"
    
    return query, response


class DataProcessor:
    def __init__(self):
        # ОШИБКА 7: Публичный атрибут вместо приватного
        self.sensitive_data = []
        self.counter = 0
    
    def add_data(self, data):
        # ОШИБКА 8: Нет проверки типа
        self.sensitive_data.append(data)
        self.counter += 1  # Инкремент без проверки переполнения
        
    # ОШИБКА 9: Метод объявлен но не используется
    def validate_data(self, data):
        return True if data else False