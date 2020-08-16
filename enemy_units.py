from base_units import Unit
from witcher_unit import *
import random


class Bandit(Unit):
    def __init__(self, level):
        Unit.__init__(self, level)
        self.attack_power = 25 * level
        self.accuracy = 0.85
        self.hp = 150 * level
        self.crit = 0.13
        self.attack_speed = 1
        self.ability = 3
        self.dodge = False
        self.special_ability = 1
        self.max_hp = self.hp
        self.threshold_hp = self.max_hp * 0.3
        self.cry_chance = 0.85
        self.crying = False
        self.block = False

    def get_fullname(self):
        return '{0} {1}й ур {2}% {3}хп {4} сила атаки'.format('Бандит', self.level, self.accuracy, self.hp,
                                                              self.attack_power)

    def check_crossbow_hit(self, result, turn, witcher, history):
        self.attack_speed = 1
        if self.ability > 0 and (result == PlayerAction.igni or result == PlayerAction.kven):
            self.attack_speed = 2
            self.ability -= 1
            print('abils left', self.ability)
            print('Ход {0}. Бандит использовал способность "выстрел из арбалета"'.format(turn))
            history.append('Ход {0}. Бандит использовал способность "выстрел из арбалета"'.format(turn))

        elif self.ability == 0 and (result == PlayerAction.igni or result == PlayerAction.kven):
            print('Ход {0}. Бандит не смог использовать способность "выстрел из арбалета"'.format(turn))
            history.append('Ход {0}. Бандит не смог использовать способность "выстрел из арбалета"'.format(turn))

    def check_dodge(self, result, turn, witcher, history):
        self.dodge = False
        self.attack_power = 25 * self.level

        if result == PlayerAction.power_attack:
            self.dodge = True
            print('Ход {}. Бандит использовал способность "Уклонение", снизив точность Ведьмака в 2 раза'.format(turn))
            history.append('Ход {}. Бандит использовал способность "Уклонение", снизив точность Ведьмака в 2 раза'.format(turn))

    def check_cry(self, turn, history):
        self.crying = False
        if self.hp < self.threshold_hp and not self.block:
            if self.special_ability == 1:
                self.crying = True
                self.special_ability -= 1
                print('Ход {0}. Бандит использовал способность Боевой клич'.format(turn))
                history.append('Ход {0}. Бандит использовал способность Боевой клич'.format(turn))

            else:
                print('Ход {0}. Бандит не смог использовать способность Боевой клич'.format(turn))
                history.append('Ход {0}. Бандит не смог использовать способность Боевой клич'.format(turn))

    def check_protector(self, turn, history):
        if not self.crying:
            if random.random() < self.cry_chance:
                self.block = True
                print('Ход {0}. Бандит откликнулся на боевой клич и заблокировал урон врага'.format(turn))
                history.append('Ход {0}. Бандит откликнулся на боевой клич и заблокировал урон врага'.format(turn))

            else:
                print('Ход {0}. Бандит откликнулся, но попал впросак'.format(turn))
                history.append('Ход {0}. Бандит откликнулся, но попал впросак'.format(turn))

    def witcher_to_enemies(self, result, damage, turn, witcher, history, enemies):
        if result == PlayerAction.igni:
            damage = 25 * witcher.level
            self.hp -= damage
            print('Ход {0}. Ведьмак нанес {1} урона Бандиту знаком Игни'.format(turn, damage))
            history.append('Ход {0}. Ведьмак нанес {1} урона Бандиту знаком Игни'.format(turn, damage))

        elif result == PlayerAction.attack or result == PlayerAction.power_attack:
            if self.dodge:
                actual_witcher_accuracy = witcher.accuracy / 2

            else:
                actual_witcher_accuracy = 0.95

            if random.random() < actual_witcher_accuracy:
                if random.random() < witcher.crit:
                    print('Ход {0}. Ведьмак нанес критический удар по Бандиту'.format(turn))
                    history.append('Ход {0}. Ведьмак нанес критический удар по Бандиту'.format(turn))
                    damage = damage * 2

                self.hp -= damage
                print('Ход {0}. Ведьмак нанес {1} урона по Бандиту'.format(turn, damage))
                history.append('Ход {0}. Ведьмак нанес {1} урона по Бандиту'.format(turn, damage))

            else:
                print('Ход {0}. Ведьмак промахнулся по Бандиту'.format(turn))
                history.append('Ход {0}. Ведьмак промахнулся по Бандиту'.format(turn))

    def next_action(self, result, damage, turn, witcher, history, enemies):
        self.crying = False
        self.attack_speed = 1
        self.check_crossbow_hit(result, turn, witcher, history)
        self.dodge = False
        self.check_dodge(result, turn, witcher, history)
        if result != PlayerAction.dodge and result != PlayerAction.kven and result != PlayerAction.axiy:
            self.check_cry(turn, history)

        alive_blockers = False

        if self.crying:
            for enemy in enemies:
                if not enemy.crying and not enemy.block and enemy.hp > 0:
                    alive_blockers = True
                    protector = enemy
                    protector.check_protector(turn, history)

                    if protector.block:
                        if result == PlayerAction.igni:
                            prot_damage = 3.57 * witcher.level
                            protector.hp -= prot_damage
                            print(
                         'Ход {0}. Откликнувшийся получил {1} урона под действием способности Боевой клич от знака Игни'
                                                                                            .format(turn, prot_damage))
                            history.append('Ход {0}. Откликнувшийся получил {1} урона под действием способности Боевой клич от знака Игни'
                                                                                            .format(turn, prot_damage))

                        elif result == PlayerAction.attack or result == PlayerAction.power_attack:
                            if random.random() < witcher.accuracy:
                                if random.random() < witcher.crit:
                                    print('Ход {0}. Ведьмак нанес критический удар по откликнувшемуся'.format(turn))
                                    history.append('Ход {0}. Ведьмак нанес критический удар по откликнувшемуся'
                                                                                                          .format(turn))
                                    prot_damage = (damage * 2) / 7

                                else:
                                    prot_damage = damage / 7

                                protector.hp -= prot_damage
                                print('Ход {0}. Ведьмак нанес {1} урона по откликнувшемуся'.format(turn, prot_damage))
                                history.append('Ход {0}. Ведьмак нанес {1} урона по откликнувшемуся'
                                                                                             .format(turn, prot_damage))

                            else:
                                print('Ход {0}. Ведьмак промахнулся по откликнувшемуся'.format(turn))
                                history.append('Ход {0}. Ведьмак промахнулся по откликнувшемуся'.format(turn))

                            print('Ход {0}. Бандит не получил урона под действием способности Боевой клич'.format(turn))
                            history.append('Ход {0}. Бандит не получил урона под действием способности Боевой клич'
                                                                                                         .format(turn))

                    else:
                        if result == PlayerAction.igni:
                            prot_damage = 25 * witcher.level
                            self.hp -= prot_damage
                            print(
                            'Ход {0}. Бандит получил {1} урона под действием способности Боевой клич'.format(
                                                                                                     turn, prot_damage))
                            history.append('Ход {0}. Бандит получил {1} урона под действием способности Боевой клич'
                                                                                             .format(turn, prot_damage))

                        elif result == PlayerAction.attack or result == PlayerAction.power_attack:
                            if self.dodge:
                                actual_accuracy = witcher.accuracy / 2

                            else:
                                actual_accuracy = witcher.accuracy

                            if random.random() < actual_accuracy:
                                if random.random() < witcher.crit:
                                    print('Ход {0}. Ведьмак нанес критический удар по кричавшему'.format(turn))
                                    history.append('Ход {0}. Ведьмак нанес критический удар по кричавшему'.format(turn))
                                    prot_damage = damage * 2

                                else:
                                    prot_damage = damage

                                self.hp -= prot_damage
                                print(
                                'Ход {0}. Ведьмак нанес {1} урона по кричавшему'.format(turn, prot_damage))
                                history.append('Ход {0}. Ведьмак нанес {1} урона по кричавшему'.format(turn, prot_damage))

                            else:
                                print('Ход {0}. Ведьмак промахнулся по кричавшему'.format(turn))
                                history.append('Ход {0}. Ведьмак промахнулся по кричавшему'.format(turn))
                    break

            if not alive_blockers:
                print('Ход {0}. Не осталось Бандитов способных откликнуться'.format(turn))
                history.append('Ход {0}. Не осталось Бандитов способных откликнуться'.format(turn))
                if self.crying:
                    self.witcher_to_enemies(result, damage, turn, witcher, history, enemies)

        if not self.crying or result == PlayerAction.dodge:
            self.witcher_to_enemies(result, damage, turn, witcher, history, enemies)

    def deal_damage_to_witcher(self, result, witcher, turn, history):
        if result == PlayerAction.dodge:
            actual_accuracy = self.accuracy / 3

        else:
            actual_accuracy = self.accuracy

        if not self.dodge or not self.block:

            for i in range(self.attack_speed):
                if i == 1:
                    damage = self.attack_power / 3

                else:
                    damage = self.attack_power

                critical_hit = False
                if random.random() < actual_accuracy:
                    if random.random() < self.crit:
                        critical_hit = True
                        damage = damage * 2
                        print('Ход {0}. Противник кританул по Ведьмаку'.format(turn))
                        history.append('Ход {0}. Противник кританул по Ведьмаку'.format(turn))

                    witcher.witcher_main_damage(damage, turn, history, critical_hit)

                else:
                    print('Ход {0}. Противник промахнулся по Ведьмаку'.format(turn))

