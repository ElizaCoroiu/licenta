from models.potential_symbol import PotentialSymbol


class AlterationFrame(PotentialSymbol):
    def __init__(self, x, y, probability, symbol_type, template_type, w, h):
        PotentialSymbol.__init__(self, x, y, probability, symbol_type, template_type)
        self.w = w
        self.h = h
        self.middle = self.x + self.w / 2, self.y + self.h / 2

    def __repr__(self):
        return f"{self.x}, " \
               f"{self.y}, " \
               f"{self.w}, " \
               f"{self.h}, " \
               f"{self.middle}, " \
               f"{self.probability}, " \
               f"{self.symbol_type}, " \
               f"{self.template_type}"
