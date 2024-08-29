import sys
import tsplib95
from genetico import algo_genetico
from util import plot_map


def main():
    problem = tsplib95.load('berlin52.tsp')
    nodes = problem.as_keyword_dict()['NODE_COORD_SECTION']

    res = algo_genetico.start(nodes)

    print(res[1])
    plot_map.draw([nodes[i] for i in res[0]], [str(i) for i in res[0]])


if __name__ == "__main__":
    main()