__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from sys import maxsize
from typing import List, Dict, Tuple

"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; 
small hydrothermal vents release smoke into the caves that slowly settles like 
rain.

If you can model how the smoke flows through the caves, you might be able to 
avoid it and be that much safer. The submarine generates a heightmap of the 
floor of the nearby caves for you (your puzzle input).
"""

################################################################################

SELF_DIR_NAME = "day_09"
INPUT_TXT_NAME = "input.txt"

################################################################################

class Heightmap(object):
    BASIN_END = 9
    KEY_ROW = "ROW"
    KEY_COLUMN = "COLUMN"
    KEY_SIZE = "SIZE"

################################################################################

    def __init__(self):
        """

        """

        super().__init__()

        with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
            self._heightmap = tuple(map(
                lambda row: tuple([int(value) for value in row]),
                [line.strip() for line in f.readlines()]))

        self._low_points = []
        self._find_low_points()
        self._basins = []
        self._find_basins()

################################################################################

    def _find_low_points(self) -> None:
        """
        Finds the locations that are lower than any of its adjacent locations.
        Most locations have four adjacent locations (up, down, left, and right);
        locations on the edge or corner of the map have three or two adjacent
        locations, respectively. (Diagonal locations do not count as adjacent.)
        """

        for row in range(len(self._heightmap)):
            for column in range(len(self._heightmap[row])):
                height = self._heightmap[row][column]

                height_up = maxsize
                if row > 0:
                    height_up = self._heightmap[row - 1][column]

                height_down = maxsize
                if row < len(self._heightmap) - 1:
                    height_down = self._heightmap[row + 1][column]

                height_left = maxsize
                if column > 0:
                    height_left = self._heightmap[row][column - 1]

                height_right = maxsize
                if column < len(self._heightmap[row]) - 1:
                    height_right = self._heightmap[row][column + 1]

                if all([height < adjacent
                        for adjacent in (height_up, height_down, height_left, height_right)]):
                    self._low_points.append({
                        self.KEY_ROW: row,
                        self.KEY_COLUMN: column
                    })

################################################################################

    def _find_basins(self) -> None:
        """
        A basin is all locations that eventually flow downward to a single low
        point. Therefore, every low point has a basin, although some basins are
        very small. Locations of height 9 do not count as being in any basin,
        and all other locations will always be part of exactly one basin.

        The size of a basin is the number of locations within the basin, including
        the low point.
        """

        for low_point in self._low_points:
            basin_center_row = low_point[self.KEY_ROW]
            basin_center_column = low_point[self.KEY_COLUMN]
            # we will recursively search for basin fields; we have to keep track
            # of them, because some fields could be added to the basin more than
            # once
            basin_fields = [{
                self.KEY_ROW: basin_center_row,
                self.KEY_COLUMN: basin_center_column
            }]
            # recursively search for the whole basin
            basin_fields = self._search_basin(basin_center_row, basin_center_column, basin_fields)

            self._basins.append({
                self.KEY_ROW: basin_center_row,
                self.KEY_COLUMN: basin_center_column,
                self.KEY_SIZE: len(basin_fields)
            })

################################################################################

    def _search_basin(self, initial_row: int, initial_column: int, basin_fields: List[Dict[str, int]]) -> List[Dict[str, int]]:
        """
        Recursively looks around a point in the heightmap in four directions; It
        adds fields to the basin as long as the height goes up and basin end
        (height 9) is not hit.

        :param initial_row: row number of a point in the heightmap we look
        around
        :param initial_column: column number of a point in the heightmap we look
        around
        :param basin_fields: fields that were so far discovered in the current
        basin
        :return: fields that were so far discovered in the current basin
        """

        height_previous = self._heightmap[initial_row][initial_column]

        # up
        row = initial_row - 1
        column = initial_column
        if row >= 0:
            basin_field = {
                self.KEY_ROW: row,
                self.KEY_COLUMN: column
            }
            if basin_field not in basin_fields:
                height = self._heightmap[row][column]
                if height != self.BASIN_END and height > height_previous:
                    basin_fields.append(basin_field)
                    basin_fields = self._search_basin(row, column, basin_fields)

        # down
        row = initial_row + 1
        column = initial_column
        if row < len(self._heightmap):
            basin_field = {
                self.KEY_ROW: row,
                self.KEY_COLUMN: column
            }
            if basin_field not in basin_fields:
                height = self._heightmap[row][column]
                if height != self.BASIN_END and height > height_previous:
                    basin_fields.append(basin_field)
                    basin_fields = self._search_basin(row, column, basin_fields)

        # left
        row = initial_row
        column = initial_column - 1
        if column >= 0:
            basin_field = {
                self.KEY_ROW: row,
                self.KEY_COLUMN: column
            }
            if basin_field not in basin_fields:
                height = self._heightmap[row][column]
                if height != self.BASIN_END and height > height_previous:
                    basin_fields.append(basin_field)
                    basin_fields = self._search_basin(row, column, basin_fields)

        # right
        row = initial_row
        column = initial_column + 1
        if column < len(self._heightmap[0]):
            basin_field = {
                self.KEY_ROW: row,
                self.KEY_COLUMN: column
            }
            if basin_field not in basin_fields:
                height = self._heightmap[row][column]
                if height != self.BASIN_END and height > height_previous:
                    basin_fields.append(basin_field)
                    basin_fields = self._search_basin(row, column, basin_fields)

        return basin_fields

################################################################################

    @property
    def risk_level_sum(self) -> int:
        """
        :return: The sum of the risk levels of all low points; the risk level of
        a low point is 1 plus its height
        """

        return sum([
            self._heightmap[low_point[self.KEY_ROW]][low_point[self.KEY_COLUMN]] + 1
            for low_point in self._low_points])

################################################################################

    @property
    def basins(self) -> Tuple:
        """
        :return: all basins with their low points and sizes
        """

        return tuple(self._basins)

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Smoke flows to the lowest point of the area it's in. For example, consider
    the following heightmap:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

    Each number corresponds to the height of a particular location, where 9 is
    the highest and 0 is the lowest a location can be.

    Your first goal is to find the low points - the locations that are lower
    than any of its adjacent locations. Most locations have four adjacent
    locations (up, down, left, and right); locations on the edge or corner of
    the map have three or two adjacent locations, respectively. (Diagonal
    locations do not count as adjacent.)

    In the above example, there are four low points, all highlighted: two are in
    the first row (a 1 and a 0), one is in the third row (a 5), and one is in
    the bottom row (also a 5). All other locations on the heightmap have some
    lower adjacent location, and so are not low points.

    The risk level of a low point is 1 plus its height. In the above example,
    the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk
    levels of all low points in the heightmap is therefore 15.

    Find all of the low points on your heightmap. What is the sum of the risk
    levels of all low points on your heightmap?
    """

    heightmap = Heightmap()
    # should be 504
    print(heightmap.risk_level_sum)

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Next, you need to find the largest basins so you know what areas are most
    important to avoid.

    A basin is all locations that eventually flow downward to a single low
    point. Therefore, every low point has a basin, although some basins are very
    small. Locations of height 9 do not count as being in any basin, and all
    other locations will always be part of exactly one basin.

    The size of a basin is the number of locations within the basin, including
    the low point. The example above has four basins.

    The top-left basin, size 3:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

    The top-right basin, size 9:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

    The middle basin, size 14:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

    The bottom-right basin, size 9:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

    Find the three largest basins and multiply their sizes together. In the
    above example, this is 9 * 14 * 9 = 1134.

    What do you get if you multiply together the sizes of the three largest
    basins?
    """

    heightmap = Heightmap()
    basins = tuple(sorted(heightmap.basins, key=lambda basin: basin[heightmap.KEY_SIZE], reverse=True))
    # should be 1558722
    print(basins[0][heightmap.KEY_SIZE] * basins[1][heightmap.KEY_SIZE] * basins[2][heightmap.KEY_SIZE])

################################################################################