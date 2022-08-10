class MovingAverage:
    def __init__(self, maxLength: int):
        self.values = []
        self.maxLength = maxLength

    def addData(self, data):
        if len(self.values) == self.maxLength:
            self.values.pop(0)

        self.values.append(data)

    def average(self):
        if len(self.values) != self.maxLength:
            return -1

        return sum(self.values) / self.maxLength
