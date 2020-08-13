class Unit:
    amount_of_alive = 0

    def __init__(self, level):
        self.level = level
        Unit.update_amount_of_alive(True)

    @staticmethod
    def update_amount_of_alive(created):
        if not created:
            Unit.amount_of_alive -= 1
        else:
            Unit.amount_of_alive += 1
        print('Amount of objects: ', Unit.amount_of_alive)