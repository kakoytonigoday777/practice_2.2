stroki = [
    "Привет мир!",
    "Простая строка",
    "Это первое задание в этом файле",
    "Мистер Бист",
    "Легенда"
]

with open("resource/text.txt", "w", encoding="utf-8") as file:
    for line in stroki:
        file.write(line + "\n")

with open("resource/text.txt", "r", encoding="utf-8") as file:
    spisok_strok = file.readlines()

num_lines = len(spisok_strok)

words = []
for line in spisok_strok:
    stripped_line = line.strip()
    slova = stripped_line.split()
    for word in slova:
        words.append(word)

num_words = len(words)

longest_line = max(spisok_strok, key=len).strip()

print(f"Количество строк: {num_lines}")
print(f"Количество слов: {num_words}")
print(f"Самая длинная строка: {longest_line}")