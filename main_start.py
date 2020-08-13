from enemy_units import *
from witcher_unit import *
from game import *




def welcome():
    print('Вас приветствует текстовая RPG - Ведьмак')


def get_initial_values():
    witcher_level = 0
    enemy_level = 0
    enemy_amount = 0
    while witcher_level == 0:
        try:
            witcher_level = int(input('Введите уровень ведьмака: '))
            enemy_level = int(input('Введите уровень противников: '))
            enemy_amount = int(input('Введите количество противников: '))
            return witcher_level, enemy_level, enemy_amount
        except Exception:
            print('не введено требуемое значение')


def get_env_and_start(witcher_level, enemy_level, enemy_amount):
    witcher = Witcher(witcher_level)
    type_enemy = random.randint(0, 2)
    enemies = []
    if type_enemy == 0:
        for el in range(0, enemy_amount):
            drowner = Drowner(enemy_level)
            enemies.append(drowner)

    elif type_enemy == 1:
        for el in range(0, enemy_amount):
            bandit = Bandit(enemy_level)
            enemies.append(bandit)
    else:
        for el in range(0, enemy_amount):
            ghost = Ghost(enemy_level)
            enemies.append(ghost)

    beginning_game = Game(witcher, enemies)

    print(beginning_game.fight())
    print('Лог боя: ')
    for el in beginning_game.history:
        print(' ' + el)
    print(beginning_game.find_turn_log('Ход 0'))


welcome()
witcher_level, enemy_level, enemy_amount = get_initial_values()
get_env_and_start(witcher_level, enemy_level, enemy_amount)