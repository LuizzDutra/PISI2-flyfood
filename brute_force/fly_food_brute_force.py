"""Algoritmo de força bruta para encontrar a rota de custo mínimo"""
from typing import List, Tuple, Dict #Para documentação

def calc_dist(pt1: Tuple[int, int], pt2: Tuple[int, int]) -> int:
    """Cálculo da distancia entre dois pontos"""
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

def calc_dist_rota(rota: List[str], pontos: Dict[str, Tuple[int, int]],
                   r: Tuple[int, int]) -> int:
    """Cálculo da distância total da rota"""
    #cálculo de ida ao primeiro ponto
    dist: int = calc_dist(r, pontos[rota[0]])
    #cálculo do caminho entre os pontos
    for i in range(1, len(rota)):
        dist += calc_dist(pontos[rota[i]], pontos[rota[i-1]])
    #cálculo de volta ao ponto R
    dist += calc_dist(pontos[rota[-1]], r)

    return dist

def permutar(pontos: List[str], start: int, r: Tuple[int, int],
             coord: Dict[str, Tuple[int, int]]) -> List[str]:
    """Calcula as rotas recursivamente"""
    if start == len(pontos)-1:
        return pontos[:]

    menor_rota: List[str] = []
    menor_dist: int = -1
    temp_dist: int
    rota: List[str]
    for i in range(start, len(pontos)):
        pontos[start], pontos[i] = pontos[i], pontos[start]
        rota = permutar(pontos, start+1, r, coord)
        pontos[start], pontos[i] = pontos[i], pontos[start]
        temp_dist = calc_dist_rota(rota, coord, r)
        if temp_dist < menor_dist or menor_dist == -1:
            menor_dist = temp_dist
            menor_rota = rota
    return menor_rota

def main():
    """Função principal que lê o arquivo de entrada e aplica o algoritmo"""
    #Entradas são computadas considerando que são válidas
    with open('entrada.txt', 'r', encoding='utf-8') as f:
        n: int
        m: int
        n, m = [int(i) for i in f.readline().split(' ')]

        matriz: List[List[str]] = [List[str]]*n
        for i in range(n):
            matriz[i] = f.readline().split(' ')
            #remoção do caractere newline
            if matriz[i][-1][-1] == '\n':
                matriz[i][-1] = matriz[i][-1][:-1]

    #Localiza os pontos
    pontos: Dict[Tuple[int, int]] = dict() #dicionário de pontos -> {A : (x,y)}
    r: Tuple[int, int] = (-1, -1)
    for i in range(n):
        for j in range(m):
            if matriz[i][j] == 'R':
                r = (i, j)
            elif matriz[i][j] != '0':
                pontos[matriz[i][j]] = (i, j)

    menor_rota: List[str] = permutar(list(pontos.keys()), 0, r, pontos)
    menor_dist = calc_dist_rota(menor_rota, pontos, r)
    #Criação da string resultado
    resultado: str = ""
    for i in menor_rota:
        resultado += i + ' '
    print(resultado[:-1])
    print(menor_dist)

if __name__ == "__main__":
    main()