class Ghost(Unit):
    def __init__(self, level):
        Unit.__init__(self, level)
        self.attack_power = 40 * level
        self.accuracy = 0.65
        self.hp = 300 * level
        self.crit = 0.08
        self.last_turn_ability_used = -1
        self.ability = 4
        self.max_hp = self.hp
        self.threshold_hp = self.max_hp * 0.3
        self.in_astral = False

    def get_fullname(self):
        return '{0} {1}й ур {2}% {3}хп {4} сила атаки'.format('Призрак', self.level, self.accuracy, self.hp,
                                                              self.attack_power)

    def check_astral(self, result, witcher, turn, history):
        self.in_astral = False
        if (self.last_turn_ability_used == -1 or turn - self.last_turn_ability_used > 1) and self.ability > 0:
            if (result == PlayerAction.power_attack) or ((witcher.last_turn_potions_used[Potions.thunder] != -1
                                                      and turn - witcher.last_turn_potions_used[Potions.thunder] < 5) or
            self.hp < self.threshold_hp):
                self.last_turn_ability_used = turn
                self.ability -= 1
                self.in_astral = True
                print('Ghost in astral', self.in_astral)
                history.append('Ход {}. Призрак ушел в Астрал'.format(turn))

    def next_action(self, result, damage, turn, witcher, history, enemies):
        self.check_astral(result, witcher, turn, history)
        k = 1.0

        if self.in_astral:
            k = 0.2

        if result == PlayerAction.igni:
            damage = (25 * witcher.level) * k
            self.hp -= damage
            print('Ход {0}. Ведьмак нанес {1} урона призраку знаком Игни'. format(turn, damage))
            history.append('Ход {0}. Ведьмак нанес {1} урона призраку знаком Игни'. format(turn, damage))

        elif result == PlayerAction.attack or result == PlayerAction.power_attack:
            if random.random() < witcher.accuracy:
                if random.random() < witcher.crit:
                    print('Ход {0}. Ведьмак нанес критический удар по призраку'.format(turn))
                    history.append('Ход {0}. Ведьмак нанес критический удар по призраку'.format(turn))
                    damage = (damage*2) * k

                else:
                    damage = k*damage

                self.hp -= damage
                print('Ход {0}. Ведьмак нанес {1} урона по Призраку'.format(turn, damage))
                history.append('Ход {0}. Ведьмак нанес {1} урона по Призраку'.format(turn, damage))

            else:
                print('Ход {0}. Ведьмак промахнулся по Призраку'.format(turn))
                history.append('Ход {0}. Ведьмак промахнулся по Призраку'.format(turn))

    def deal_damage_to_witcher(self, result, witcher, turn, history):
        if result == PlayerAction.dodge:
            actual_accuracy = self.accuracy / 3

        else:
            actual_accuracy = self.accuracy

        critical_hit = False
        damage = self.attack_power
        if random.random() < actual_accuracy:
            if random.random() < self.crit:
                critical_hit = True
                damage = damage * 2
                print('Ход {0}. Противник кританул по Ведьмаку'.format(turn))
                history.append('Ход {0}. Противник кританул по Ведьмаку'.format(turn))

            witcher.witcher_main_damage(damage, turn, history, critical_hit)
        else:
            print('Ход {0}. Противник промахнулся по Ведьмаку'.format(turn))

