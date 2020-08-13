import random
from witcher_unit import *
from base_units import *
from enemy_units import *


class Game:
    def __init__(self, witcher: Witcher, enemies: list, history: list = []):
        self.witcher = witcher
        self.enemies = enemies
        self.turn = 0
        self.history = history

    def enemies_is_alive(self) -> bool:
        return len(self.enemies) > 0

    def get_damage_to_enemies(self, inf: list) -> PlayerAction:
        result: tuple = self.witcher.next_move(self.history, self.turn, inf)

        for enemy in self.enemies:
            enemy.block = False

        for enemy in self.enemies:
            enemy.next_action(result[0], result[1], self.turn, self.witcher, self.history, self.enemies)

        return result[0]

    def get_damage_to_witcher(self, result: PlayerAction) -> None:
        attacker = None
        accuracy = self.enemies[0].accuracy

        if result == PlayerAction.axiy:
            attacker = random.choice(self.enemies)
            attacker_position = self.enemies.index(attacker)

            if len(self.enemies) > 1:
                defender = random.choice(self.enemies[:attacker_position] + self.enemies[attacker_position+1:])

                if random.random() > accuracy:
                    print('Ход {0}. Противник номер {1} промахнулся по противнику номер {2} под действием Аксия'
                                                   .format(self.turn, self.enemies.index(attacker),
                                                                                      self.enemies.index(defender)))
                    self.history.append('Ход {0}. Противник номер {1} промахнулся по противнику номер {2} под действием Аксия'
                                                                            .format(self.turn, self.enemies.index(attacker),
                                                                                              self.enemies.index(defender)))

                else:
                    k = 1.0

                    if isinstance(defender, Ghost) and defender.in_astral:
                        k = 0.2
                        print('Призрак ушел в астрал под Аксием')

                    if random.random() < attacker.crit:
                        k *= 2
                        print('Аттакер кританул')

                    damage = attacker.attack_power * k
                    defender.hp -= damage
                    print('Ход {0}. Противник номер {1} попал по противнику номер {2} по действием знака Аксий и нанес '
                      '{3} урона'.format(self.turn, self.enemies.index(attacker), self.enemies.index(defender), damage))
                    self.history.append('Ход {0}. Противник номер {1} попал по противнику номер {2} по действием знака Аксий и нанес '
                      '{3} урона'.format(self.turn, self.enemies.index(attacker), self.enemies.index(defender), damage))

        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            if enemy == attacker:
                print('Противник номер {0} находится под действием аксия'.format(i))
                self.history.append('Противник номер {0} находится под действием аксия'.format(i))
                continue

            count = 0

            if isinstance(enemy, Drowner) or isinstance(enemy, Bandit):
                if result == PlayerAction.dodge:
                    actual_accuracy = enemy.accuracy / 3

                else:
                    actual_accuracy = enemy.accuracy

                if isinstance(enemy, Bandit) and (enemy.dodge or enemy.block):
                    continue

                for _ in range(enemy.attack_speed):
                    if count == 1 and isinstance(enemy, Bandit):
                        damage = enemy.attack_power / 3

                    else:
                        damage = enemy.attack_power

                    if random.random() < actual_accuracy:
                        if random.random() < enemy.crit:
                            damage = damage*2
                            print('Ход {0}. Противник номер {1} кританул по Ведьмаку'.format(self.turn, i))
                            self.history.append('Ход {0}. Противник номер {1} кританул по Ведьмаку'.format(self.turn, i))

                        if self.witcher.shield > 0:
                            if damage > self.witcher.shield:
                                diff_damage = damage - self.witcher.shield
                                diff_shield = damage - diff_damage
                                self.witcher.shield = self.witcher.shield - diff_shield
                                print('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'.format(
                                    self.turn, i, int(diff_shield)))
                                self.history.append('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'
                                                                                .format(self.turn, i, int(diff_shield)))
                                self.witcher.hp = self.witcher.hp - diff_damage
                                print('Ход {0}. Противник номер {1} пробил щит и нанес Ведьмаку {2} урона'.format(
                                    self.turn, i, diff_damage))
                                self.history.append('Ход {0}. Противник номер {1} пробил щит и нанес Ведьмаку {2} урона'
                                                                                .format(self.turn, i, int(diff_damage)))

                            else:
                                self.witcher.shield = self.witcher.shield - damage
                                print('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'.format(
                                    self.turn, i, damage))
                                self.history.append('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'
                                                                                     .format(self.turn, i, int(damage)))

                        else:
                            if damage == enemy.attack_power*2 or damage == (enemy.attack_power/3) * 2:
                                self.witcher.hp = self.witcher.hp - damage
                                print('Ход {0}. Противник номер {1} нанес критический урон {2} по Ведьмаку'.format(
                                    self.turn, i, int(damage)))
                                self.history.append(
                                    'Ход {0}. Противник номер {1} нанес критический урон {2} по Ведьмаку'.format(
                                        self.turn, i, int(damage)))

                            else:
                                self.witcher.hp = self.witcher.hp - damage
                                print(
                                    'Ход {0}. Противник номер {1} попал по Ведьмаку и нанес {2} урона '.format(
                                                                                             self.turn, i, int(damage)))
                                self.history.append(
                                    'Ход {0}. Противник номер {1} попал по Ведьмаку и нанес {2} урона '.format(
                                                                                             self.turn, i, int(damage)))

                    else:
                        print('Ход {0}. Противник номер {1} промахнулся по ведьмаку'.format(self.turn, i))
                        self.history.append(
                            'Ход {0}. Противник номер {1} промахнулся по ведьмаку.HP ведьмака {2}'.format(self.turn, i,
                                                                                                       self.witcher.hp))
                    count += 1
            else:
                if result == PlayerAction.dodge:
                    actual_accuracy = enemy.accuracy / 3

                else:
                    actual_accuracy = enemy.accuracy

                if random.random() < actual_accuracy:
                    damage = enemy.attack_power

                    if random.random() < enemy.crit:
                        damage = enemy.attack_power * 2
                        print('Ход {0}. Противник номер {1} кританул по Ведьмаку'.format(self.turn, i))
                        self.history.append('Ход {0}. Противник номер {1} кританул по Ведьмаку'.format(self.turn, i))

                    if self.witcher.shield > 0:
                        if damage > self.witcher.shield:
                            diff_damage = damage - self.witcher.shield
                            diff_shield = damage - diff_damage
                            self.witcher.shield = self.witcher.shield - diff_shield
                            print('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'.format(self.turn,
                                                                                                   i, int(diff_shield)))
                            self.history.append('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'
                                                                                     .format(self.turn, i, diff_shield))
                            self.witcher.hp = self.witcher.hp - diff_damage
                            print('Ход {0}. Противник номер {1} пробил щит и нанес Ведьмаку {2} урона'.format(self.turn,
                                                                                                   i, int(diff_damage)))
                            self.history.append('Ход {0}. Противник номер {1} пробил щит и нанес Ведьмаку {2} урона'
                                                                                .format(self.turn, i, int(diff_damage)))

                        else:
                            self.witcher.shield = self.witcher.shield - damage
                            print('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'.format(self.turn,
                                                                                                        i, int(damage)))
                            self.history.append('Ход {0}. Противник номер {1} попал по щиту. Щит поглотил {2} урона'
                                                                                     .format(self.turn, i, int(damage)))

                    else:
                        if damage > enemy.attack_power:
                            self.witcher.hp = self.witcher.hp - damage
                            print(
                                'Ход {0}. Противник номер {1} нанес критический урон {2} по Ведьмаку'.format(self.turn,
                                                                                                        i, int(damage)))
                            self.history.append(
                                'Ход {0}. Противник номер {1} нанес критический урон {2} по Ведьмаку'.format(self.turn,
                                                                                                        i, int(damage)))
                        else:
                            self.witcher.hp = self.witcher.hp - damage
                            print(
                                'Ход {0}. Противник номер {1} попал по Ведьмаку и нанес {2} урона '.format(self.turn,
                                                                                                        i, int(damage)))
                            self.history.append(
                                'Ход {0}. Противник номер {1} попал по Ведьмаку и нанес {2} урона '.format(self.turn,
                                                                                                        i, int(damage)))
                else:
                    print('Ход {0}.Противник номер {1} промахнулся по ведьмаку'.format(self.turn, i))
                    self.history.append(
                        'Ход {0}.Противник номер {1} промахнулся по ведьмаку.HP ведьмака {2}'.format(self.turn, i,
                                                                                                     self.witcher.hp))

    def fight(self) -> str:
        while True:
            inf: list = []
            inf = list(map(lambda enemy: enemy.get_fullname(), self.enemies))
            result = self.get_damage_to_enemies(inf)

            for enemy in self.enemies:
                if enemy.hp <= 0:
                    Unit.update_amount_of_alive(False)

            self.enemies: list = list(filter(lambda x: x.hp > 0, self.enemies))
            if not self.enemies_is_alive():
                break

            self.get_damage_to_witcher(result)

            if self.witcher.hp <= 0:
                Unit.update_amount_of_alive(False)
                break

            self.turn += 1

        if self.witcher.hp <= 0:
            self.history.append('Поражение. Ведьмак мертв')
            self.store_history()

            return 'Ведьмак мертв, ты проиграл'
        else:
            self.history.append('Победа. Все враги повержены')
            self.store_history()

            return 'Все враги мертвы, Ведьмак победил'

    def store_history(self) -> None:
        with open('game_log.txt', 'w', encoding='utf-8') as f:
            for el in self.history:
                f.write(el + '\n')

    def find_turn_log(self, n: str) -> list:
        result = list(filter(lambda x: x.find(n) != -1, self.history))

        return result