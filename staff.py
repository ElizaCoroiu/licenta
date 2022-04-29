from typing import List
from note import Note, PotentialNote


class Staff:
    def __init__(self):
        self.lines: List[Line] = []
        self.notes: List[Note] = []
        self.possible_notes: List[PotentialNote] = []

    def remove_duplicates(self):
        new_notes = []
        prev_note = -1
        new_group = []
        for n in self.possible_notes:
            if prev_note == -1 or abs(n.x - prev_note) < 4:
                new_group.append(n)
            else:
                if new_group:
                    best_note = max(new_group, key=lambda x: x.probability)
                else:
                    best_note = n
                new_notes.append(best_note)
                new_group = []
            prev_note = n.x
        if new_group:
            best_note = max(new_group, key=lambda x: x.probability)
            new_notes.append(best_note)
        self.possible_notes = new_notes

    def set_pitch_and_duration(self):
        notes: List[Note] = []
        for possible_note in self.possible_notes:
            note = Note()

            for i in range(len(self.lines) - 1):
                current_line = self.lines[i]
                next_line = self.lines[i + 1]
                if abs(current_line.y1 - possible_note.y) < 3:
                    note.pitch = self.match_note_between_lines(possible_note)
                elif current_line.y1 < possible_note.y < next_line.y1 and (possible_note.y - current_line.y1) > 3 and \
                        abs(next_line.y1 - possible_note.y) > 3:
                    note.pitch = self.match_note_on_lines(possible_note)

            note.duration = set_duration(possible_note)

            notes.append(note)
        self.notes = notes

    def match_note_between_lines(self, possible_note):
        # staff lines:
        first_line_y = self.lines[0].y1
        second_line_y = self.lines[1].y1
        third_line_y = self.lines[2].y1
        fourth_line_y = self.lines[3].y1
        fifth_line_y = self.lines[4].y1

        if abs(possible_note.y - first_line_y) < 3:
            # cv2.putText(img=cdstP, text='MI', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "E5"
        elif abs(possible_note.y - second_line_y) < 3:
            # cv2.putText(img=cdstP, text='DO', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "C5"
        elif abs(possible_note.y - third_line_y) < 3:
            # cv2.putText(img=cdstP, text='LA', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "A4"
        elif abs(possible_note.y - fourth_line_y) < 3:
            # cv2.putText(img=cdstP, text='FA', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "F4"
        elif abs(possible_note.y - fifth_line_y) < 3:
            # cv2.putText(img=cdstP, text='RE', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "D4"

    def match_note_on_lines(self, possible_note):
        # staff lines:
        first_line_y = self.lines[0].y1
        second_line_y = self.lines[1].y1
        third_line_y = self.lines[2].y1
        fourth_line_y = self.lines[3].y1
        fifth_line_y = self.lines[4].y1

        if first_line_y < possible_note.y < second_line_y:
            # cv2.putText(img=cdstP, text='RE', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "D5"
        elif second_line_y < possible_note.y < third_line_y:
            # cv2.putText(img=cdstP, text='SI', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "B4"
        elif third_line_y < possible_note.y < fourth_line_y:
            # cv2.putText(img=cdstP, text='SOL', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "G4"
        elif fourth_line_y < possible_note.y < fifth_line_y:
            # cv2.putText(img=cdstP, text='MI', org=(possible_note.x, possible_note.y - 5), fontFace=cv2.QT_FONT_NORMAL, fontScale=1,
            #             color=(0, 0, 0), thickness=1)
            return "E4"

def set_duration(possible_note):
    if possible_note.note_type == "quarter":
        return 0.5
    elif possible_note.note_type == "half":
        return 1
    elif possible_note.note_type == "whole":
        return 2

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

