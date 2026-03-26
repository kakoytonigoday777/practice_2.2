import requests
import json

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = 'resource/save.json'
COURSES_FILE = 'resource/courses.json'  # файл для хранения курсов

def load_course():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        print("Ответ сервера:", response.text)
        data = response.json()
        return data['Valute']
    except requests.RequestException as e:
        print(f"Ошибка при получении данных о курсах: {e}")
        return None
    except json.JSONDecodeError:
        print("Ошибка парсинга json")
        return None
    except KeyError:
        print("Неправильный формат данных")
        return None

def show_all(course):
    if not course:
        print("Нет данных о курсах")
        return
    print("\nВсе валюты и курсы:")
    for code, info in course.items():
        if all(k in info for k in ('Код', 'Название', 'Курс')):
            print(f"{info['Код']}: {info['Название']} - {info['Курс']} руб.")
        else:
            print(f"Некорректная запись для кода {code}: {info}")

def get_by_code(course, code):
    if not course:
        print("Нет данных о курсах")
        return None
    return course.get(code)

def load_groups():
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            groups = json.load(f)
        return groups
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Ошибка при чтении файла групп, создается новая")
        return {}

def save_groups(groups):
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def create_group(groups, group_name):
    if group_name in groups:
        print("Группа с таким именем уже существует!")
    else:
        groups[group_name] = []
        print(f"Группа '{group_name}' создана")

def add_to_group(groups, group_name, currency_code):
    if group_name not in groups:
        print("Группа не найдена")
        return
    if currency_code in groups[group_name]:
        print("Валюта уже в группе")
    else:
        groups[group_name].append(currency_code)
        print(f"Валюта {currency_code} добавлена в группу {group_name}")

def delete_from_group(groups, group_name, valuta_code):
    if group_name not in groups:
        print("Группа не найдена")
        return
    if valuta_code in groups[group_name]:
        groups[group_name].remove(valuta_code)
        print(f"Валюта {valuta_code} удалена из группы {group_name}")
    else:
        print("Валюта не найдена в группе")

def show_groups(groups):
    if not groups:
        print("Нет созданных групп")
        return
    print("\nСписок групп и валют в них:")
    for group_name, valutes in groups.items():
        print(f"'{group_name}': {', '.join(valutes) if valutes else 'пусто'}")

def save_courses(course):
    try:
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(course, f, ensure_ascii=False, indent=4)
        print("Курсы успешно сохранены в файл 'courses.json'.")
    except Exception as e:
        print(f"Ошибка при сохранении курсов: {e}")

def main():
    print("Загружаю данные о курсах валют...")
    course = load_course()
    if course:
        save_courses(course)  # сохраняем курсы в отдельный файл
    else:
        print("Не удалось загрузить курсы валют, пытаюсь загрузить из файла 'courses.json'...")

        # Попытка загрузить из файла, если интернет недоступен
        try:
            with open(COURSES_FILE, 'r', encoding='utf-8') as f:
                course = json.load(f)
            print("Данные о курсах загружены из файла.")
        except Exception:
            print("Не удалось загрузить данные о курсах. Завершение.")
            return

    groups = load_groups()

    while True:
        print("\n=== Главное меню ===")
        print("1. Просмотреть все валюты")
        print("2. Посмотреть курс валюты по коду")
        print("3. Создать группу валют")
        print("4. Добавить валюту в группу")
        print("5. Удалить валюту из группы")
        print("6. Посмотреть все группы")
        print("7. Выйти")
        choice = input("Выберите действие (1-7): ").strip()

        if choice == '1':
            show_all(course)
        elif choice == '2':
            code = input("Введите код валюты (например, USD): ").upper()
            val = get_by_code(course, code)
            if val:
                print(f"{val['Name']} ({val['CharCode']}): {val['Value']} руб.")
            else:
                print("Валюта с таким кодом не найдена")
        elif choice == '3':
            name = input("Введите название группы: ").strip()
            create_group(groups, name)
            save_groups(groups)
        elif choice == '4':
            group_name = input("Введите название группы: ").strip()
            code = input("Введите код валюты: ").upper()
            if code in course:
                add_to_group(groups, group_name, code)
                save_groups(groups)
            else:
                print("Некорректный код валюты")
        elif choice == '5':
            group_name = input("Введите название группы: ").strip()
            code = input("Введите код валюты: ").upper()
            delete_from_group(groups, group_name, code)
            save_groups(groups)
        elif choice == '6':
            show_groups(groups)
        elif choice == '7':
            print("До свидания!")
            break
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()