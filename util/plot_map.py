"""Responsável por gerar os plots das soluções"""
from typing import List, Tuple
import matplotlib.pyplot as plt

LINE_COLOR = 'b'
POINT_COLOR = 'r'

def draw(points: List[Tuple], points_str: List[str]):
    """Desenha o mapa de pontos com o caminho da rota traçado"""
    x_coords = [i[0] for i in points]
    y_coords = [i[1] for i in points]

    plt.plot(x_coords, y_coords, LINE_COLOR)
    #Plota a volta ao último ponto
    plt.plot([x_coords[-1], x_coords[0]], [y_coords[-1], y_coords[0]], LINE_COLOR)

    plt.scatter(x_coords, y_coords, c=POINT_COLOR)

    for i in range(len(points)):
        plt.text(x_coords[i], y_coords[i], points_str[i], fontsize="large",
                 verticalalignment="bottom")

    plt.show()


if __name__ == "__main__":
    #Rota ótima do flyfood
    rota_str = ["R", "A", "G", "D", "C", "E", "F", "B"]
    rota = [(3, 0), (1, 1), (0, 2), (0, 4), (2, 4), (1, 3), (1, 2), (3, 2)]

    draw(rota, rota_str)
