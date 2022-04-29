import sys
import random

import cv2
import cv2 as cv
import numpy as np


def main(argv):
    default_file = 'images/mary.jpg'
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

    staves = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            line = linesP[i][0]
            dist = line[2] - line[0]
            # print(dist, 0.5 * width, 0.95 * width)
            if 0.6 * width <= dist <= 0.95 * width:
                staves.append(line)

    staves.sort(key=lambda x: x[1])

    filtered_staves = []

    for i in range(len(staves) - 1):
        current = staves[i]
        next = staves[i + 1]

        if next[1] - current[1] >= 5:
            filtered_staves.append(current)

    grouped_staves = [filtered_staves[i:i + 5] for i in range(0, len(filtered_staves), 5)]

    for staff in grouped_staves:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        print("staff")

        for line in staff:
            print(line)

            x1 = line[0]
            x2 = line[2]
            y = line[1]

            cv.line(cdstP, (x1, y), (x2, y), (r, g, b), 1, cv.LINE_AA)
            cv.circle(cdstP, (x1, y), 3, (139, 0, 0), -1)

    cv.imshow("Detected Staves (in red) - Probabilistic Line Transform", cdstP)

    cv.waitKey()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
