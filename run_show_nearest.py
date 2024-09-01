from nearest_neighbor import vizinho_prox_first_random
from util import plot_map

def main():
    """Recebe a lista com os indices e coordenadas do código e cria o mapa"""
    res = vizinho_prox_first_random.principal()
    plot_map.draw([tuple([x[1], x[2]]) for x in res], [str(i[0]) for i in res])

if __name__ == "__main__":
    main()
