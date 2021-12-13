__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join

"""
--- Day 11: Dumbo Octopus ---

You enter a large cavern full of rare bioluminescent dumbo octopuses! They seem 
to not like the Christmas lights on your submarine, so you turn them off for 
now.

There are 100 octopuses arranged neatly in a 10 by 10 grid. Each octopus slowly 
gains energy over time and flashes brightly for a moment when its energy is 
full. Although your lights are off, maybe you could navigate through the cave 
without disturbing the octopuses if you could predict when the flashes of light 
will happen.
"""

################################################################################

SELF_DIR_NAME = "day_11"
INPUT_TXT_NAME = "input.txt"
STEPS = 100


################################################################################

class Octopus(object):
    FLASH_ENERGY_LEVEL = 10
    ENERGY_LEVEL_RESET = 0

################################################################################

    def __init__(self, energy_level: int, row: int, column: int):
        """
        Creates a Dumbo Octopus with an initial energy level. It knows about its
        position in the octopuses map and keeps track of the number of its
        flashes as well.

        :param energy_level: initial energy level
        :param row: octopus row
        :param column: octopus column
        """

        super().__init__()
        self._energy_level = energy_level
        self._flashes_count = 0
        self._row = row
        self._column = column

################################################################################

    def increase_energy_level(self, octopuses) -> None:
        """
        Increases octopus energy level by one. If it causes the octopus to
        flash, it increases energy level of each of its neighbour by one as
        well.

        :param octopuses: octopuses map
        """

        self._energy_level += 1

        if self._energy_level == self.FLASH_ENERGY_LEVEL:
            self._flashes_count += 1

            if self._row > 0:
                if self._column > 0:
                    # top left
                    octopuses[self._row - 1][self._column - 1].increase_energy_level(octopuses)
                # top
                octopuses[self._row - 1][self._column].increase_energy_level(octopuses)
                if self._column < len(octopuses[self._row]) - 1:
                    # top right
                    octopuses[self._row - 1][self._column + 1].increase_energy_level(octopuses)

            if self._column > 0:
                # left
                octopuses[self._row][self._column - 1].increase_energy_level(octopuses)

            if self._column < len(octopuses[self._row]) - 1:
                # right
                octopuses[self._row][self._column + 1].increase_energy_level(octopuses)
            if self._row < len(octopuses) - 1:
                if self._column > 0:
                    # bottom left
                    octopuses[self._row + 1][self._column - 1].increase_energy_level(octopuses)
                # bottom
                octopuses[self._row + 1][self._column].increase_energy_level(octopuses)

                if self._column < len(octopuses[self._row]) - 1:
                    # bottom right
                    octopuses[self._row + 1][self._column + 1].increase_energy_level(octopuses)

################################################################################

    def reset_energy_level(self) -> None:
        """
        If this octopus flashed this step, its energy level is reset.
        """

        if self._energy_level >= self.FLASH_ENERGY_LEVEL:
            self._energy_level = self.ENERGY_LEVEL_RESET

################################################################################

    @property
    def flashes_count(self) -> int:
        """
        :return: How many times this octopus flashed.
        """

        return self._flashes_count

################################################################################

    @property
    def energy_level(self) -> int:
        """
        :return: current energy level
        """

        return self._energy_level

################################################################################



