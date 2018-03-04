class Camp:
    __camps = set()

    def __init__(self, ant_number):
        self.ant_number = ant_number
        Camp.__camps.add(self)

    @staticmethod
    def get_camps():
        return Camp.__camps
