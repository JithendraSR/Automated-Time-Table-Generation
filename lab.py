  """To create a time table for labs"""
import random


def generate_dict(sections):
	"""To create a dictionary for storing number of labs for each sem"""
	labs = dict()
	for section in sections:
		if(section.startswith('3')):    # 3rd sem
			labs[section] = 3
		elif(section.startswith('5')):  # 5th sem
			labs[section] = 2
		else:                           # 7th sem
			labs[section] = 1

	return labs


def create_lab_table(sections, lab_table):
	"""To create the final time table for labs for all semesters"""
	max_labs = generate_dict(sections)

	# print(max_labs)
	# random_value_day = random.randint(6)

		# print(lab_table)
	lab_table[5][2] = -1 #Slot is free on Saturday
	#Assigning for 7th sem

	x = random.randint(0, 1)
	y = 1 - x

	lab_table[4+x][0] = "7A"
	lab_table[4+y][0] = "7B"
	max_labs["7A"]-=1
	max_labs["7B"]-=1

	list5 = ["5A","5B","5C"] #For choosing random values
	list3 = ["3A","3B","3C"]

	for day in range(6):  # for all days 
		if(day < 4):
			random_value_slot = random.randint(0, len(list5)-1)
			lab_table[day][random_value_slot] = list5[random_value_slot]
			max_labs[list5[random_value_slot]] -= 1
			if(not max_labs[list5[random_value_slot]]):
				list5.pop(random_value_slot)
		else:
			random_value_slot = random.randint(0, len(list5)-1)
			lab_table[day][1] = list5[random_value_slot]
			max_labs[list5[random_value_slot]] -= 1
			if(not max_labs[list5[random_value_slot]]):
				list5.pop(random_value_slot)


	list3 = list3*3
	# k = 0
	for day in range(6):
		for slot in range(3):
			if(not lab_table[day][slot]):
				lab_table[day][slot] = list3.pop()
				

def store_table(lab_table):
	with open('lab_timing.txt', 'w') as f:
		for i in range(6):
			for j in range(3):
				f.write(str(lab_table[i][j]))
				f.write(" ")
			f.write('\n')

	

def print_table(lab_table):
	for i in range(6):
		for j in range(3):
			print(f"{lab_table[i][j]}", end="  ")
		print()


def main():
	sections = ['3A', '3B', '3C',
	 			'5A', '5B', '5C',
	 			'7A', '7B']

	lab_table = [[None for i in range(3)] for j in range(6)]

	create_lab_table(sections, lab_table)

	print_table(lab_table)

	store_table(lab_table)


if __name__ == '__main__':
	main()