################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Each octopus has an energy level - your submarine can remotely measure the
    energy level of each octopus (your puzzle input). For example:

    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526

    The energy level of each octopus is a value between 0 and 9. Here, the
    top-left octopus has an energy level of 5, the bottom-right one has an
    energy level of 6, and so on.

    You can model the energy levels and flashes of light in steps. During a
    single step, the following occurs:

    -First, the energy level of each octopus increases by 1.
    -Then, any octopus with an energy level greater than 9 flashes. This
     increases the energy level of all adjacent octopuses by 1, including
     octopuses that are diagonally adjacent. If this causes an octopus to have
     an energy level greater than 9, it also flashes. This process continues as
     long as new octopuses keep having their energy level increased beyond 9.
     (An octopus can only flash at most once per step.)
    -Finally, any octopus that flashed during this step has its energy level set
     to 0, as it used all of its energy to flash.

    Adjacent flashes can cause an octopus to flash on a step even if it begins
    that step with very little energy. Consider the middle octopus with 1 energy
    in this situation:

    Before any steps:

    11111
    19991
    19191
    19991
    11111

    After step 1:

    34543
    40004
    50005
    40004
    34543

    After step 2:

    45654
    51115
    61116
    51115
    45654

    An octopus is highlighted when it flashed during the given step.

    Here is how the larger example above progresses:

    Before any steps:

    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526

    After step 1:

    6594254334
    3856965822
    6375667284
    7252447257
    7468496589
    5278635756
    3287952832
    7993992245
    5957959665
    6394862637

    After step 2:

    8807476555
    5089087054
    8597889608
    8485769600
    8700908800
    6600088989
    6800005943
    0000007456
    9000000876
    8700006848

    After step 3:

    0050900866
    8500800575
    9900000039
    9700000041
    9935080063
    7712300000
    7911250009
    2211130000
    0421125000
    0021119000

    After step 4:

    2263031977
    0923031697
    0032221150
    0041111163
    0076191174
    0053411122
    0042361120
    5532241122
    1532247211
    1132230211

    After step 5:

    4484144000
    2044144000
    2253333493
    1152333274
    1187303285
    1164633233
    1153472231
    6643352233
    2643358322
    2243341322

    After step 6:

    5595255111
    3155255222
    3364444605
    2263444496
    2298414396
    2275744344
    2264583342
    7754463344
    3754469433
    3354452433

    After step 7:

    6707366222
    4377366333
    4475555827
    3496655709
    3500625609
    3509955566
    3486694453
    8865585555
    4865580644
    4465574644

    After step 8:

    7818477333
    5488477444
    5697666949
    4608766830
    4734946730
    4740097688
    6900007564
    0000009666
    8000004755
    6800007755

    After step 9:

    9060000644
    7800000976
    6900000080
    5840000082
    5858000093
    6962400000
    8021250009
    2221130009
    9111128097
    7911119976

    After step 10:

    0481112976
    0031112009
    0041112504
    0081111406
    0099111306
    0093511233
    0442361130
    5532252350
    0532250600
    0032240000

    After step 10, there have been a total of 204 flashes. Fast forwarding, here
    is the same configuration every 10 steps:

    After step 20:

    3936556452
    5686556806
    4496555690
    4448655580
    4456865570
    5680086577
    7000009896
    0000000344
    6000000364
    4600009543

    After step 30:

    0643334118
    4253334611
    3374333458
    2225333337
    2229333338
    2276733333
    2754574565
    5544458511
    9444447111
    7944446119

    After step 40:

    6211111981
    0421111119
    0042111115
    0003111115
    0003111116
    0065611111
    0532351111
    3322234597
    2222222976
    2222222762

    After step 50:

    9655556447
    4865556805
    4486555690
    4458655580
    4574865570
    5700086566
    6000009887
    8000000533
    6800000633
    5680000538

    After step 60:

    2533334200
    2743334640
    2264333458
    2225333337
    2225333338
    2287833333
    3854573455
    1854458611
    1175447111
    1115446111

    After step 70:

    8211111164
    0421111166
    0042111114
    0004211115
    0000211116
    0065611111
    0532351111
    7322235117
    5722223475
    4572222754

    After step 80:

    1755555697
    5965555609
    4486555680
    4458655580
    4570865570
    5700086566
    7000008666
    0000000990
    0000000800
    0000000000

    After step 90:

    7433333522
    2643333522
    2264333458
    2226433337
    2222433338
    2287833333
    2854573333
    4854458333
    3387779333
    3333333333

    After step 100:

    0397666866
    0749766918
    0053976933
    0004297822
    0004229892
    0053222877
    0532222966
    9322228966
    7922286866
    6789998766

    After 100 steps, there have been a total of 1656 flashes.

    Given the starting energy levels of the dumbo octopuses in your cavern,
    simulate 100 steps. How many total flashes are there after 100 steps?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        lines = tuple([tuple(line.strip()) for line in f.readlines()])
        octopuses = tuple([tuple([Octopus(int(lines[row][column]), row, column)
                                  for column in range(len(lines[row]))])
                           for row in range(len(lines))])

        for _ in range(STEPS):
            [octopuses[row][column].increase_energy_level(octopuses)
             for row in range(len(octopuses))
             for column in range(len(octopuses[row]))]
            [octopuses[row][column].reset_energy_level()
             for row in range(len(octopuses))
             for column in range(len(octopuses[row]))]

        # should be 1697
        print(sum([octopuses[row][column].flashes_count
                   for row in range(len(octopuses))
                   for column in range(len(octopuses[row]))]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    It seems like the individual flashes aren't bright enough to navigate.
    However, you might have a better option: the flashes seem to be
    synchronizing!

    In the example above, the first time all octopuses flash simultaneously is
    step 195:

    After step 193:

    5877777777
    8877777777
    7777777777
    7777777777
    7777777777
    7777777777
    7777777777
    7777777777
    7777777777
    7777777777

    After step 194:

    6988888888
    9988888888
    8888888888
    8888888888
    8888888888
    8888888888
    8888888888
    8888888888
    8888888888
    8888888888

    After step 195:

    0000000000
    0000000000
    0000000000
    0000000000
    0000000000
    0000000000
    0000000000
    0000000000
    0000000000
    0000000000

    If you can calculate the exact moments when the octopuses will all flash
    simultaneously, you should be able to navigate through the cavern. What is
    the first step during which all octopuses flash?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        lines = tuple([tuple(line.strip()) for line in f.readlines()])
        octopuses = tuple([tuple([Octopus(int(lines[row][column]), row, column)
                                  for column in range(len(lines[row]))])
                           for row in range(len(lines))])

        step = 0
        while any([octopuses[row][column].energy_level != Octopus.ENERGY_LEVEL_RESET
                   for row in range(len(octopuses))
                   for column in range(len(octopuses[row]))]):
            [octopuses[row][column].increase_energy_level(octopuses)
             for row in range(len(octopuses))
             for column in range(len(octopuses[row]))]
            [octopuses[row][column].reset_energy_level()
             for row in range(len(octopuses))
             for column in range(len(octopuses[row]))]
            step += 1

        # should be 344
        print(step)

################################################################################