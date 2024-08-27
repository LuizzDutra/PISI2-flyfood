from typing import List, Dict
from random import randint, uniform
import tsplib95

POPULATION_SIZE = 100
MAX_GEN = 100


def make_random_path(nodes: Dict[int, List[int]]) -> List[int]:
    new_vetor = list(nodes.keys())
    for i in range(len(new_vetor)):
        rand_idx = randint(i, len(new_vetor)-1)
        temp_var = new_vetor[i]
        new_vetor[i] = new_vetor[rand_idx]
        new_vetor[rand_idx] = temp_var
    return new_vetor


def mutate(vetor: List[int]) -> List[int]:
    i: int = randint(0, len(vetor)-2)
    j: int = randint(i+1, len(vetor))

    split = vetor[i:j+1]
    split.reverse()
    return vetor[:i] + split + vetor[j+1:]

def get_dis(a: List[float], b: List[float], nodes: Dict[int, List[int]]):
    x = nodes[a]
    y = nodes[b]
    return ((x[0] - y[0])**2 + (x[1] - y[1])**2)**(1/2)

def get_fit(vetor: List[int], nodes: Dict[int, List[int]]) -> int:
    fitness = get_dis(vetor[0], vetor[-1], nodes)
    for i in range(0, len(vetor)-1):
        fitness += get_dis(vetor[i], vetor[i+1], nodes)
    return 1/fitness

def get_chosen(population_fit: List[int]) -> int:
    fit_sum = sum(population_fit)
    point = uniform(0, 1)
    search_sum = 0
    for i, fit in enumerate(population_fit):
        search_sum += fit/fit_sum
        if point <= search_sum:
            return i
    return -1


def main():
    problem = tsplib95.load('berlin52.tsp')
    nodes: Dict = problem.as_keyword_dict()['NODE_COORD_SECTION']

    #Cria população
    population: List[List[int]] = [int]*POPULATION_SIZE
    for i in range(POPULATION_SIZE):
        population[i] = make_random_path(nodes)

    #Gerações
    population_fit = [int]*len(population)
    new_population = [int]*POPULATION_SIZE
    for _ in range(MAX_GEN):
        for i, lone in enumerate(population):
            population_fit[i] = get_fit(lone, nodes)

        for i in range(POPULATION_SIZE):
            chosen_idx = get_chosen(population_fit)
            new_population[i] = mutate(population[chosen_idx])
        population = new_population
    
    #Resultado final
    for i, lone in enumerate(population):
            population_fit[i] = get_fit(lone, nodes)
    print(sorted(population_fit)[0]**(-1))









if __name__ == '__main__':
    main()
