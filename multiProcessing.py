import multiprocessing as mp
from itertools import product
import random
import time
import section1_ga as sga
import clsTimeTable as table_sem


class CLASHVERIFICATION(object):
    '''
    Class representing individual in population
    '''
    cnt = 0

    def __init__(self, chromosome):     #54*6
        for i in range(len(chromosome)):
            for j in range(len(chromosome[i])):
                if(chromosome[i][j] == ' '):
                    chromosome[i][j] = str(CLASHVERIFICATION.cnt)
                    CLASHVERIFICATION.cnt += 1
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    def cal_fitness(self):
        xfitness = 0
        time_table_list = self.chromosome
        for values in zip(*time_table_list):        #convert to 1 dim    
            n = len(values)                         #n = 6 classes.
            m = len(set(values))                    #m = dist teachers.
            xfitness += (n - m)                     #if no clashes.

        teachers_names = []                 #teacher hectic schedule check
        for i in time_table_list:
            for x in i:
                if(not x.isdigit()):
                    teachers_names.append(x)

        teachers_names = list(set(teachers_names))

        for teacher in teachers_names:
            start = -1
            for i in range(54):
                for j in range(len(time_table_list)):       #len = 6 days and 9 classes.
                    if(time_table_list[j][i] == teacher):
                        start = i
                        break
                if(start != -1):
                    break

            end = 1
            for i in range(53, -1, -1):
                for j in range(len(time_table_list)):
                    if(time_table_list[j][i] == teacher):
                        end = i
                        break

            if(end - start >= 7):           #more than 7hrs should not be there for a faculty
                xfitness += 50

        return xfitness

    def change(self):
        found = False
        for j in range(54):
            set1 = set()
            for i in range(6):
                n = len(set1)
                set1.add(self.chromosome[i][j])
                if(n == len(set1)):
                    found = True
                    break
            if(found):
                break

        k = j // 9
        start = 0
        end = 0
        for k in range(9):
            if(not self.chromosome[i][k].isdigit()):
                start = k
                break

        for k in range(8, -1, -1):
            if(not self.chromosome[i][k].isdigit()):
                end = k
                break

        for k in range(start, end + 1):
            temp = self.chromosome[i][k], self.chromosome[i][j]
            self.chromosome[i][j], self.chromosome[i][k] = temp
            if(self.cal_fitness() == 0):
                self.fitness = 0
                return
            temp = self.chromosome[i][k], self.chromosome[i][j]
            self.chromosome[i][j], self.chromosome[i][k] = temp

        cls_tech = self.chomosome[i][j]
        for k in range(i - 1, -1, -1):
            if(self.chromosome[k][j] == cls_tech):
                break

        i = k
        k = j // 9
        start = 0
        end = 0
        for k in range(9):
            if(not self.chromosome[i][k].isdigit()):
                start = k
                break

        for k in range(8, -1, -1):
            if(not self.chromosome[i][k].isdigit()):
                end = k
                break

        for k in range(start, end + 1):
            temp = self.chromosome[i][k], self.chromosome[i][j]
            self.chromosome[i][j], self.chromosome[i][k] = temp
            swap(self.chromosome[i][k], self.chromosome[i][j])
            if(self.cal_fitness() == 0):
                self.fitness = 0
                return
            temp = self.chromosome[i][k], self.chromosome[i][j]
            self.chromosome[i][j], self.chromosome[i][k] = temp

        return


section1 = ""


def read_file():
    sections_list = []
    teachers_list = []
    credits_list = []
    with open("class_teachers.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            sections, teachers, credits = line.split("$")
            teachers = teachers.split()
            credits = list(map(int, credits.split()))

            sections_list.append(sections)
            teachers_list.append(teachers)
            credits_list.append(credits)

    return sections_list, teachers_list, credits_list


def find_sectionTimeTable(sec, teachers, credits):
    global section1

    while(True):
        section1 = sga.TEMPLATE(sec, teachers, credits)

        ans, fitness = section1.calculateSectionTimeTable()

        # print(fitness)

        if(ans != -1):
            return ans

        # print("BAD Chromosome")


def clash_teachers(time_table_list):
    for j in range(54):
        set1 = set()
        for i in range(6):
            n = len(set1)
            set1.add(time_table_list[i][j])
            if(n == len(set1)):
                print(time_table_list[i][j], ord(time_table_list[i][j]) - 64, j)


def create_time_table(valdict, sections_list, teachers_list, credits_list):
    # sections_all[2], teachers_list, credits_list = read_file()
    # print(sections_all[2])
    for i in range(len(sections_list)):
        x = list(zip(teachers_list[i], credits_list[i]))
        random.shuffle(x)
        x = list(zip(*x))
        teachers_list[i] = list(x[0])
        credits_list[i] = list(x[1])

    time_table_list = []        #for all sections.
    for i in range(len(teachers_list)):
        time_table = find_sectionTimeTable(sections_list[i], teachers_list[i], credits_list[i])
        time_table_list.append(time_table)

    valdict[random.randint(1, 1000)] = time_table_list


def display(time_table, section):
    global section1
    section1 = sga.TEMPLATE(0, [], [])

    print()
    print(section.center(45))
    print()

    time_table = section1.reverse_dictionary(time_table)

    for i in range(6):
        for j in range(9):
            print(time_table[i * 9 + j].center(5), end="")
        print()


def print_time_table1(value):
    # for key, value in time_table.items():
    #     print("         ", key)
    #     print()
    for i in value:
        for j in i:
            if(j == 'A1' or j == 'B1'):
                print("PMS".center(5), end="")
            elif(j == 'A2' or j == 'B2'):
                print("AMC".center(5), end="")
            elif(j == 'A4' or j == 'B4'):
                print("BTP".center(5), end="")
            else:
                print(str(j).center(5), end="")
        print()
    print()


def main():

    start = time.time()
    table_population = []

    sections_list, teachers_list, credits_list = read_file()

    manager = mp.Manager()
    valdict = manager.dict()
    # sections_all = manager.dict()

    jobs = []

    for i in range(4):
        p = mp.Process(target=create_time_table, args=(valdict, sections_list, teachers_list, credits_list, ))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    sample_population = []

    for value in valdict.values():
        sample_population.append(value)

    total_population = 4096

    # print("After multiprocessing", time.time()-start)

    a = [0, 1, 2, 3]        #different processes.
    for indexs in list(product(a, repeat=6)):
        temp_population = []
        for i, ind in enumerate(indexs):
            temp_population.append(sample_population[ind][i])
        table_population.append(CLASHVERIFICATION(temp_population))
        if(table_population[-1].fitness == 0):
            break

    # print("After 4096", time.time()-start)
    # print(len(table_population))

    # for population in sorted(table_population, key=lambda x: x.fitness)[:100]:
    #     print(population.fitness, end="  ")

    # 10% of total population
    total_population = 100
    table_population = sorted(table_population, key=lambda x: x.fitness)[:total_population]

    idx = 0
    while(table_population[0].fitness):
        table_population[0] = table_population[idx]
        table_population[0].change()
        idx += 1

    for i in range(len(sections_list)):
        display(table_population[0].chromosome[i], sections_list[i])

    # print(table_population[0].fitness)

    clash_teachers(table_population[0].chromosome)

    time_table_7 = table_sem.fun()

    print()
    print("7A".center(45))
    print()
    print_time_table1(time_table_7['7A'])
    
    print("7B".center(45))
    print()
    print_time_table1(time_table_7['7B'])

    print("\nTotal time taken is ", time.time() - start)


if __name__ == '__main__':
    main()
