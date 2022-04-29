import sys
import random
from typing import List

import cv2
import cv2 as cv
import numpy as np
import musicalbeeps

from note import Note, PotentialNote
from staff import Staff, Line

def main(argv):





    default_file = 'resources/images/mary.jpg'
    filename = argv[0] if len(argv) > 0 else default_file

    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    width = src.shape[1]

    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    # bitwise the image background color (white should be the background)
    dst = cv2.bitwise_not(src)
    cdst = cv.cvtColor(src, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    linesP = cv.HoughLinesP(dst, rho=1, theta=np.pi / 180, threshold=50, lines=None, minLineLength=150, maxLineGap=1)

    all_lines = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            line: Line = Line(linesP[i][0][0], linesP[i][0][1], linesP[i][0][2], linesP[i][0][3])
            dist = Line.get_distance(line)
            # print(dist, 0.5 * width, 0.95 * width)
            if 0.7 * width <= dist <= 0.95 * width:
                all_lines.append(line)

    all_lines.sort(key=lambda line: line.y1)

    lines_without_duplicates = [] 
    for i in range(len(all_lines) - 1):
        current = all_lines[i]
        next = all_lines[i + 1]

        if next.y1 - current.y1 >= 5:
            lines_without_duplicates.append(current)
    lines_without_duplicates.append(all_lines[len(all_lines) - 1])

    grouped_lines = [lines_without_duplicates[i:i + 5] for i in range(0, len(lines_without_duplicates), 5)]

    staves = []
    for group in grouped_lines:
        staff: Staff = Staff()
        for line in group:
            staff.lines.append(line)
        staves.append(staff)

    for staff in staves:
        r = random.randint(0, 100)
        g = random.randint(0, 100)
        b = random.randint(0, 100)

        for line in staff.lines:
            x1 = line.x1
            x2 = line.x2
            y = line.y1

            cv.line(cdstP, (x1, y), (x2, y), (r, g, b), 2, cv.LINE_AA)

    # ------------------------------------- notes

    note_paths = {
        "quarter": [
            "resources/templates/notes/quarter.png",
            "resources/templates/notes/solid-note.png"
        ],
        "half": [
            "resources/templates/notes/half-space.png",
            "resources/templates/notes/half-note-line.png",
            "resources/templates/notes/half-line.png",
            "resources/templates/notes/half-note-space.png"
        ],
        "whole": [
            "resources/templates/notes/whole-space.png",
            "resources/templates/notes/whole-note-line.png",
            "resources/templates/notes/whole-line.png",
            "resources/templates/notes/whole-note-space.png"
        ]
    }

    locations = []
    notes = []

    for note_type in note_paths:
        samples = note_paths[note_type]
        for sample in samples:
            template = cv.imread(sample, 0)
            img_gray = cv.cvtColor(cdstP, cv.COLOR_BGR2GRAY)
            w, h = template.shape[::-1]
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            loc_and_type = (loc, note_type)
            locations.append(loc_and_type)

            for pt in zip(loc[1], loc[0]):
                pt = (*pt, res[pt[1], pt[0]])
                note = PotentialNote(pt[0], pt[1], res[pt[1], pt[0]], note_type)
                notes.append(note)
                cv.rectangle(cdstP, pt[:2], (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    grouped_notes_by_staff = []

    for staff in staves:
        current_staff_notes = []
        first_line = staff.lines[0]
        last_line = staff.lines[4]

        for note in notes:
            if first_line.y1 <= note.y <= last_line.y1:
                current_staff_notes.append(note)
        grouped_notes_by_staff.append((staff, current_staff_notes))

    all_notes: List[Note] = []
    for staff, possible_notes in grouped_notes_by_staff:
        possible_notes.sort(key=lambda x: x.x)
        staff.possible_notes = possible_notes
        staff.remove_duplicates()
        staff.set_pitch_and_duration()

        all_notes.append(staff.notes)

    # ------------------------------------------ play the notes
    player = musicalbeeps.Player(volume=0.3, mute_output=False)

    for final_per_staff in all_notes:
        for note in final_per_staff:
            print(note.pitch, note.duration)
            player.play_note(note.pitch, note.duration)

    cv.imwrite('res.png', cdstP)
    cv.imshow('result', cv2.resize(cdstP, (1280, 960)))
    cv.waitKey()

if __name__ == "__main__":
    main(sys.argv[1:])
