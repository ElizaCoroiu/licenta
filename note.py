from typing import List


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


class Note:
    def __init__(self, pitch=None, duration=None):
        self.pitch = pitch
        self.duration = duration
