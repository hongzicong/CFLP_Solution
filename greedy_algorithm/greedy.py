# -*- coding: utf-8 -*-

import time
import random
import math
import numpy as np

class GreedyAlgorithm:

    def __init__(self, file_name, max_iteration):
        self.J, self.I = 0, 0
        self.s_arr = []
        self.f_arr = []
        self.d_arr = []
        self.c_arr = []
        self.get_data_from_file(file_name)
        self.max_iteration = max_iteration

        self.min_result = 0
        self.min_solution = []
        self.process()

    
    def process(self):
        for iter_i in range(self.max_iteration):
            while True:
                solution = [[False] * self.I for i in range(self.J)]
                for i in range(self.I):
                    solution[random.randint(0, self.J - 1)][i] = True
                if self.is_in_cap(solution):
                    if len(self.min_solution) == 0 or self.min_result > self.fitness(solution):
                        self.min_solution = solution
                        self.min_result = self.fitness(solution)
                    break


    def get_data_from_file(self, file_name):
        with open(file_name.format(file_name_i)) as file:
            text_line = file.readline()
            self.J, self.I = map(int, text_line.split())

            for i in range(self.J):
                text_line = file.readline()
                s, f = map(int, text_line.split()[0:2])
                self.s_arr.append(s)
                self.f_arr.append(f)

            for i in range(math.ceil(self.I / 10)):
                text_line = file.readline()
                self.d_arr.extend(map(float, text_line.split()))
            
            self.d_arr = np.array(self.d_arr)

            for i in range(math.ceil(self.I * self.J / 10)):
                text_line = file.readline()
                self.c_arr.extend(map(float, text_line.split()))

            self.c_arr = np.array(self.c_arr).reshape(self.J, self.I)


    def fitness(self, solution):
        sum = 0

        if not self.is_in_cap(solution):
            return 1000000

        for j in range(self.J):
            for i in range(self.I):
                if solution[j][i]:
                    sum += self.f_arr[j]
                    break
        
        for j in range(self.J):
            for i in range(self.I):
                if solution[j][i]:
                    sum += self.c_arr[j][i]
        
        return sum


    def is_in_cap(self, solution):
        for j in range(self.J):
            max_cap = self.s_arr[j]
            cap = 0
            for i in range(self.I):
                if solution[j][i]:
                    cap += self.d_arr[i]
            if cap > max_cap:
                return False
        return True
    
    def print_best_solution(self, output_file):
        output_file.write("Cost: {}\n".format(self.min_result))

        open = [0] * self.J

        for j in range(self.J):
            for i in range(self.I):
                if self.min_solution[j][i]:
                    open[j] = 1
                    break
        
        for open_j in open:
            output_file.write("{} ".format(open_j))
        
        output_file.write("\n")
        
        for i in range(self.I):
            for j in range(self.J):
                if self.min_solution[j][i]:
                    output_file.write("{} ".format(j))
        
        output_file.write("\n")


if __name__ == "__main__":
    file_name = "../Instances/p{}"
    output_name = "./detail.txt"
    with open(output_name, "w") as output_file:
        for file_name_i in range(54, 72):
            print(file_name_i)
            time_start = time.time()
            greedy_algorithm = GreedyAlgorithm(file_name, 100)
            time_end = time.time()
            output_file.write("Case {}   Data Name: {}   Time cost: {}\n".format(file_name_i, file_name.format(file_name_i), time_end - time_start))
            greedy_algorithm.print_best_solution(output_file)