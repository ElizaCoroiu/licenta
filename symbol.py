
class PotentialNote:
    def __init__(self, x, y, probability, note_type):
        self.x = x
        self.y = y
        self.probability = probability
        self.note_type = note_type

    def get_note(self):
        pass

    def __repr__(self):
        return f"{self.x},{self.y}:{self.probability},{self.note_type}"

    def set_duration(self):
        if self.note_type == "quarter":
            return 0.5
        elif self.note_type == "half":
            return 1
        elif self.note_type == "whole":
            return 2


class Note:
    def __init__(self, pitch=None, duration=None):
        self.pitch = pitch
        self.duration = duration
