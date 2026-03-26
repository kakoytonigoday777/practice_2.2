import json

FILENAME = 'resource/library.json'

def load_data():
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {FILENAME} не найден. Загружается пустая библиотека.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения файла {FILENAME}. Проверьте формат JSON.")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при загрузке данных: {e}")
        return []

def save_data(data):
    try:
        with open(FILENAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def prosmotr_vsego():
    data = load_data()
    if not data:
        print("Библиотека пуста.")
        return
    for book in data:
        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Доступность: {book['available']}")

def poisk():
    data = load_data()
    criteriy = input("Поиск по (1) названию или (2) автору? Введите 1 или 2: ")
    kluchevoe_slovo = input("Введите ключевое слово: ").lower()
    result = []
    for book in data:
        if criteriy == '1' and kluchevoe_slovo in book['title'].lower():
            result.append(book)
        elif criteriy == '2' and kluchevoe_slovo in book['author'].lower():
            result.append(book)
    if result:
        for book in result:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Доступность: {book['available']}")
    else:
        print("Книги не найдены.")

def add():
    data = load_data()
    max_id = max([book['id'] for book in data], default=0)
    new_id = max_id + 1
    title = input("Введите название книги: ")
    author = input("Введите автора: ")
    year = input("Введите год написания: ")
    available = 'в наличии'
    new_book = {'id': new_id, 'title': title, 'author': author, 'year': year, 'available': available}
    data.append(new_book)
    save_data(data)
    print("Книга добавлена.")

def change_status():
    data = load_data()
    try:
        id_book = int(input("Введите ID книги: "))
        for book in data:
            if book['id'] == id_book:
                book['available'] = 'взята' if book['available'] == 'в наличии' else 'в наличии'
                save_data(data)
                print(f"Доступность книги изменена на: {book['available']}")
                return
        print("Книга с таким ID не найдена.")
    except ValueError:
        print("Неправильный ввод. Пожалуйста, введите числовой ID.")

def delete():
    data = load_data()
    try:
        id_delete = int(input("Введите ID книги для удаления: "))
        new_list = [book for book in data if book['id'] != id_delete]
        if len(new_list) == len(data):
            print("Книга с таким ID не найдена.")
        else:
            save_data(new_list)
            print("Книга удалена.")
    except ValueError:
        print("Неправильный ввод. Пожалуйста, введите числовой ID.")

def export():
    data = load_data()
    dostupniye = [book for book in data if book['available'] == 'в наличии']
    try:
        with open('available_books.txt', 'w', encoding='utf-8') as f:
            for book in dostupniye:
                f.write(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}\n")
        print("Список доступных книг экспортирован в available_books.txt.")
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")

def main_menu():
    while True:
        print("\nМеню:")
        print("1. Просмотр всех книг")
        print("2. Поиск книг")
        print("3. Добавить новую книгу")
        print("4. Изменить доступность книги")
        print("5. Удалить книгу")
        print("6. Экспорт доступных книг")
        print("0. Выход")
        choise = input("Выберите действие: ")
        if choise == '1':
            prosmotr_vsego()
        elif choise == '2':
            poisk()
        elif choise == '3':
            add()
        elif choise == '4':
            change_status()
        elif choise == '5':
            delete()
        elif choise == '6':
            export()
        elif choise == '0':
            break
        else:
            print("Неправильный выбор, попробуйте снова!")

if __name__ == "__main__":
    main_menu()