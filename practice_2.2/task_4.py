import requests

TOKEN = ''

headers = {}
if TOKEN:
    headers['Authorization'] = f'token {TOKEN}'

BASE_URL = 'https://api.github.com'


def get_user_profile(username):
    url = f'{BASE_URL}/users/{username}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        profile_info = {
            'name': data.get('name'),
            'profile_url': data.get('html_url'),
            'public_repos': data.get('public_repos'),
            'public_gists': data.get('public_gists'),
            'following': data.get('following'),
            'followers': data.get('followers')
        }
        return profile_info
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_user_repos(username):
    url = f'{BASE_URL}/users/{username}/repos'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json()
        repo_list = []
        for repo in repos:
            repo_info = {
                'name': repo.get('name'),
                'html_url': repo.get('html_url'),
                'watchers_count': repo.get('watchers_count'),
                'language': repo.get('language'),
                'visibility': 'public' if not repo.get('private') else 'private',
                'default_branch': repo.get('default_branch')
            }
            repo_list.append(repo_info)
        return repo_list
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def search_user_repositories(username, poisk):
    url = f'{BASE_URL}/search/repositories'
    params = {'q': f'{poisk} user:{username}'}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        repositories = []
        for item in results.get('items', []):
            repo_info = {
                'name': item.get('name'),
                'html_url': item.get('html_url'),
                'description': item.get('description'),
                'owner': item.get('owner', {}).get('login')
            }
            repositories.append(repo_info)
        return repositories
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def main():
    print("Добро пожаловать! Выберите действие:")
    print("1. Просмотр профиля пользователя")
    print("2. Получение всех репозиториев выбранного пользователя")
    print("3. Поиск репозиториев по названию")
    print("0. Выйти")

    while True:
        choice = input("Введите номер действия: ")

        if choice == '1':
            username = input("Введите имя пользователя GitHub: ")
            profile = get_user_profile(username)
            if profile:
                print("\nПрофиль пользователя:")
                for key, value in profile.items():
                    print(f'{key}: {value}')

        elif choice == '2':
            username = input("Введите имя пользователя GitHub: ")
            repos = get_user_repos(username)
            if repos:
                print("\nРепозитории пользователя:")
                for repo in repos:
                    print(f"\nНазвание: {repo['name']}")
                    print(f"Ссылка: {repo['html_url']}")
                    print(f"Просмотры: {repo['watchers_count']}")
                    print(f"Язык: {repo['language']}")
                    print(f"Видимость: {repo['visibility']}")
                    print(f"Ветка по умолчанию: {repo['default_branch']}")
            else:
                print("Репозитории не найдены")

        elif choice == '3':
            username = input("Введите имя пользователя GitHub: ")
            query = input("Введите название репозитория для поиска: ")
            results = search_user_repositories(username, query)
            if results:
                print("\nРезультаты поиска:")
                for repo in results:
                    print(f"\nНазвание: {repo['name']}")
                    print(f"Ссылка: {repo['html_url']}")
                    print(f"Описание: {repo['description']}")
                    print(f"Владелец: {repo['owner']}")
            else:
                print("Репозитории не найдены")

        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("Неправильный выбор, попробуйте снова")


if __name__ == '__main__':
    main()