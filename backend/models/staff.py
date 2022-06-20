from typing import List

import cv2

from models.symbol import Symbol
from models.potential_symbol import PotentialSymbol
from models.frame import AlterationFrame
from models.line import Line


class Staff:
    def __init__(self):
        self.lines: List[Line] = []
        self.symbols: List[Symbol] = []
        self.possible_symbols: List[PotentialSymbol] = []
        self.alterations_frames: List[AlterationFrame] = []
        self.alterations: str = []

        self.line_one = Line()
        self.line_two = Line()
        self.line_three = Line()
        self.line_four = Line()
        self.line_five = Line()

        self.line_spacing = 0
        self.image = None

    def remove_duplicates(self):
        new_symbols = []
        prev_symbol = -1
        new_group = []

        for n in self.possible_symbols:
            if prev_symbol == -1 or abs(n.x - prev_symbol) < 4:
                new_group.append(n)
            else:
                if new_group:
                    best_symbol = max(new_group, key=lambda x: x.probability)
                    new_group = [n]
                else:
                    best_symbol = n
                    new_group = []

                new_symbols.append(best_symbol)
            prev_symbol = n.x
        if new_group:
            best_symbol = max(new_group, key=lambda x: x.probability)
            new_symbols.append(best_symbol)
        self.possible_symbols = new_symbols

    def get_symbols_inside_staff(self, locations):
        current_staff_symbols = []

        for symbol in locations:
            if (self.line_one.y1 - self.line_spacing * 4) <= symbol.y <= (
                    self.line_five.y1 + self.line_spacing * 4):
                current_staff_symbols.append(symbol)

        return current_staff_symbols

    def set_pitch_and_duration(self):
        symbols: List[Symbol] = []

        for possible_symbol in self.possible_symbols:
            if possible_symbol.template_type == "alteration":
                self.alterations_frames.append(possible_symbol)

        for possible_symbol in self.possible_symbols:
            symbol = Symbol()

            if possible_symbol.template_type == "rest":
                symbol.name = "rest"
                symbol.pitch = "pause"

            if possible_symbol.template_type == "note":
                symbol.name = "note"

                for i in range(len(self.lines) - 1):
                    current_line = self.lines[i]
                    next_line = self.lines[i + 1]

                    if abs(current_line.y1 - possible_symbol.y) <= 3:
                        symbol.pitch = self.match_note_between_lines_inside_staff(possible_symbol)
                    elif current_line.y1 < possible_symbol.y < next_line.y1 and abs(possible_symbol.y - current_line.y1) > 3 and \
                            abs(next_line.y1 - possible_symbol.y) > 3:
                        symbol.pitch = self.match_note_on_lines_inside_staff(possible_symbol)

                # above the staff
                if possible_symbol.y < self.line_one.y1:

                    first_line_above_y = self.line_one.y1 - self.line_spacing
                    second_line_above_y = self.line_one.y1 - 2 * self.line_spacing
                    third_line_above_y = self.line_one.y1 - 3 * self.line_spacing

                    if first_line_above_y < possible_symbol.y < self.line_one.y1 and \
                            abs(possible_symbol.y - first_line_above_y) > 3 and \
                            abs(self.line_one.y1 - possible_symbol.y) > 3:
                        cv2.putText(img=self.image, text='F5', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "F5"

                    elif abs(first_line_above_y - possible_symbol.y) <= 3:
                        cv2.putText(img=self.image, text='G5', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "G5"

                    elif second_line_above_y < possible_symbol.y < first_line_above_y and \
                            abs(possible_symbol.y - second_line_above_y) > 3 and \
                            abs(first_line_above_y - possible_symbol.y) > 3:
                        cv2.putText(img=self.image, text='A5', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "A5"

                    elif abs(second_line_above_y - possible_symbol.y) <= 3:
                        cv2.putText(img=self.image, text='B5', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "B5"

                    elif third_line_above_y < possible_symbol.y < second_line_above_y and \
                            abs(possible_symbol.y - third_line_above_y) > 3 and \
                            abs(second_line_above_y - possible_symbol.y) > 3:
                        cv2.putText(img=self.image, text='C6', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "C6"

                    elif abs(third_line_above_y - possible_symbol.y) <= 3:
                        cv2.putText(img=self.image, text='D6', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "D6"

                # below staff
                elif possible_symbol.y > self.line_five.y1:

                    first_line_below_y = self.line_five.y1 + self.line_spacing
                    second_line_below_y = self.line_five.y1 + 2 * self.line_spacing
                    third_line_below_y = self.line_five.y1 + 3 * self.line_spacing

                    if abs(self.line_five.y1 - possible_symbol.y) <= 3:
                        cv2.putText(img=self.image, text='D4', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "D4"

                    elif self.line_five.y1 < possible_symbol.y < first_line_below_y and \
                            abs(possible_symbol.y - self.line_five.y1) > 3 and \
                            abs(first_line_below_y - possible_symbol.y) > 3:
                        cv2.putText(img=self.image, text='C4', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "C4"

                    elif abs(first_line_below_y - possible_symbol.y) <= 3:
                        cv2.putText(img=self.image, text='B3', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "B3"

                    elif first_line_below_y < possible_symbol.y < second_line_below_y and \
                            abs(possible_symbol.y - first_line_below_y) > 3 and \
                            abs(second_line_below_y - possible_symbol.y) > 3:
                        cv2.putText(img=self.image, text='A3', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "A3"

                    elif abs(second_line_below_y - possible_symbol.y) <= 3:
                        cv2.putText(img=self.image, text='G3', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "G3"

                    elif second_line_below_y < possible_symbol.y < third_line_below_y and \
                            abs(possible_symbol.y - second_line_below_y) > 3 and \
                            abs(third_line_below_y - possible_symbol.y) > 3:
                        cv2.putText(img=self.image, text='F3', org=(possible_symbol.x, possible_symbol.y - 5),
                                    fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                                    color=(0, 0, 0), thickness=1)
                        symbol.pitch = "F3"

            symbol.duration = possible_symbol.set_duration()

            if symbol.pitch is not None:
                symbols.append(symbol)
        self.symbols = symbols

    def match_note_between_lines_inside_staff(self, possible_note):
        if abs(possible_note.y - self.line_one.y1) <= 3:
            cv2.putText(img=self.image, text='E5', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "E5"

        elif abs(possible_note.y - self.line_two.y1) <= 3:
            cv2.putText(img=self.image, text='C5', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "C5"

        elif abs(possible_note.y - self.line_three.y1) <= 3:
            cv2.putText(img=self.image, text='A4', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "A4"

        elif abs(possible_note.y - self.line_four.y1) <= 3:
            cv2.putText(img=self.image, text='F4', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "F4"

        elif abs(possible_note.y - self.line_five.y1) <= 3:
            cv2.putText(img=self.image, text='D4', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "D4"

    def match_note_on_lines_inside_staff(self, possible_note):
        if self.line_one.y1 < possible_note.y < self.line_two.y1:
            cv2.putText(img=self.image, text='D5', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "D5"

        elif self.line_two.y1 < possible_note.y < self.line_three.y1:
            cv2.putText(img=self.image, text='B4', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "B4"
        elif self.line_three.y1 < possible_note.y < self.line_four.y1:
            cv2.putText(img=self.image, text='G4', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "G4"

        elif self.line_four.y1 < possible_note.y < self.line_five.y1:
            cv2.putText(img=self.image, text='E4', org=(possible_note.x, possible_note.y - 5),
                        fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
                        color=(0, 0, 0), thickness=1)
            return "E4"

    def set_alterations(self, symbol_type):
        if symbol_type == "sharp":
            if len(self.alterations_frames) == 1:
                self.alterations.append(["F#"])
            elif len(self.alterations_frames) == 2:
                self.alterations.append(["F#", "C#"])
            elif len(self.alterations_frames) == 3:
                self.alterations.append(["F#", "C#", "G#"])
            elif len(self.alterations_frames) == 4:
                self.alterations.append(["F#", "C#", "G#", "D#"])
            elif len(self.alterations_frames) == 5:
                self.alterations.append(["F#", "C#", "G#", "D#", "A#"])
            elif len(self.alterations_frames) == 6:
                self.alterations.append(["F#", "C#", "G#", "D#", "A#", "E#"])
            elif len(self.alterations_frames) == 7:
                self.alterations.append(["F#", "C#", "G#", "D#", "A#", "E#", "B#"])
        elif symbol_type == "flat":
            if len(self.alterations_frames) == 1:
                self.alterations.append(["Bb"])
            elif len(self.alterations_frames) == 2:
                self.alterations.append(["Bb", "Eb"])
            elif len(self.alterations_frames) == 3:
                self.alterations.append(["Bb", "Eb", "Ab"])
            elif len(self.alterations_frames) == 4:
                self.alterations.append(["Bb", "Eb", "Ab", "Db"])
            elif len(self.alterations_frames) == 5:
                self.alterations.append(["Bb", "Eb", "Ab", "Db", "Gb"])
            elif len(self.alterations_frames) == 6:
                self.alterations.append(["Bb", "Eb", "Ab", "Db", "Gb", "Cb"])
            elif len(self.alterations_frames) == 7:
                self.alterations.append(["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"])

    def apply_alterations_to_notes(self):
        for symbol in self.symbols:
            if symbol.name != "rest" and symbol.pitch is not None:
                for alt_list in self.alterations:
                    for alteration in alt_list:
                        if symbol.pitch[0] == alteration[0]:
                            symbol.pitch += alteration[1]
