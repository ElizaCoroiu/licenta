from typing import List

import cv2
import cv2 as cv
import numpy as np

from models.line import Line
from models.staff import Staff
from models.symbol import Symbol
from image_processing import template_matching


def get_notes(default_file):
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

    rest_paths = {
        "eighth": ["resources/templates/rest/eighth_rest.jpg"],
        "quarter": ["resources/templates/rest/quarter_rest.jpg"],
        "half": ["resources/templates/rest/half_rest_1.jpg",
                 "resources/templates/rest/half_rest_2.jpg"],
        "whole": ["resources/templates/rest/whole_rest.jpg"]
    }

    alterations_paths = {
        "sharp": [
            "resources/templates/alterations/sharp-line.png",
            "resources/templates/alterations/sharp-space.png"
        ],
        "flat": [
            "resources/templates/alterations/flat-line.png",
            "resources/templates/alterations/flat-space.png"
        ]
    }

    # default_file = 'resources/images/mary.jpg'
    src = cv.imread(cv.samples.findFile(default_file), cv.IMREAD_GRAYSCALE)
    width = src.shape[1]

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

    # process only staff lines ---------------------

    if linesP is not None:
        for i in range(0, len(linesP)):
            line: Line = Line(linesP[i][0][0], linesP[i][0][1], linesP[i][0][2], linesP[i][0][3])
            dist = Line.get_distance(line)

            if 0.7 * width <= dist <= 0.95 * width:
                all_lines.append(line)

    all_lines.sort(key=lambda line: line.y1)

    # remove line duplicates ----------------

    lines_without_duplicates = []
    for i in range(len(all_lines) - 1):
        current_line = all_lines[i]
        next_line = all_lines[i + 1]

        if next_line.y1 - current_line.y1 >= 5:
            lines_without_duplicates.append(current_line)

    lines_without_duplicates.append(all_lines[len(all_lines) - 1])

    # group line by staff
    grouped_lines = [lines_without_duplicates[i:i + 5] for i in range(0, len(lines_without_duplicates), 5)]

    # create the staff and all its 5 specific lines
    staves = []
    for group in grouped_lines:
        staff: Staff = Staff()
        for line in group:
            staff.lines.append(line)

        staff.line_one = staff.lines[0]
        staff.line_two = staff.lines[1]
        staff.line_three = staff.lines[2]
        staff.line_four = staff.lines[3]
        staff.line_five = staff.lines[4]

        staff.line_spacing = staff.line_two.y1 - staff.line_one.y1
        staves.append(staff)

    # template matching for notes, rests, alterations
    note_locations = template_matching.match(cdstP, note_paths, 0.7, "note")
    rest_locations = template_matching.match(cdstP, rest_paths, 0.8, "rest")
    alterations_frames = template_matching.match(cdstP, alterations_paths, 0.7, "alteration")

    grouped_symbols_by_staff = []

    # append found matches to each corresponding staff / group all symbols by staff
    for staff in staves:
        current_staff_symbols = []

        current_staff_notes = staff.get_symbols_inside_staff(note_locations)
        current_staff_rests = staff.get_symbols_inside_staff(rest_locations)

        for note in current_staff_notes:
            current_staff_symbols.append(note)

        for rest in current_staff_rests:
            current_staff_symbols.append(rest)

        for alteration in alterations_frames:
            if staff.line_one.y1 <= alteration.middle[1] <= staff.line_five.y1:
                current_staff_symbols.append(alteration)

        grouped_symbols_by_staff.append((staff, current_staff_symbols))

    # create the symbols for each staff, sort the symbols, remove duplicates, set pitch and duration for rest and notes
    # and set and apply alterations for each staff

    all_symbols: List[Symbol] = []
    for staff, possible_symbols in grouped_symbols_by_staff:
        possible_symbols.sort(key=lambda x: x.x)

        staff.possible_symbols = possible_symbols

        staff.remove_duplicates()

        staff.set_pitch_and_duration()

        staff.set_alterations(staff.alterations_frames[0].symbol_type)

        staff.apply_alterations_to_notes()

        all_symbols.append(staff.symbols)
    return all_symbols
