__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from re import compile

"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents 
constantly produce large, opaque clouds, so it would be best to avoid them if 
possible.
"""

################################################################################

SELF_DIR_NAME = "day_05"
INPUT_TXT_NAME = "input.txt"
X1_KEY = "X1"
X2_KEY = "X2"
Y1_KEY = "Y1"
Y2_KEY = "Y2"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    They tend to form in lines; the submarine helpfully produces a list of
    nearby lines of vents (your puzzle input) for you to review. For example:

    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2

    Each line of vents is given as a line segment in the format x1,y1 -> x2,y2
    where x1,y1 are the coordinates of one end the line segment and x2,y2 are
    the coordinates of the other end. These line segments include the points at
    both ends. In other words:

    -An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    -An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

    For now, only consider horizontal and vertical lines: lines where either
    x1 = x2 or y1 = y2.

    So, the horizontal and vertical lines from the above list would produce the
    following diagram:

    .......1..
    ..1....1..
    ..1....1..
    .......1..
    .112111211
    ..........
    ..........
    ..........
    ..........
    222111....

    In this diagram, the top left corner is 0,0 and the bottom right corner is
    9,9. Each position is shown as the number of lines which cover that point
    or . if no line covers that point. The top-left pair of 1s, for example,
    comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping
    lines 0,9 -> 5,9 and 0,9 -> 2,9.

    To avoid the most dangerous areas, you need to determine the number of
    points where at least two lines overlap. In the above example, this is
    anywhere in the diagram with a 2 or larger - a total of 5 points.

    Consider only horizontal and vertical lines. At how many points do at least
    two lines overlap?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        pattern = compile(r'\d+')
        lines = [{
            X1_KEY: int(pattern.findall(line)[0]),
            Y1_KEY: int(pattern.findall(line)[1]),
            X2_KEY: int(pattern.findall(line)[2]),
            Y2_KEY: int(pattern.findall(line)[3])
        } for line in f.readlines()]

        # filter only horizontal and vertical lines out
        horizontal = tuple(filter(lambda line: line[Y1_KEY] == line[Y2_KEY], lines))
        vertical = tuple(filter(lambda line: line[X1_KEY] == line[X2_KEY], lines))

        # figure out the diagram size and create the diagram
        width = max([max(line[X1_KEY], line[X2_KEY]) for line in horizontal + vertical])
        height = max([max(line[Y1_KEY], line[Y2_KEY]) for line in horizontal + vertical])
        diagram = list([list([0 for _ in range(width + 1)]) for _ in range(height + 1)])

        # put all the horizontal and vertical lines in the diagram
        for line in horizontal:
            for x in range(min(line[X1_KEY], line[X2_KEY]), max(line[X1_KEY], line[X2_KEY]) + 1):
                diagram[line[Y1_KEY]][x] += 1

        for line in vertical:
            for y in range(min(line[Y1_KEY], line[Y2_KEY]), max(line[Y1_KEY], line[Y2_KEY]) + 1):
                diagram[y][line[X1_KEY]] += 1

    # should be 8111
    print(sum([sum([1 for number in row if number >= 2]) for row in diagram]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Unfortunately, considering only horizontal and vertical lines doesn't give
    you the full picture; you need to also consider diagonal lines.

    Because of the limits of the hydrothermal vent mapping system, the lines in
    your list will only ever be horizontal, vertical, or a diagonal line at
    exactly 45 degrees. In other words:

    -An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    -An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

    Considering all lines from the above example would now produce the following
    diagram:

    1.1....11.
    .111...2..
    ..2.1.111.
    ...1.2.2..
    .112313211
    ...1.2....
    ..1...1...
    .1.....1..
    1.......1.
    222111....

    You still need to determine the number of points where at least two lines
    overlap. In the above example, this is still anywhere in the diagram with a
    2 or larger - now a total of 12 points.

    Consider all of the lines. At how many points do at least two lines overlap?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        pattern = compile(r'\d+')
        lines = [{
            X1_KEY: int(pattern.findall(line)[0]),
            Y1_KEY: int(pattern.findall(line)[1]),
            X2_KEY: int(pattern.findall(line)[2]),
            Y2_KEY: int(pattern.findall(line)[3])
        } for line in f.readlines()]

        # sort the lines to horizontal, vertical and diagonal
        horizontal = tuple(filter(lambda line: line[Y1_KEY] == line[Y2_KEY], lines))
        vertical = tuple(filter(lambda line: line[X1_KEY] == line[X2_KEY], lines))
        diagonal = tuple(filter(lambda line: line not in horizontal and line not in vertical, lines))

        # figure out the diagram size and create the diagram
        width = max([max(line[X1_KEY], line[X2_KEY]) for line in lines])
        height = max([max(line[Y1_KEY], line[Y2_KEY]) for line in lines])
        diagram = list([list([0 for _ in range(width + 1)]) for _ in range(height + 1)])

        # put all the lines in the diagram
        for line in horizontal:
            for x in range(min(line[X1_KEY], line[X2_KEY]), max(line[X1_KEY], line[X2_KEY]) + 1):
                diagram[line[Y1_KEY]][x] += 1

        for line in vertical:
            for y in range(min(line[Y1_KEY], line[Y2_KEY]), max(line[Y1_KEY], line[Y2_KEY]) + 1):
                diagram[y][line[X1_KEY]] += 1

        for line in diagonal:
            if line[X1_KEY] < line[X2_KEY]:
                x_coords = tuple(range(line[X1_KEY], line[X2_KEY] + 1))
            else:
                x_coords = tuple(reversed(range(line[X2_KEY], line[X1_KEY] + 1)))
            if line[Y1_KEY] < line[Y2_KEY]:
                y_coords = tuple(range(line[Y1_KEY], line[Y2_KEY] + 1))
            else:
                y_coords = tuple(reversed(range(line[Y2_KEY], line[Y1_KEY] + 1)))

            for i in range(len(x_coords)):
                diagram[y_coords[i]][x_coords[i]] += 1

    # should be 22088
    print(sum([sum([1 for number in row if number >= 2]) for row in diagram]))

################################################################################