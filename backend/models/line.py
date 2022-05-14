class Line:
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return f"{self.x1}, {self.y1}, {self.x2}, {self.y2}"

    def get_distance(self):
        return self.x2 - self.x1
