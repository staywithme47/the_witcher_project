from base_units import Unit
from enum import Enum
from functools import reduce


class Potions(Enum):
    swallow = 1
    thunder = 2
    tawny_owl = 3


class PlayerAction(Enum):
    attack = 1
    power_attack = 2
    dodge = 3
    igni = 8
    kven = 9
    axiy = 10


class Witcher(Unit):
    def __init__(self, level:int):
        Unit.__init__(self, level)
        self.attack_power = 30 * level
        self.accuracy = 0.95
        self.hp = 400 * level
        self.potions = {Potions.swallow: 2, Potions.thunder: 2, Potions.tawny_owl:1}
        self.last_turn_potions_used = {Potions.swallow: -1, Potions.thunder: -1,Potions.tawny_owl:-1}
        self.last_turn_power_attack = -1
        self.max_hp = self.hp
        self.threshold_hp = self.max_hp * 0.3
        self.energy = 100
        self.max_energy = self.energy
        self.shield = 0
        self.crit = 0.16

    def get_fullname(self) -> str:
        return 'Ведьмак {0}й ур, {1}%, {2}хп, {3} сила атаки, {4} текущий щит, {5} текущий уровень энергии. {6}'.format(self.level, self.accuracy, self.hp,
                                                                       self.attack_power, self.shield, self.energy,
                                                                       'кол-во зелий Ласточка: {0}, кол-во зелий Гром: {1}, кол-во зелий Неясыть: {2}'.format(
                                                                           self.potions[Potions.swallow],
                                                                           self.potions[Potions.thunder],self.potions[Potions.tawny_owl]))

    def next_move(self, history: list, turn: int, enemies_info: list) -> tuple:
        print(reduce(lambda x, y: str(x) + '\n' + str(y), enemies_info))
        while True:
            print('номер хода: ' + str(turn))
            try:
                player_action = int(
                    input('выберите действие (7 для инфы):  '))
                if player_action == 1:
                    playerAction = PlayerAction.attack
                    if self.last_turn_potions_used[Potions.thunder] != -1 and turn - self.last_turn_potions_used[
                        Potions.thunder] <= 5:
                        damage = self.attack_power * 1.5
                        history.append(
                            'Ход {0} Ведьмак использовал быструю атаку. HP ведьмака {1}'.format(turn, self.hp))
                    else:
                        damage = self.attack_power
                    break
                if player_action == 2:
                    playerAction = PlayerAction.power_attack
                    if self.last_turn_power_attack == -1 or turn - self.last_turn_power_attack >= 3:
                        self.last_turn_power_attack = turn
                        if self.last_turn_potions_used[Potions.thunder] != -1 and turn - self.last_turn_potions_used[
                            Potions.thunder] < 5:
                            damage = self.attack_power * 2 * 1.5
                            history.append('Ведьмак использовал силовую атаку. HP ведьмака {0}'.format(self.hp))
                        else:
                            damage = self.attack_power * 2
                        break
                    else:
                        print('Вы не можете провести силовую атаку, введите действие еще раз')

                if player_action == 3:
                    playerAction = PlayerAction.dodge
                    damage = 0
                    history.append('Ведьмак использовал уклонение {0}, HP ведьмака {1}'.format(turn, self.hp))
                    break

                if player_action == 4:
                    if self.potions[Potions.thunder] != 0:
                        self.potions[Potions.thunder] -= 1
                        self.last_turn_potions_used[Potions.thunder] = turn

                        history.append('{0}, {1}, использован Гром'.format(turn, self.hp))
                    else:
                        print('У вас нет зелья Гром. Введите действие еще раз')

                if player_action == 5:
                    if self.potions[Potions.swallow] != 0:
                        self.potions[Potions.swallow] -= 1
                        self.last_turn_potions_used[Potions.swallow] = turn
                        history.append('{0}, {1}, использована Ласточка'.format(turn, self.hp))
                    else:
                        print('У вас нет зелья Ласточка. Введите действие еще раз')

                if player_action == 6:
                    print(self.get_fullname())

                    if self.last_turn_potions_used[Potions.swallow] != -1 and turn - self.last_turn_potions_used[
                        Potions.swallow] < 5:
                        print('Ласточка действует.', 'Осталось:',
                              5 - abs(self.last_turn_potions_used[Potions.swallow] - turn), 'ходов')

                    if self.last_turn_potions_used[Potions.thunder] != -1 and turn - self.last_turn_potions_used[
                        Potions.thunder] < 5:
                        print('Гром действует. Осталось: ',
                              5 - abs(self.last_turn_potions_used[Potions.swallow] - turn), 'ходов')

                    if self.last_turn_power_attack != -1 and turn - self.last_turn_power_attack < 3:
                        print('Силовая атака была использована: ', abs(self.last_turn_power_attack - turn),
                              'ходов назад')
                    else:
                        print('Силовая атака доступна')

                    if self.last_turn_potions_used[Potions.tawny_owl]!= -1 and turn - self.last_turn_potions_used[
                        Potions.tawny_owl]<5:
                        print('Неясыть действует. Осталось: {} ходов'.format(5-abs(self.last_turn_potions_used[
                                                                                       Potions.tawny_owl] - turn)))

                if player_action == 7:
                    print(
                        'Cписок доступных действий: ' + '\n 1 - Быстрая атака' + '\n 2 - Силовая атака' + '\n 3 - Уклониться'
                        + '\n 4 - Выпить Гром' + '\n 5 - Выпить Ласточку' + '\n 6 - Вывести текущее состояние ведьмака' +
                        '\n 8 - Использовать Игни' +'\n 9 - Использовать Квен' + '\n10 - Использовать Аксий' +
                        '\n11 - Использовать Неясыть')

                if player_action == 8:
                    playerAction = PlayerAction.igni
                    if self.energy == 100:
                        damage: int = 0
                        self.energy -= 85
                        history.append('Ход {0}.Использован Игни. ХП Ведьмака {1}'.format(turn, self.hp))
                        break
                    else:
                        print('недостаточно энергии на использование знака')

                if player_action == 9:
                    playerAction = PlayerAction.kven
                    if self.energy == 100:
                        self.energy -= 70
                        self.shield = 60 * self.level
                        damage = 0
                        history.append(
                        '{0}, {1}, использован Квен. {2} Щит от Квена'.format(turn, self.hp, self.shield))
                        break
                    else:
                        print('недостаточно энергии на использование знака')

                if player_action == 10:
                    playerAction = PlayerAction.axiy
                    if self.energy == 100:
                        damage = 0
                        self.energy -= 90
                        history.append('Ход {0}.Использован Аксий. ХП Ведьмака {1}'.format(turn, self.hp))
                        break
                    else:
                        print('недостаточно энергии на использование знака')

                if player_action == 11:
                    if self.potions[Potions.tawny_owl]!= 0:
                        self.potions[Potions.tawny_owl]-=1
                        self.last_turn_potions_used[Potions.tawny_owl] = turn
                        history.append('{0}, {1}, использована Неясыть'.format(turn, self.hp))
                    else:
                        print('У вас нет зелья Неясыть. Введите действие еще раз')
            except ValueError:
                print('Вы ввели неверную команду. Введите число от 1 до 7')

        if self.last_turn_potions_used[Potions.swallow] != -1 and turn - self.last_turn_potions_used[
            Potions.swallow] < 5:
            previous_hp = self.hp
            self.hp = self.hp + (20 * self.level)
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            history.append('Ход {0}.ласточка захилила +{1} хп'.format(turn, abs(previous_hp - self.hp)))
            print('Ход {0}.ласточка захилила +{1} хп'.format(turn, abs(previous_hp - self.hp)))

        if self.last_turn_potions_used[Potions.tawny_owl]!=-1 and turn-self.last_turn_potions_used[Potions.tawny_owl] < 5:
                previous_energy = self.energy
                self.energy = self.energy + (20 * 1.5)
                if self.energy > self.max_energy:
                    self.energy = self.max_energy
                history.append('Ход {0}. Неясыть восстановила +{1} энергии'.format(turn, abs(previous_energy - self.energy)))
                print('Ход {0}. Неясыть восстановила +{1} энергии'.format(turn,abs(previous_energy - self.energy)))

        else:

            if self.energy < self.max_energy:
                self.energy += 20

            if self.energy > self.max_energy:
                self.energy = self.max_energy

        return playerAction, damage

    def witcher_shield_damage(self, damage, turn, history, critical_hit):
        if self.shield > 0:
            if damage > self.shield:
                diff_damage = damage - self.shield
                diff_shield = damage - diff_damage
                self.shield = self.shield - diff_shield
                print('Ход {0}. Противник попал по щиту. Щит поглотил {1} урона'.format(
                    turn, int(diff_shield)))
                history.append('Ход {0}. Противник попал по щиту. Щит поглотил {1} урона'
                               .format(turn, int(diff_shield)))
                self.hp = self.hp - diff_damage
                print('Ход {0}. Противник пробил щит и нанес Ведьмаку {1} урона'.format(
                    turn, diff_damage))
                history.append('Ход {0}. Противник пробил щит и нанес Ведьмаку {1} урона'
                               .format(turn, int(diff_damage)))

            else:
                self.shield = self.shield - damage
                print('Ход {0}. Противник попал по щиту. Щит поглотил {1} урона'.format(
                    turn, damage))
                history.append('Ход {0}. Противник попал по щиту. Щит поглотил {1} урона'
                               .format(turn, int(damage)))

        else:
            if critical_hit:
                self.hp = self.hp - damage
                print('Ход {0}. Противник нанес критический урон {1} по Ведьмаку'.format(turn, int(damage)))
                history.append(
                    'Ход {0}. Противник нанес критический урон {1} по Ведьмаку'.format(turn, int(damage)))

            else:
                self.hp = self.hp - damage
                print(
                    'Ход {0}. Противник попал по Ведьмаку и нанес {1} урона '.format(
                        turn, int(damage)))
                history.append(
                    'Ход {0}. Противник попал по Ведьмаку и нанес {1} урона '.format(turn, int(damage)))