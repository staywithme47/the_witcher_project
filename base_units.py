class Unit:
    amount_of_alive = 0

    def __init__(self, level):
        self.level = level
        Unit.update_amount_of_alive(0)

    @staticmethod
    def update_amount_of_alive(number):
        if number > 0:
            Unit.amount_of_alive -= 1
        else:
            Unit.amount_of_alive += 1
        print('Amount of objects: ', Unit.amount_of_alive)