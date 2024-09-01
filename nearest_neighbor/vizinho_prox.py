"""Código que vai ler um arquivo com pontos de distâncias e
 informa possivelmente o menor caminho,
usa a heuristica do vizinho mais próximo"""

from random import choice


# FUNÇÕES DE CALCULO DE DISTÃNCIA ENTRE DOIS PONTOS
def distance_2d(ponto1, ponto2):
    """Função que calcula a distância entre 2 pontos euclidianos,
    retorna qual o ponto de chegada e a distância entre eles"""
    xd = float(ponto1[1]) - float(ponto2[1])
    yd = float(ponto1[2]) - float(ponto2[2])
    dist = round((xd**2 + yd**2) ** 0.5)
    return ponto2[0], dist


# FUNÇÕES GENÉRICAS
def somatorio_dist(lista):
    """Vai receber uma lista e vai somar todos os
    segundos elementos, vai dar o total das distâncias"""
    soma_caminhos = 0
    for x in lista:
        soma_caminhos += x
    return soma_caminhos


def calcular_distancia(tipo, nodes):
    """Faz o cálculo da distancia referente ao tipo, recebe uma string e lista de tuplas,
    as tuplas correspondem a chave e valores,
    e retorna uma lista com tuplas(CHAVE, DISTANCIA) que vão guardar chaves
    que indicam os pontos, e a distância é do ponto anterior até o atual"""

    visitados = [choice(nodes)]  # Definindo o ponto inicial
    nao_visitados = [
        x for x in nodes if x[0] != visitados[0][0]
    ]  # Listando o restante dos pontos
    # Lista que guarda keys e as distancias percorridas
    lista_distancias = []

    # Loop que só para quando todos os pontos forem percorridos
    while nao_visitados != []:
        # Lista temporária das distâncias entre o ponto de partida e todos os não percorridos
        lista_pontos = {}
        for x in nao_visitados:
            # Chamando a função corresponde ao tipo com o inicial e a iteração do for
            if tipo == "EUC_2D":
                distancia = distance_2d(visitados[-1], x)
            # Guardando tds distancias temporariamente
            lista_pontos[distancia[0]] = distancia[1]

        # Após todas as distâncias serem calculadas escolhe a menor
        menor_distancia = min(lista_pontos.values())
        # Encontrando a chave correspondente ao menor valor
        chave_da_menor = [
            x for x, valor in lista_pontos.items() if valor == menor_distancia
        ]
        # Coloca na lista de distâncias o ponto de chegada e a distância para ele
        lista_distancias += [(menor_distancia)]

        # Adiciona na lista de visitados o ponto que possui a chave correspondente a menor
        visitados += [x for x in nao_visitados if x[0] == chave_da_menor[0]]

        # Remove da lista de nao visitados o ponto que possui menor caminho
        nao_visitados = [x for x in nao_visitados if x[0] != chave_da_menor[0]]

    # Distancia do ponto final para o inicial(TEMPORÁRIO)
    dis_ate_inicio = distance_2d(visitados[-1], visitados[0])
    lista_distancias += [dis_ate_inicio[1]]

    return lista_distancias, visitados


# FUNÇÃO COM CÓDIGO MAIN
def run():
    """Função que vai executar todo o código"""

    with open("nearest_neighbor/mapa.txt", encoding="utf-8") as arquivo:
        linha = arquivo.readline().split()
        # Listando as palavras chaves que indicam inicio de fornecimento de dados
        keyword = "NODE_COORD_SECTION"
        # Verificando qual o tipo de ponto que será dado até chegar na sessão de dados
        tipo_de_pontos = None
        while linha[0] != keyword:
            if linha[0] == "EDGE_WEIGHT_TYPE:" or linha[0] == "EDGE_WEIGHT_TYPE":
                tipo_de_pontos = linha[-1]
            linha = arquivo.readline().split()

        # Guardando todas as linhas de dados em formato de tupla(por enquanto)
        pontos = []
        linha = arquivo.readline().split()

        while linha[0] != "EOF":
            # Transforma as coordenadas
            linha = [linha[0]] + [float(x) for x in linha[1:]]
            pontos += [tuple(linha)]
            linha = arquivo.readline().split()

    # Chamada que vai passar uma string com tipo de pontos e uma lista de tuplas
    duas_listas = calcular_distancia(tipo_de_pontos, pontos)
    # A primeira lista se refere distancias
    # A segunda lista se refere a chaves e coordenadas

    # Chamada que vai pegar todas a lista de tuplas e somar as distâncias
    saida = somatorio_dist(duas_listas[0])

    # print(duas_listas[1])
    # print(saida)

    return duas_listas[1], saida


if __name__ == "__main__":
    run()
