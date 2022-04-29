import sys
import math
import cv2 as cv
import numpy as np


def main(argv):
    default_file = 'piano.png'
    filename = argv[0] if len(argv) > 0 else default_file

    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    height = src.shape[0]
    width = src.shape[1]

    print(height)
    print(width)

    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    # Edge detection
    dst = cv.Canny(src, 50, 200, None, 3)
    # cv.imshow("edges", dst)
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    # print(lines)

    # count = 0
    # n = len(lines)
    # i = 0
    # for i in range(n):
    #     for j in range(i + 1, n):
    #         if lines[i][0][0] == lines[j][0][0] and lines[i][0][1] == lines[j][0][1]:
    #             count += 1
    # print(count)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]

            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho

            # print("------")
            # print(x0, y0)
            # pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            # pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            pt1 = (int(x0) + 50, int(y0))
            pt2 = (int(x0) + 650, int(y0))
            if theta > 1.55 and theta < 1.58:
                cv.line(cdst, pt1, pt2, (0, 0, 255), 1, cv.LINE_AA)
                # print(theta, rho)


    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    linesPSorted = np.sort(linesP, axis=0)
    # print(linesPSorted)

    startingPoints = []
    endingPoints = []

    if linesPSorted is not None:
        for i in range(0, len(linesPSorted)):
            l = linesPSorted[i][0]

            startingPoints.append([l[0], l[1]])
            endingPoints.append((l[2], l[3]))
    # print(endingPoints)

    if linesP is not None:
        for i in range(0, len(linesP) - 1):
            l = linesP[i][0]
            dist = l[2] - l[0];
            print(dist)
            # if l[0] >= 10 and l[0] <= 100 and l[2] >= 650:
            if (dist >= 0.5 * width and dist <= 0.95 * width):
                # print(dist)
                cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)

    # cv.imshow("Source", src)
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv.waitKey()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
