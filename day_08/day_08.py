__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join

"""
--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave 
mouth, collapsing it. Sensors indicate another exit to this cave at a much 
greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that 
the four-digit seven-segment displays in your submarine are malfunctioning; they 
must have been damaged during the escape. You'll be in a lot of trouble without 
them, so you'd better figure out what's wrong.
"""

################################################################################

SELF_DIR_NAME = "day_08"
INPUT_TXT_NAME = "input.txt"
SEPARATOR = "|"

################################################################################

def decode_entry(entry: str) -> int:
    """
    :param entry: consists of ten unique signal patterns, a | delimiter, and
    finally the four digit output value
    :return: four-digit output value for the entry
    """

    input_patterns = tuple(map(
        lambda pattern: "".join(sorted(pattern)),
        entry.split(SEPARATOR)[0].strip().split(" ")))
    output_values = tuple(map(
        lambda value: "".join(sorted(value)), entry.split(SEPARATOR)[1].strip().split(" ")))
    # we start with no idea which signal (letter [a-g]) goes to which segment
    segments = ["abcdefg", "abcdefg", "abcdefg", "abcdefg", "abcdefg", "abcdefg", "abcdefg"]

    # number 1
    # pattern is known, it's the only one with two segments
    pattern_1 = tuple(filter(lambda pattern: len(pattern) == 2, input_patterns))[0]
    # we cannot tell the difference between top and bottom right segments at
    # this point
    segments[2] = pattern_1
    segments[5] = pattern_1
    for char in pattern_1:
        segments = list(map(
            lambda segment: segment.replace(char, "")
            if segment != pattern_1 else pattern_1, segments))

    # number 4
    # pattern is known, it's the only one with four segments
    pattern_4 = tuple(filter(lambda pattern: len(pattern) == 4, input_patterns))[0]
    # we can get the top left and middle segments, it's the two which are
    # not in the pattern for number 1
    # we cannot tell the difference between top left and middle segments at
    # this point
    pattern_4_part = "".join(sorted(set(pattern_4).symmetric_difference(pattern_1)))
    segments[1] = pattern_4_part
    segments[3] = pattern_4_part
    for char in pattern_4_part:
        segments = list(map(
            lambda segment: segment.replace(char, "")
            if segment != pattern_4_part else pattern_4_part, segments))

    # number 7
    # pattern is known, it's the only one with three segments
    pattern_7 = tuple(filter(lambda pattern: len(pattern) == 3, input_patterns))[0]
    # top segment is the one which is not in the pattern for number one
    top_segment = "".join(set(pattern_1).symmetric_difference(pattern_7))
    segments[0] = top_segment
    segments = list(map(
        lambda segment: segment.replace(top_segment, "")
        if segment != top_segment else top_segment, segments))

    # numbers 2, 3 and 5 - five segments patterns
    patterns_235 = tuple(filter(lambda pattern: len(pattern) == 5, input_patterns))
    # top, middle and bottom segments are common between patterns for
    # numbers 2, 3 and 5
    common_segments = "".join(char for char in patterns_235[0]
                              if all([char in pattern for pattern in
                                      patterns_235]))
    # the partial pattern for number 4 (top left and middle segments)
    # contains only one of the common segments between patterns for numbers
    # 2, 3 and 5 - the middle segment
    middle_segment = "".join(set(pattern_4_part).intersection(common_segments))
    segments[3] = middle_segment
    segments = list(map(
        lambda segment: segment.replace(middle_segment, "")
        if segment != middle_segment else middle_segment, segments))
    # now that we know the top and middle segments, we can isolate the
    # bottom one
    bottom_segment = common_segments.replace(top_segment, "").replace(middle_segment, "")
    segments[6] = bottom_segment
    segments = list(map(
        lambda segment: segment.replace(bottom_segment, "")
        if segment != bottom_segment else bottom_segment, segments))

    # numbers 0, 6 and 9 - six segments patterns
    patterns_069 = tuple(filter(lambda pattern: len(pattern) == 6, input_patterns))
    # we can isolate the pattern for number 6, it's the only one which
    # does not contain the full pattern for number 1
    pattern_6 = tuple(filter(lambda pattern: any([char not in pattern for char in pattern_1]), patterns_069))[0]
    # finally we can isolate bottom right segment - it's the one which is
    # in both number 6 pattern and number 1 pattern
    bottom_right_segment = "".join(set(pattern_6).intersection(pattern_1))
    segments[5] = bottom_right_segment
    segments = list(map(
        lambda segment: segment.replace(bottom_right_segment, "")
        if segment != bottom_right_segment else bottom_right_segment, segments))

    patterns = {
        "".join(sorted(segments[0] + segments[1] + segments[4] + segments[6] + segments[5] + segments[2])): 0,
        "".join(sorted(segments[2] + segments[5])): 1,
        "".join(sorted(segments[0] + segments[2] + segments[3] + segments[4] + segments[6])): 2,
        "".join(sorted(segments[0] + segments[2] + segments[3] + segments[5] + segments[6])): 3,
        "".join(sorted(segments[1] + segments[3] + segments[2] + segments[5])): 4,
        "".join(sorted(segments[0] + segments[1] + segments[3] + segments[5] + segments[6])): 5,
        "".join(sorted(segments[0] + segments[1] + segments[3] + segments[5] + segments[6] + segments[4])): 6,
        "".join(sorted(segments[0] + segments[2] + segments[5])): 7,
        "".join(sorted("".join(segments))): 8,
        "".join(sorted(segments[0] + segments[1] + segments[2] + segments[3] + segments[5] + segments[6])): 9
    }

    return int("".join(str(patterns[output_value]) for output_value in output_values))

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Each digit of a seven-segment display is rendered by turning on or off any
    of seven segments named a through g:

      0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

      5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg

    So, to render a 1, only segments c and f would be turned on; the rest would
    be off. To render a 7, only segments a, c, and f would be turned on.

    The problem is that the signals which control the segments have been mixed
    up on each display. The submarine is still trying to display numbers by
    producing output on signal wires a through g, but those wires are connected
    to segments randomly. Worse, the wire/segment connections are mixed up
    separately for each four-digit display! (All of the digits within a display
    use the same connections, though.)

    So, you might know that only signal wires b and g are turned on, but that
    doesn't mean segments b and g are turned on: the only digit that uses two
    segments is 1, so it must mean segments c and f are meant to be on. With
    just that information, you still can't tell which wire (b/g) goes to which
    segment (c/f). For that, you'll need to collect more information.

    For each display, you watch the changing signals for a while, make a note of
    all ten unique signal patterns you see, and then write down a single four
    digit output value (your puzzle input). Using the signal patterns, you
    should be able to work out which pattern corresponds to which digit.

    For example, here is what you might see in a single entry in your notes:

    acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
    cdfeb fcadb cdfeb cdbaf

    (The entry is wrapped here to two lines so it fits; in your notes, it will
    all be on a single line.)

    Each entry consists of ten unique signal patterns, a | delimiter, and
    finally the four digit output value. Within an entry, the same wire/segment
    connections are used (but you don't know what the connections actually are).
    The unique signal patterns correspond to the ten different ways the
    submarine tries to render a digit using the current wire/segment
    connections. Because 7 is the only digit that uses three segments, dab in
    the above example means that to render a 7, signal lines d, a, and b are on.
    Because 4 is the only digit that uses four segments, eafb means that to
    render a 4, signal lines e, a, f, and b are on.

    Using this information, you should be able to work out which combination of
    signal wires corresponds to each of the ten digits. Then, you can decode the
    four digit output value. Unfortunately, in the above example, all of the
    digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and
    are more difficult to deduce.

    For now, focus on the easy digits. Consider this larger example:

    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
    fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
    fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
    cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
    efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
    gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
    gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
    cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
    ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
    gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
    fgae cfgab fg bagce

    Because the digits 1, 4, 7, and 8 each use a unique number of segments, you
    should be able to tell which combinations of signals correspond to those
    digits. Counting only digits in the output values (the part after | on each
    line), in the above example, there are 26 instances of digits that use a
    unique number of segments (highlighted above).

    In the output values, how many times do digits 1, 4, 7, or 8 appear?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        patterns = tuple([line for line in f.readlines()])
        output_values = tuple([pattern.split(SEPARATOR)[1].strip()
                               for pattern in patterns])

        digits_1478_count = sum([len([
            value for value in output_value
            if len(value) == 2
               or len(value) == 4
               or len(value) == 3
               or len(value) == 7])
            for output_value in map(
                lambda output_values: output_values.split(" "), output_values)])

    # should be 261
    print(digits_1478_count)

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Through a little deduction, you should now be able to determine the
    remaining digits. Consider again the first example above:

    acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
    cdfeb fcadb cdfeb cdbaf

    After some careful analysis, the mapping between signal wires and segments
    only make sense in the following configuration:

     dddd
    e    a
    e    a
     ffff
    g    b
    g    b
     cccc

    So, the unique signal patterns would correspond to the following digits:

    acedgfb: 8
    cdfbe: 5
    gcdfa: 2
    fbcad: 3
    dab: 7
    cefabd: 9
    cdfgeb: 6
    eafb: 4
    cagedb: 0
    ab: 1

    Then, the four digits of the output value can be decoded:

    cdfeb: 5
    fcadb: 3
    cdfeb: 5
    cdbaf: 3

    Therefore, the output value for this entry is 5353.

    Following this same process for each entry in the second, larger example
    above, the output value of each entry can be determined:

    fdgacbe cefdb cefbgd gcbe: 8394
    fcgedb cgb dgebacf gc: 9781
    cg cg fdcagb cbg: 1197
    efabcd cedba gadfec cb: 9361
    gecf egdcabf bgf bfgea: 4873
    gebdcfa ecba ca fadegcb: 8418
    cefg dcbef fcge gbcadfe: 4548
    ed bcgafe cdgba cbgef: 1625
    gbdfcae bgc cg cgb: 8717
    fgae cfgab fg bagce: 4315

    Adding all of the output values in this larger example produces 61229.

    For each entry, determine all of the wire/segment connections and decode the
    four-digit output values. What do you get if you add up all of the output
    values?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        entries = tuple([line.strip() for line in f.readlines()])
        # should be 987553
        print(sum([decode_entry(entry) for entry in entries]))

################################################################################