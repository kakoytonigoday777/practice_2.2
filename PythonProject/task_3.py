filename = 'resource/products.csv'

def read_products():
    products = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                return products
            headers = lines[0].strip().split(',')
            for line in lines[1:]:
                row = line.strip().split(',')
                product = {
                    'Название': row[0],
                    'Количество': int(row[1]),
                    'Цена': float(row[2])
                }
                products.append(product)
    except FileNotFoundError:
        pass
    return products

def save_products(products):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('Название,Количество,Цена\n')
        for p in products:
            line = f"{p['Название']},{p['Количество']},{p['Цена']}\n"
            file.write(line)

products = read_products()

def add_product():
    name = input("Введите название товара: ")
    quantity = int(input("Введите количество: "))
    price = float(input("Введите цену: "))
    products.append({'Название': name, 'Количество': quantity, 'Цена': price})

def search_product():
    search_name = input("Введите название товара для поиска: ")
    found = False
    for p in products:
        if p['Название'].lower() == search_name.lower():
            print(f"Найден товар: {p}")
            found = True
            break
    if not found:
        print("Товар не найден.")

def total_value():
    total = 0
    for p in products:
        total += p['Количество'] * p['Цена']
    print(f"Общая стоимость всех товаров: {total}")

while True:
    print("\nМеню:")
    print("1. Добавить товар")
    print("2. Поиск товара")
    print("3. Расчет общей стоимости")
    print("4. Выйти и сохранить изменения")
    choice = input("Выберите действие (1-4): ")

    if choice == '1':
        add_product()
    elif choice == '2':
        search_product()
    elif choice == '3':
        total_value()
    elif choice == '4':
        save_products(products)
        print("Программа завершена.")
        break
    else:
        print("Неправильный выбор, попробуйте снова!")