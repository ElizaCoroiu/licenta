from typing import List

import cv2 as cv
import numpy as np

from models.potential_symbol import PotentialSymbol
from models.frame import AlterationFrame


def match(img, paths, threshold, template_type):
    locations: List[PotentialSymbol] = []
    frames: List[AlterationFrame] = []

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    for symbol_duration in paths:
        samples = paths[symbol_duration]

        if symbol_duration == "flat":
            threshold = 0.77

        for sample in samples:
            template = cv.imread(sample, 0)

            w, h = template.shape[::-1]
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            tuples = zip(loc[1], loc[0])

            for pt in tuples:
                pt = (*pt, res[pt[1], pt[0]])
                symbol = PotentialSymbol(pt[0], pt[1], res[pt[1], pt[0]], symbol_duration, template_type)
                locations.append(symbol)

                if template_type == "alteration":
                    frame = AlterationFrame(symbol.x, symbol.y, symbol.probability,
                                            symbol.symbol_type, symbol.template_type, w, h)
                    frames.append(frame)

                #cv.circle(img, (pt[0], pt[1]), 5, (139, 0, 0), -1)

                #cv.rectangle(img, pt[:2], (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    if len(frames) > 0:
        return frames

    return locations

