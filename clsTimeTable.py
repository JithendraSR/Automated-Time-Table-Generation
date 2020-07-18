"""To create time table for each class"""

import random


def swap(a, b):
    a, b = b, a


def shuffle(s, numOfClasses):
    """For Dynamic values of timetable"""
    random.seed(7)
    section = [s + str(i + 1) for i in range(numOfClasses)]
    section *= 2
    random.shuffle(section)
    section *= 2
    return section


def optimizing_clashes_7th(time_table):
    """Rotating the time table"""
    section = ""
    if(time_table['7A'][3][1] == 'TT'):
        section = "7A"
    else:
        section = "7B"

    # for saturday class
    for i in range(3):
        time_table[section][5][i], time_table[section][5][i + 3] = \
            time_table[section][5][i + 3], time_table[section][5][i]

    # for afternoon last class
    for i in range(3, 6):
        time_table[section][i][3], time_table[section][i][5] = \
            time_table[section][i][5], time_table[section][i][3]


def make_7thsem_time_table(time_table):
    # for tutorials
    sections = ['7A', '7B']
    for section in sections:
        indexes = [(ix, iy) for ix, day in enumerate(time_table[section])
                   for iy, clss in enumerate(day) if(clss == section)]
        for i, j in indexes:
            time_table[section][i - 1][j] = 'TT'

    # for actual classes
    sectionA = shuffle('A', 4)
    sectionB = shuffle('B', 4)

    # remove elective classes
    sectionA = list(filter(lambda a: a != 'A3', sectionA))
    sectionB = list(filter(lambda a: a != 'B3', sectionB))

    # assign elective classes
    for section in sections:
        for day in range(3, 5):
            for slot in range(6, 8):
                time_table[section][day][slot] = 'EL'

    # print(sectionA)
    # print(sectionB)

    # assign regular classes
    sectionAB = [sectionA, sectionB]

    for idx, section in enumerate(sections):
        for day in range(3, 6):
            for slot in range(8):
                if(not time_table[section][day][slot + 1].startswith(('7', 'T'))):
                    if(time_table[section][day][slot] == '-1'):
                        time_table[section][day][slot] = sectionAB[idx].pop()
                if(len(sectionAB[idx]) == 0):
                    break

    optimizing_clashes_7th(time_table)


def print_time_table(time_table):
    for key, value in time_table.items():
        print("         ", key)
        print()
        for i in value:
            for j in i:
                print(j, end="  ")
            print()
        print()
        print()


def fun():
    lab_table = []
    with open("lab_timing.txt", 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]

    for line in lines:
        lab_table.append(line.split())

    # print(lab_table)

    time_table = dict()
    classes = ['3A', '3B', '3C', '5A', '5B', '5C', '7A', '7B']

    for clss in classes:
        temp = [[str(-1) for i in range(9)] for i in range(6)]
        time_table[clss] = temp

    for day_idx, day in enumerate(lab_table):
        for clss_idx, clss in enumerate(day):
            if(clss != '-1'):
                for i in range(clss_idx * 3, (clss_idx + 1) * 3):
                    time_table[clss][day_idx][i] = clss
                    if(not clss.startswith('3') and (i == 0 or i == 8)):
                        time_table[clss][day_idx][i] = -1

    make_7thsem_time_table(time_table)

    # print_time_table(time_table)
    return time_table


def main():
    print("")


if __name__ == '__main__':
    main()
