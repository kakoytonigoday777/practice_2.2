import requests

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

def check_url(url):
    try:
        otvet = requests.get(url, timeout=10)
        code = otvet.status_code

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
        return f"{url} – {status} – {code}"

    except requests.exceptions.Timeout:
        return f"{url} – не доступен(время вышло) - {code}"
    except requests.exceptions.ConnectionError:
        return f"{url} – не доступен(ошибка соединения) - {code}"
    except requests.exceptions.RequestException as e:
        return f"{url} – ошибка: {e} - {code}"

for url in urls:
    print(check_url(url))