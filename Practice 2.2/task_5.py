import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import requests
import psutil
import json
import os

SAVE_FILE = 'save_groups.json'
COURSES_FILE = 'courses.json'
TOKEN = ''

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Настольное приложение")
        self.geometry("1000x800")
        self.courses = {}
        self.groups = {}
        self.load_courses()
        self.load_groups()
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')
        self.page_url_check = ttk.Frame(notebook)
        self.page_resources = ttk.Frame(notebook)
        self.page_courses = ttk.Frame(notebook)
        self.page_github = ttk.Frame(notebook)
        notebook.add(self.page_url_check, text='Проверка URL')
        notebook.add(self.page_resources, text='Ресурсы системы')
        notebook.add(self.page_courses, text='Курсы валют')
        notebook.add(self.page_github, text='GitHub')
        self.setup_url_check()
        self.setup_resources()
        self.setup_courses()
        self.setup_github()

    def setup_url_check(self):
        ttk.Label(self.page_url_check, text="Введите URL или список URL через запятую:").pack(pady=5)
        self.txt_urls = tk.Text(self.page_url_check, height=10)
        self.txt_urls.pack(pady=5)
        ttk.Button(self.page_url_check, text="Проверить URL", command=self.check_urls).pack(pady=5)
        self.txt_url_result = scrolledtext.ScrolledText(self.page_url_check, height=15)
        self.txt_url_result.pack(pady=5)

    def check_urls(self):
        urls_text = self.txt_urls.get("1.0", tk.END).strip()
        urls = [u.strip() for u in urls_text.split(',')]
        self.txt_url_result.delete('1.0', tk.END)
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                code = response.status_code
                if code == 200:
                    status = "доступен"
                elif code == 404:
                    status = "не доступен"
                elif code == 403:
                    status = "вход запрещен"
                elif code >= 500:
                    status = "ошибка сервера"
                else:
                    status = "не найден"
                result = f"{url} – {status} – {code}\n"
            except requests.exceptions.Timeout:
                result = f"{url} – не доступен(время вышло)\n"
            except requests.exceptions.ConnectionError:
                result = f"{url} – не доступен(ошибка соединения)\n"
            except requests.exceptions.RequestException as e:
                result = f"{url} – ошибка: {e}\n"
            self.txt_url_result.insert(tk.END, result)

    def setup_resources(self):
        ttk.Label(self.page_resources, text="Загрузка ресурсов системы").pack(pady=5)
        ttk.Button(self.page_resources, text="Показать загрузку CPU", command=self.show_cpu).pack(pady=2)
        ttk.Button(self.page_resources, text="Память", command=self.show_memory).pack(pady=2)
        ttk.Button(self.page_resources, text="Диск", command=self.show_disk).pack(pady=2)
        self.txt_resources = scrolledtext.ScrolledText(self.page_resources, height=20)
        self.txt_resources.pack(pady=5)

    def show_cpu(self):
        cpu = psutil.cpu_percent(interval=1)
        self.txt_resources.insert(tk.END, f"Загрузка CPU: {cpu}%\n")

    def show_memory(self):
        mem = psutil.virtual_memory()
        self.txt_resources.insert(tk.END, f"Использование памяти: {mem.percent}%\n")

    def show_disk(self):
        disk = psutil.disk_usage('/')
        self.txt_resources.insert(tk.END, f"Использование диска: {disk.percent}%\n")

    def load_courses(self):
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.courses = data['Valute']
            with open(COURSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.courses, f, ensure_ascii=False, indent=4)
        except:
            if os.path.exists(COURSES_FILE):
                with open(COURSES_FILE, 'r', encoding='utf-8') as f:
                    self.courses = json.load(f)
            else:
                self.courses = {}

    def load_groups(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    self.groups = json.load(f)
            except:
                self.groups = {}
        else:
            self.groups = {}

    def save_groups(self):
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.groups, f, ensure_ascii=False, indent=4)

    def setup_courses(self):
        frame = self.page_courses
        top_frame = ttk.Frame(frame)
        top_frame.pack(pady=5, fill='x')
        ttk.Button(top_frame, text="Обновить курсы", command=self.load_courses).pack(side='left', padx=5)
        ttk.Label(top_frame, text="Код валюты:").pack(side='left', padx=5)
        self.entry_code = ttk.Entry(top_frame, width=10)
        self.entry_code.pack(side='left', padx=5)
        ttk.Button(top_frame, text="Показать курс", command=self.show_course_by_code).pack(side='left', padx=5)
        ttk.Button(top_frame, text="Показать все валюты", command=self.show_all_courses).pack(side='left', padx=5)
        middle_frame = ttk.Frame(frame)
        middle_frame.pack(pady=5, fill='both', expand=True)
        ttk.Label(middle_frame, text="Группы валют").pack()
        self.list_groups = tk.Listbox(middle_frame)
        self.list_groups.pack(side='left', fill='y', padx=5)
        self.list_groups.bind('<<ListboxSelect>>', self.show_group_contents)
        ttk.Button(middle_frame, text="Создать группу", command=self.create_group).pack(pady=2)
        ttk.Button(middle_frame, text="Удалить группу", command=self.delete_group).pack(pady=2)
        right_frame = ttk.Frame(middle_frame)
        right_frame.pack(side='left', fill='both', expand=True, padx=10)
        ttk.Label(right_frame, text="Валюты в группе").pack()
        self.list_group_contents = tk.Listbox(right_frame)
        self.list_group_contents.pack(fill='both', expand=True)
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(pady=5)
        ttk.Label(bottom_frame, text="Код валюты:").pack(side='left', padx=5)
        self.entry_group_currency = ttk.Entry(bottom_frame, width=10)
        self.entry_group_currency.pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Добавить в группу", command=self.add_currency_to_group).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Удалить из группы", command=self.remove_currency_from_group).pack(side='left', padx=5)
        self.refresh_group_list()

    def refresh_group_list(self):
        self.list_groups.delete(0, tk.END)
        for group in self.groups:
            self.list_groups.insert(tk.END, group)

    def show_group_contents(self, event):
        selected = self.list_groups.curselection()
        if not selected:
            return
        index = selected[0]
        group_name = self.list_groups.get(index)
        self.current_group = group_name
        self.list_group_contents.delete(0, tk.END)
        for val in self.groups.get(group_name, []):
            self.list_group_contents.insert(tk.END, val)

    def create_group(self):
        name = simpledialog.askstring("Создать группу", "Введите название группы:")
        if name:
            if name in self.groups:
                messagebox.showerror("Ошибка", "Группа с таким именем уже существует")
            else:
                self.groups[name] = []
                self.save_groups()
                self.refresh_group_list()

    def delete_group(self):
        selected = self.list_groups.curselection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите группу")
            return
        index = selected[0]
        name = self.list_groups.get(index)
        if messagebox.askyesno("Удалить", f"Удалить группу '{name}'?"):
            del self.groups[name]
            self.save_groups()
            self.refresh_group_list()
            self.list_group_contents.delete(0, tk.END)

    def show_all_courses(self):
        if hasattr(self, 'txt_all_courses'):
            self.txt_all_courses.destroy()
        self.txt_all_courses = scrolledtext.ScrolledText(self, height=20)
        self.txt_all_courses.pack(pady=5, fill='both', expand=True)
        self.txt_all_courses.delete('1.0', tk.END)
        for code, info in self.courses.items():
            self.txt_all_courses.insert(tk.END, f"{info['CharCode']}: {info['Name']} - {info['Value']} руб.\n")

    def show_course_by_code(self):
        code = self.entry_code.get().upper()
        info = self.courses.get(code)
        if info:
            messagebox.showinfo("Курс валюты", f"{info['CharCode']}: {info['Name']} - {info['Value']} руб.")
        else:
            messagebox.showerror("Ошибка", "Валюта с таким кодом не найдена")

    def add_currency_to_group(self):
        code = self.entry_group_currency.get().upper()
        if code not in self.courses:
            messagebox.showerror("Ошибка", "Некорректный код валюты")
            return
        selected = self.list_groups.curselection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите группу")
            return
        index = selected[0]
        group_name = self.list_groups.get(index)
        if code in self.groups[group_name]:
            messagebox.showinfo("Инфо", "Валюта уже в группе")
        else:
            self.groups[group_name].append(code)
            self.save_groups()
            self.show_group_contents(None)

    def remove_currency_from_group(self):
        selected_group = self.list_groups.curselection()
        if not selected_group:
            messagebox.showerror("Ошибка", "Выберите группу")
            return
        index = selected_group[0]
        group_name = self.list_groups.get(index)
        selected_val = self.list_group_contents.curselection()
        if not selected_val:
            messagebox.showerror("Ошибка", "Выберите валюту для удаления")
            return
        val_index = selected_val[0]
        code = self.list_group_contents.get(val_index)
        if code in self.groups[group_name]:
            self.groups[group_name].remove(code)
            self.save_groups()
            self.show_group_contents(None)

    def setup_github(self):
        frame = self.page_github
        ttk.Label(frame, text="Работа с GitHub API").pack(pady=5)
        user_frame = ttk.Frame(frame)
        user_frame.pack(pady=5)
        ttk.Label(user_frame, text="Имя пользователя:").pack(side='left')
        self.entry_username = ttk.Entry(user_frame, width=20)
        self.entry_username.pack(side='left', padx=5)
        ttk.Button(frame, text="Показать профиль", command=self.get_github_profile).pack(pady=2)
        ttk.Button(frame, text="Список репозиториев", command=self.get_github_repos).pack(pady=2)
        ttk.Button(frame, text="Поиск по репозиториям", command=self.search_github_repos).pack(pady=2)
        self.txt_github_output = scrolledtext.ScrolledText(frame, height=20)
        self.txt_github_output.pack(pady=5, fill='both', expand=True)

    def get_github_profile(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Введите имя пользователя")
            return
        url = f'https://api.github.com/users/{username}'
        headers = {}
        if TOKEN:
            headers['Authorization'] = f'token {TOKEN}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            output = (
                f"Имя: {data.get('name')}\n"
                f"Профиль: {data.get('html_url')}\n"
                f"Публичных репозиториев: {data.get('public_repos')}\n"
                f"Гистов: {data.get('public_gists')}\n"
                f"Подписки: {data.get('following')}\n"
                f"Подписчики: {data.get('followers')}\n"
            )
            self.txt_github_output.delete('1.0', tk.END)
            self.txt_github_output.insert(tk.END, output)
        except requests.HTTPError as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении профиля: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def get_github_repos(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Введите имя пользователя")
            return
        url = f'https://api.github.com/users/{username}/repos'
        headers = {}
        if TOKEN:
            headers['Authorization'] = f'token {TOKEN}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            repos = response.json()
            self.txt_github_output.delete('1.0', tk.END)
            for repo in repos:
                self.txt_github_output.insert(tk.END, f"Название: {repo.get('name')}\n")
                self.txt_github_output.insert(tk.END, f"Ссылка: {repo.get('html_url')}\n")
                self.txt_github_output.insert(tk.END, f"Описание: {repo.get('description')}\n")
                self.txt_github_output.insert(tk.END, f"Язык: {repo.get('language')}\n")
                self.txt_github_output.insert(tk.END, f"Видимость: {'приват' if repo.get('private') else 'публичный'}\n")
                self.txt_github_output.insert(tk.END, f"Ветка: {repo.get('default_branch')}\n")
                self.txt_github_output.insert(tk.END, "-"*40 + "\n")
        except requests.HTTPError as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении репозиториев: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def search_github_repos(self):
        username = self.entry_username.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Введите имя пользователя")
            return
        poisk = simpledialog.askstring("Поиск репозиториев", "Введите название для поиска:")
        if not poisk:
            return
        url = f'https://api.github.com/search/repositories'
        headers = {}
        if TOKEN:
            headers['Authorization'] = f'token {TOKEN}'
        params = {'q': f'{poisk} user:{username}'}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            self.txt_github_output.delete('1.0', tk.END)
            for item in data.get('items', []):
                self.txt_github_output.insert(tk.END, f"Название: {item.get('name')}\n")
                self.txt_github_output.insert(tk.END, f"Ссылка: {item.get('html_url')}\n")
                self.txt_github_output.insert(tk.END, f"Описание: {item.get('description')}\n")
                self.txt_github_output.insert(tk.END, f"Владелец: {item.get('owner', {}).get('login')}\n")
                self.txt_github_output.insert(tk.END, "-"*40 + "\n")
        except requests.HTTPError as e:
            messagebox.showerror("Ошибка", f"Ошибка при поиске: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()