class Drowner(Unit):
    def __init__(self, level):
        Unit.__init__(self, level)
        self.attack_power = 50 * level
        self.accuracy = 0.55
        self.hp = 200 * level
        self.crit = 0.10
        self.ability = 3
        self.in_rage = False
        self.attack_speed = 1

    def get_fullname(self):
        return '{0} {1}й ур {2}% {3}хп {4} сила атаки'.format('Утопец', self.level, self.accuracy, self.hp,
                                                              self.attack_power)

    def in_fury(self, turn, witcher, result):
        self.in_rage = False

        if self.ability > 0 and result != PlayerAction.dodge and (result == PlayerAction.igni or witcher.hp < witcher.threshold_hp or witcher.shield > 0):
            self.ability -= 1
            self.in_rage = True

    def next_action(self, result, damage, turn, witcher, history, enemies):
        self.attack_speed = 1
        self.in_fury(turn, witcher, result)

        if result == PlayerAction.igni:
            damage = 25 * witcher.level
            self.hp = self.hp - damage
            print('Ход {0}.Ведьмак нанес Утопцу {1} урона знаком Игни'.format(turn, damage))
            history.append('Ход {0}.Ведьмак нанес Утопцу {1} урона знаком Игни'.format(turn, damage))

            if self.in_rage:
                self.attack_speed = 2
                print('Ход {0}. Утопец использовал способность Ярость'.format(turn))
                history.append('Ход {0}. Утопец использовал способность Ярость'.format(turn))
            else:
                self.attack_speed = 1
                print('Ход {0}. Утопец не смог использовать способность Ярость'.format(turn))
                history.append('Ход {0}. Утопец не смог использовать способность Ярость'.format(turn))

        elif result == PlayerAction.kven:

            if self.in_rage:
                self.attack_speed = 2
                print('Ход {0}. Утопец использовал способность Ярость'.format(turn))
                history.append('Ход {0}. Утопец использовал способность Ярость'.format(turn))
            else:
                self.attack_speed = 1
                print('Ход {0}. Утопец не смог использовать способность Ярость'.format(turn))
                history.append('Ход {0}. Утопец не смог использовать способность Ярость'.format(turn))

        elif result == PlayerAction.dodge:
            self.attack_speed = 1

        elif witcher.hp < witcher.threshold_hp or witcher.shield > 0:
            if self.in_rage:
                self.attack_speed = 2
                print('Ход {0}. Утопец использовал способность Ярость'.format(turn))
                history.append('Ход {0}. Утопец использовал способность Ярость'.format(turn))

            else:
                self.attack_speed = 1
                print('Ход {0}. Утопец не смог использовать способность Ярость'.format(turn))
                history.append('Ход {0}. Утопец не смог использовать способность Ярость'.format(turn))

            if (result != PlayerAction.kven or result != PlayerAction.axiy) and damage != 0:
                if random.random() < witcher.accuracy:
                    if random.random() < witcher.crit:
                        print('Ход {0}. Ведьмак нанес критический удар по Утопцу'.format(turn))
                        history.append('Ход {0}. Ведьмак нанес критический удар по Утопцу'.format(turn))
                        damage = (damage * 2)

                    self.hp -= damage
                    print('Ход {0}. Ведьмак нанес {1} урона по Утопцу'.format(turn, damage))
                    history.append('Ход {0}. Ведьмак нанес {1} урона по Утопцу'.format(turn, damage))

                else:
                    print('Ход {0}. Ведьмак промахнулся по Утопцу'.format(turn))
                    history.append('Ход {0}. Ведьмак промахнулся по Утопцу'.format(turn))

        elif result == PlayerAction.attack or result == PlayerAction.power_attack:
            if random.random() < witcher.accuracy:
                if random.random() < witcher.crit:
                    print('Ход {0}. Ведьмак нанес критический удар по Утопцу'.format(turn))
                    history.append('Ход {0}. Ведьмак нанес критический удар по Утопцу'.format(turn))
                    damage = (damage * 2)

                self.hp -= damage
                print('Ход {0}. Ведьмак нанес {1} урона по Утопцу'.format(turn, damage))
                history.append('Ход {0}. Ведьмак нанес {1} урона по Утопцу'.format(turn, damage))

            else:
                print('Ход {0}. Ведьмак промахнулся по Утопцу'.format(turn))
                history.append('Ход {0}. Ведьмак промахнулся по Утопцу'.format(turn))

    def deal_damage_to_witcher(self, result, witcher, turn, history):
        if result == PlayerAction.dodge:
            actual_accuracy = self.accuracy / 3

        else:
            actual_accuracy = self.accuracy

        critical_hit = False
        for _ in range(self.attack_speed):
            damage = self.attack_power

            if random.random() < actual_accuracy:
                if random.random() < self.crit:
                    critical_hit = True
                    damage = damage * 2
                    print('Ход {0}. Противник кританул по Ведьмаку'.format(turn))
                    history.append('Ход {0}. Противник кританул по Ведьмаку'.format(turn))

                witcher.witcher_main_damage(damage, turn, history, critical_hit)

            else:
                print('Ход {0}. Противник промахнулся по Ведьмаку'.format(turn))