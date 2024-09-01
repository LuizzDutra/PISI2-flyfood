"""Código que pega os pontos e distância total do código 'vizinho_prox' e
   fornece ao 'plot_map que trasnforma numa saída visual'"""

from util import plot_map
from nearest_neighbor import vizinho_prox


def main():
    """Recebe do vizinho_prox.py dois valores o primeiro é uma lista,
    contém as chaves e coordenadas organizado na ordem que foram percorridos,
    e o segundo é um inteiro que mostra o tamanho total do percurso"""
    # Roda o codigo e recebe suas saídas
    res = vizinho_prox.run()
    # Mostra a dist total
    print(f"Distância total: {res[1]}")
    # Transforma em visual recebendo os parametros de pontos, chaves
    plot_map.draw([(x[1], x[2]) for x in res[0]], [(x[0]) for x in res[0]])


if __name__ == "__main__":
    main()
