log_filename = 'resource/calculator.log'

def show_last_operations():
    try:
        with open(log_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print("Последние 5 операций:")
            for line in lines[-5:]:
                print(line.strip())
    except FileNotFoundError:
        print("Лог-файл пуст или не существует.")

def format_result(result):
    if result == int(result):
        return str(int(result))
    else:
        return str(result)

def log_operation(expression, result):
    time_module = __import__('time')
    current_time = time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime())
    log_line = f"[{current_time}] {expression} = {result}\n"
    with open(log_filename, 'a', encoding='utf-8') as f:
        f.write(log_line)

def clear_log():
    open(log_filename, 'w', encoding='utf-8').close()
    print("Лог-файл очищен.")

def calculator():
    show_last_operations()
    while True:
        print("\nВыберите действие:")
        print("1. Выполнить расчет")
        print("2. Очистить лог-файл")
        print("3. Выйти")
        choice = input("Введите номер действия: ")

        if choice == '1':
            try:
                num1 = float(input("Введите первое число: "))
                num2 = float(input("Введите второе число: "))
                op = input("Выберите операцию (+, -, *, /): ").strip()

                if op not in ['+', '-', '*', '/']:
                    print("Неправильная операция.")
                    continue

                if op == '+':
                    result = num1 + num2
                elif op == '-':
                    result = num1 - num2
                elif op == '*':
                    result = num1 * num2
                elif op == '/':
                    if num2 == 0:
                        print("На ноль делить нельзя!")
                        continue
                    result = num1 / num2

                formatted_result = format_result(result)
                expression = f"{num1} {op} {num2}"
                print(f"Результат: {formatted_result}")
                log_operation(expression, formatted_result)
            except:
                print("Ошибка при вводе чисел.")
        elif choice == '2':
            clear_log()
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неправильный выбор, попробуйте снова!")

if __name__ == "__main__":
    calculator()