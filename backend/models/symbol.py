class Symbol:
    def __init__(self, name=None, pitch=None, duration=None):
        self.name = name
        self.pitch: str = pitch
        self.duration = duration

    def __repr__(self):
        return f"{self.name} - {self.pitch} - {self.duration}"
