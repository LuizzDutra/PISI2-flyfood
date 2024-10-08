from typing import List, Dict
from random import randint, uniform, choices
from math import dist

POPULATION_SIZE = 2000
MAX_GEN = 300
MUTATION_CHANCE = 5
ELITISM = 90


def make_random_path(nodes: Dict[int, List[int]]) -> List[int]:
    new_vetor = list(nodes.keys())
    for i in range(len(new_vetor)):
        rand_idx = randint(i, len(new_vetor)-1)
        temp_var = new_vetor[i]
        new_vetor[i] = new_vetor[rand_idx]
        new_vetor[rand_idx] = temp_var
    return new_vetor


def mutate(vetor: List[int]) -> List[int]:
    mutation_size = randint(2, len(vetor)-1)
    i: int = randint(0, len(vetor)-mutation_size)
    j: int = i+mutation_size

    split = vetor[i:j+1]
    split.reverse()
    return vetor[:i] + split + vetor[j+1:]

def crossover(s: List[int], t: List[int]) -> List[List[int]]:
    offspring = [s[:], t[:]]
    crossover_size = randint(1, len(s))
    s_point = randint(0, len(s)-crossover_size)
    for i in range(s_point, s_point+crossover_size):
        for j in range(0, len(offspring[0])):
            if offspring[0][j] == t[i]:
                offspring[0][i], offspring[0][j] = offspring[0][j], offspring[0][i]
                break
        for j in range(0, len(offspring[0])):
            if offspring[1][j] == s[i]:
                offspring[1][i], offspring[1][j] = offspring[1][j], offspring[1][i]
                break
            
    return offspring


def get_dis(a: List[float], b: List[float], nodes: Dict[int, List[int]]):
    x = nodes[a]
    y = nodes[b]
    return dist(x, y)

def get_fit(vetor: List[int], nodes: Dict[int, List[int]]) -> int:
    fitness = get_dis(vetor[0], vetor[-1], nodes)
    for i in range(0, len(vetor)-1):
        fitness += get_dis(vetor[i], vetor[i+1], nodes)
    return 1/fitness


def start(nodes: Dict[int, List[int]]):
    #Cria população
    population: List[List[int]] = [List[int]]*POPULATION_SIZE
    for i in range(POPULATION_SIZE):
        population[i] = make_random_path(nodes)

    #Gerações
    population_fit = [int]*POPULATION_SIZE
    new_population = [int]*POPULATION_SIZE
    new_population_fit = [int]*POPULATION_SIZE

    all_time_best_fit = 0
    all_time_best_route = [List[int]]

    #fitness initialization
    for i, lone in enumerate(population):
        population_fit[i] = get_fit(lone, nodes)

    for _ in range(MAX_GEN):
         #crossover
        for i in range(0, POPULATION_SIZE, 2):
            chosen_idx = choices(range(len(population_fit)), weights=population_fit, k=2)
            offspring = crossover(population[chosen_idx[0]], population[chosen_idx[1]])
            
            #offspring mutation chance
            if uniform(0, 100) <= MUTATION_CHANCE:
                offspring[0] = mutate(offspring[0])
            if uniform(0, 100) <= MUTATION_CHANCE:
                offspring[1] = mutate(offspring[1])
            
            offspring_fit = get_fit(offspring[0], nodes), get_fit(offspring[1], nodes)


            for j in range(2):
                if offspring_fit[j] < population_fit[i+j] and uniform(0, 100) <= ELITISM:
                    new_population[i+j] = population[chosen_idx[j]]
                    new_population_fit[i+j] = population_fit[chosen_idx[j]]
                else:
                    new_population[i+j] = offspring[j]
                    new_population_fit[i+j] = offspring_fit[j]

        population = new_population
        population_fit = new_population_fit
        gen_best = max(population_fit)
        print(_)
        print(1/gen_best)
        print()
        if gen_best > all_time_best_fit:
            all_time_best_fit = gen_best
            all_time_best_route = population[population_fit.index(gen_best)]


    #Resultado final
    #end_idx = -1
    #end_fit = 0
    #for i, lone in enumerate(population):
    #    if population_fit[i] > end_fit:
    #        end_fit = population_fit[i]
    #        end_idx = i

    return all_time_best_route, 1/all_time_best_fit


if __name__ == '__main__':

    print(start({1: [5, 4], 2:[3, 2], 3:[10, 7]}))
