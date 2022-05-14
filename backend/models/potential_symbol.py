class PotentialSymbol:
    def __init__(self, x, y, probability, symbol_type, template_type):
        self.x = x
        self.y = y
        self.probability = probability
        self.symbol_type = symbol_type
        self.template_type = template_type

    def __repr__(self):
        return f"({self.x},{self.y}) : {self.probability}, {self.symbol_type}, {self.template_type}"

    def set_duration(self):
        if self.symbol_type == "quarter":
            return 0.5
        elif self.symbol_type == "half":
            return 1
        elif self.symbol_type == "whole":
            return 2
