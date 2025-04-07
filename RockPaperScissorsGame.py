import random
import time
import os

print("Добро пожаловать в игру 'Камень, Ножницы, Бумага'!")

FILE_NAME = os.path.join(os.getcwd(), "game_results.txt")
CHOICES = ["Камень", "Ножницы", "Бумага"]

def load_ratings():
    ratings = {}
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    name, wins = line.strip().split(":")
                    ratings[name] = int(wins)
                except ValueError:
                    continue
    return ratings

def save_ratings(ratings):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for name, wins in ratings.items():
                file.write(f"{name}:{wins}\n")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def get_winner(player, computer):
    if player == computer:
        return "draw"
    elif (player == "Камень" and computer == "Ножницы") or \
         (player == "Ножницы" and computer == "Бумага") or \
         (player == "Бумага" and computer == "Камень"):
        return "player"
    else:
        return "computer"

def display_ratings(ratings):
    print("\nРейтинговая таблица:")
    if not ratings:
        print("Рейтинговая таблица пока пуста.")
        return
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    for name, wins in sorted_ratings:
        print(f"{name}: {wins} побед")

def play_game(player_name, ratings):
    player_wins, computer_wins = 0, 0
    total_wins = ratings.get(player_name, 0)

    print("В этом режиме у вас есть 12 секунд на ход\nИгра проводится до 3 побед\n")
    print(f"Ваш текущий рейтинг (победы): {total_wins}")

    while player_wins < 3 and computer_wins < 3:
        print(f"\nТекущий счёт: {player_name} {player_wins} - {computer_wins} Компьютер")

        start_time = time.time()
        user_choice = input("Введите ваш выбор (Камень, Ножницы, Бумага): ").capitalize()
        elapsed_time = time.time() - start_time

        if elapsed_time > 12 or user_choice not in CHOICES:
            print("Компьютер выигрывает раунд." if elapsed_time > 12 else "Некорректный ввод. Компьютер выигрывает раунд.")
            computer_wins += 1
            continue

        computer_choice = random.choice(CHOICES)
        print(f"Компьютер выбрал: {computer_choice}")

        result = get_winner(user_choice, computer_choice)
        if result == "draw":
            print("Это ничья!\n")
        elif result == "player":
            print("Поздравляем, вы выиграли раунд!\n")
            player_wins += 1
        else:
            print("Компьютер выиграл раунд.\n")
            computer_wins += 1

    print("\nИтоговый счёт:")
    print(f"{player_name}: {player_wins}")
    print(f"Компьютер: {computer_wins}")

    if player_wins == 3:
        print("Поздравляем, вы выиграли игру!")
        ratings[player_name] = total_wins + 1
    else:
        print("Компьютер выиграл игру. Удачи в следующий раз!")

    print(f"Ваш обновлённый рейтинг (победы): {ratings.get(player_name, 0)}")
    display_ratings(ratings)

def training_mode():
    print("Вы вошли в режим тренировки. Здесь нет ограничений по времени или подсчёта побед.")
    while True:
        user_choice = input("Введите ваш выбор (Камень, Ножницы, Бумага) или 'выход' для завершения: ").capitalize()
        if user_choice.lower() == "выход":
            print("Выход из режима тренировки.")
            break
        if user_choice not in CHOICES:
            print("Некорректный ввод. Попробуйте снова.")
            continue
        computer_choice = random.choice(CHOICES)
        print(f"Компьютер выбрал: {computer_choice}")
        result = get_winner(user_choice, computer_choice)
        if result == "draw":
            print("Это ничья!")
        elif result == "player":
            print("Вы выиграли раунд!")
        else:
            print("Компьютер выиграл раунд.")

player_name = input("Введите ваше имя: ").capitalize()
ratings = load_ratings()

while True:
    mode = input("Выберите режим: 'игра', 'тренировка' или 'выход': ").lower()
    if mode == "игра":
        play_game(player_name, ratings)
        save_ratings(ratings)
    elif mode == "тренировка":
        training_mode()
    elif mode == "выход":
        print("Спасибо за игру!\n")
        print("История развития игры 'камень, ножницы, бумага':\n\n"
              "        3000 лет до н.э.                    105 год до н.э.\n"
              "       изобретение ножниц                 изобретение бумаги\n"
              "---------------|----------------------------------|-----------------\n"
              "    ничьи                 победы камня                   баланс        ")
        break
    else:
        print("Некорректный ввод. Попробуйте снова.")