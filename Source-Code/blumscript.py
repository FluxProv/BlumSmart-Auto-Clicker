
import requests as req
import json
import time
import random

def make_request(url, headers, data=None, method='get', retries=3):
    for _ in range(retries):
        try:
            if method == 'post':
                response = req.post(url, headers=headers, json=data)
            else:
                response = req.get(url, headers=headers)
            response.raise_for_status()
            return response
        except req.exceptions.HTTPError as http_err:
            if response.status_code == 401:  # Unauthorized
                return "Токен истек. Пожалуйста, введите новый токен."
            elif 500 <= response.status_code < 600:  # Server error
                return f"Серверная ошибка: {response.status_code}. Повторная попытка..."
            else:
                return f"HTTP ошибка: {http_err}"
        except req.exceptions.RequestException as err:
            return f"Ошибка запроса: {err}"
    return None

def main(jwt, show_message):
    head = {
        'Authorization': 'Bearer ' + jwt,
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }

    resp = make_request('https://game-domain.blum.codes/api/v1/user/balance', headers=head)
    if not resp:
        show_message("Не удалось получить баланс. Прерывание выполнения.")
        return
    
    try:
        count = json.loads(resp.text)['playPasses']
    except KeyError:
        show_message("Не удалось получить количество игр")
        return

    total_point = 0
    if count != 0:
        show_message("Начал играть...")
        for i in range(count):
            try:
                post_id = make_request('https://game-domain.blum.codes/api/v1/game/play', headers=head, method='post')
                if not post_id:
                    show_message("Ошибка при запуске игры. Попробуйте позже.")
                    continue
                
                id = json.loads(post_id.text)['gameId']

                time.sleep(random.uniform(30, 60))

                points = random.randint(150, 250)
                endGame = make_request('https://game-domain.blum.codes/api/v1/game/claim', headers=head, data={
                    "gameId": id, "points": points}, method='post')
                if not endGame:
                    show_message("Ошибка при завершении игры. Попробуйте позже.")
                    continue
                
                show_message(f"{i + 1} / {count} игр завершено")
                time.sleep(random.uniform(1, 5))

                total_point += points
            except req.exceptions.RequestException as e:
                show_message(f"Ошибка во время игры: {e}")
                continue
    else:
        show_message("Нету кристалов для игры :(")
        return
    
    show_message(f"Всего зафармленно поинтов: {total_point}")

if __name__ == '__main__':
    jwt = input("Введите Bearer токен: ")
    main(jwt, print)
