import tsplib95
from util import plot_map


def main():
    problem = tsplib95.load('berlin52.tsp')
    nodes = problem.as_keyword_dict()['NODE_COORD_SECTION']

    res_str = "36 39 40 37 38 48 24 5 15 6 4 25 12 28 26 47 27 13 14 52 11 51 33 43 10 9 8 41 19 45 32 49 1 22 31 18 3 17 21 42 7 2 30 23 20 50 29 16 46 44 34 35"
    res = [int(i) for i in res_str.split()]

    print(res)
    plot_map.draw([nodes[i] for i in res], res)


if __name__ == "__main__":
    main()