# -*- coding: utf-8 -*-

import time
import random
import math
import copy
import numpy as np

class GeneticAlgorithm:

    def __init__(self, file_name):
        self.J, self.I = 0, 0
        self.s_arr = []
        self.f_arr = []
        self.d_arr = []
        self.c_arr = []
        
        self.get_data_from_file(file_name)
        self.max_iteration = 1000
        self.max_population = 100
        self.child_count = 20
        self.best_solution_arr = []

        # crossover probability
        self.p_c = 0.6

        # mutation probability
        self.p_m = 0.1

        # Each solution in the population
        # True: use False: not use
        # dimension: J x I
        self.population = [] 
        self.init_poplution(10)
        self.process(0)

    
    def process(self, selection_method = 0):
        for iter_i in range(self.max_iteration):
            
            # self.best_solution_arr.append(self.get_best_solution()[0])
            # print(self.get_best_solution()[0])
            if iter_i % 100 == 0:
                print("iteration: {}".format(iter_i))
            
            if selection_method == 0:
                # selection: tournament 
                new_population = []
                while len(new_population) < self.max_population:
                    solution_a, solution_b = random.choices(self.population, k=2)
                    win_solution = solution_a if self.fitness(solution_a) < self.fitness(solution_b) else solution_b
                    new_population.append(copy.deepcopy(win_solution))
                self.population = new_population

            elif selection_method == 1:
                # selection: roulette
                new_population = []
                fitness_sum = self.get_fitness_sum()
                fitness_arr = []
                begin = 0
                end = 0
                for solution_i in range(len(self.population)):
                    end = begin + (1 / self.fitness(self.population[solution_i])) / fitness_sum
                    fitness_arr.append([begin, end])
                    begin = end
                while len(new_population) < self.max_population - self.child_count:
                    win_i = 0
                    win_rand = random.random()
                    for fitness_arr_i in range(len(fitness_arr)):
                        if win_rand < fitness_arr[fitness_arr_i][1] and win_rand >= fitness_arr[fitness_arr_i][0]:
                            win_i = fitness_arr_i
                            break
                    new_population.append(copy.deepcopy(self.population[win_i]))
                self.population = new_population

            self.crossover()

            self.mutation()



    def get_cap_num(self):
        sum = 0
        for solution in self.population:
            if self.is_in_cap(solution):
                sum += 1
        return sum


    def get_fitness_sum(self):
        sum = 0
        for solution in self.population:
            sum += 1 / self.fitness(solution)
        return sum


    def crossover(self):
        count = 0
        while count < self.child_count:
            solution_a, solution_b = random.choices(self.population, k=2)
            cross_pos = random.randint(0, self.I - 1)
            solution_a = solution_a[:]
            solution_b = solution_b[:]
            if random.random() < self.p_c:
                for J_i in range(self.J):
                    solution_a[J_i][0:cross_pos], solution_b[J_i][0:cross_pos] = solution_b[J_i][0:cross_pos], solution_a[J_i][0:cross_pos]
            self.population.append(copy.deepcopy(solution_a))
            self.population.append(copy.deepcopy(solution_b))
            count += 2


    def mutation(self):
        for solution in self.population:
            if random.random() < self.p_m:
                I_i = random.randint(0, self.I - 1)
                for J_i in range(self.J):
                    solution[J_i][I_i] = False
                solution[random.randint(0, self.J - 1)][I_i] = True


    def init_poplution(self, init_num):
        init_i = 0
        while True:
            if init_i == init_num:
                break
            solution = [[False] * self.I for i in range(self.J)]
            for i in range(self.I):
                solution[random.randint(0, self.J - 1)][i] = True
            if self.is_in_cap(solution):
                self.population.append(solution)
                init_i += 1


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


    def get_best_solution(self):
        min_result = 0
        min_solution = []
        for solution in self.population:
            if self.is_in_cap(solution):
                if len(min_solution) == 0 or min_result < self.fitness(solution):
                    min_solution = solution
                    min_result = self.fitness(solution)
        
        return min_result, min_solution
    
    def print_best_solution(self, output_file):
        min_result, min_solution = self.get_best_solution()
        output_file.write("Cost: {}\n".format(min_result))

        open = [0] * self.J

        for j in range(self.J):
            for i in range(self.I):
                if min_solution[j][i]:
                    open[j] = 1
                    break
        
        for open_j in open:
            output_file.write("{} ".format(open_j))
        
        output_file.write("\n")
        
        for i in range(self.I):
            for j in range(self.J):
                if min_solution[j][i]:
                    output_file.write("{} ".format(j))
        
        output_file.write("\n")


if __name__ == "__main__":
    file_name = "../Instances/p{}"
    output_name = "./detail"
    with open(output_name, "w") as output_file:
        for file_name_i in range(68,72):
            time_start = time.time()
            genetic_algorithm = GeneticAlgorithm(file_name)
            time_end = time.time()
            output_file.write("Case {}   Data Name: {}   Time cost: {}\n".format(file_name_i, file_name.format(file_name_i), time_end - time_start))
            genetic_algorithm.print_best_solution(output_file)