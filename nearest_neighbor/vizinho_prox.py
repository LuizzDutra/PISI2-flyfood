from math import cos, acos

arquivo = open("nearest_neighbor/mapa.txt", encoding="utf-8")
linha = arquivo.readline().split()
# Listando as palavras chaves que indicam inicio de fornecimento de dados
keywords = [
    "NODE_COORD_SECTION",
    "DEPOT_SECTION",
    "DEMAND_SECTION",
    "EDGE_DATA_SECTION",
    "FIXED_EDGES_SECTION",
    "DISPLAY DATA SECTION ",
    "TOUR_SECTION",
    "EDGE_WEIGHT_SECTION",
]
# Verificando qual o tipo de ponto que será dado até chegar na sessão de dados
tipo_de_pontos = None
while linha[0] not in keywords:
    if linha[0] == "EDGE_WEIGHT_TYPE:":
        tipo_de_pontos = linha[1]
    elif linha[0] == "EDGE_WEIGHT_FORMAT":
        pass
    elif linha[0] == "EDGE_DATA_FORMAT":
        pass
    elif linha[0] == "NODE_COORD_TYPE:":
        pass
    elif linha[0] == "DISPLAY_DATA_TYPE:":
        pass
    linha = arquivo.readline().split()

# Guardando todas as linhas de dados em formato de tupla(por enquanto)
pontos = []
linha = arquivo.readline().split()
while linha[0] != "EOF":
    pontos += [tuple(linha)]
    linha = arquivo.readline().split()


def distance_2d(ponto1, ponto2):
    """Função que calcula a distância entre 2 pontos euclidianos,
    retorna qual o ponto de chegada e a distância entre eles"""
    xd = float(ponto1[1]) - float(ponto2[1])
    yd = float(ponto1[2]) - float(ponto2[2])
    dist = round((xd**2 + yd**2) ** 0.5)
    return ponto2[0], dist


def distance_3d(ponto1, ponto2):
    """Função que calcula a distância entre 3 pontos euclidianos,
    retorna qual o ponto de chegada e a distância entre eles"""
    xd = float(ponto1[1]) - float(ponto2[1])
    yd = float(ponto1[2]) - float(ponto2[2])
    zd = float(ponto1[3]) - float(ponto2[3])
    dist = round((xd**2 + yd**2 + zd**2) ** 0.5)
    return ponto2[0], dist


def converter_lat_long(ponto1):
    """Função que dado uma tupla com (chave, grau e minuto)
    retorna a latitude e longitudes que é necessário para função
    de distancia entre pontos geograficos"""
    PI = 3.141592
    grau = round(float(ponto1[1]))
    minu = float(ponto1[1]) - grau
    latitude = PI * (grau + 5.0 * minu / 3.0) / 180.0
    grau = round(float(ponto1[2]))
    minu = float(ponto1[2]) - grau
    longitude = PI * (grau + 5.0 * minu / 3.0) / 180.0
    return latitude, longitude


def distance_geo(ponto1, ponto2):
    """Função que recebe duas tuplas (chave, grau e minuto),
    chama a função de conversão com latitude e longitude e
    faz uma nova tupla substituindo grau e minuto respectivamente,
    retorna a chave correspondente ao ponto de chegada e sua distância
    """
    temp = converter_lat_long(ponto1)
    ponto1_convertido = (ponto1[0], temp[0], temp[1])
    temp = converter_lat_long(ponto2)
    ponto2_convertido = (ponto2[0], temp[0], temp[1])

    RRR = 6378.388
    q1 = cos(ponto1_convertido[2] - ponto2_convertido[2])
    q2 = cos(ponto1_convertido[1] - ponto2_convertido[1])
    q3 = cos(ponto1_convertido[1] + ponto2_convertido[1])
    dist = RRR * acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0
    return ponto2_convertido[0], int(dist)


# Definindo as funções que calcula as distâncias
def calcular_distancia(tipo, nodes):
    """Faz o cálculo da distancia referente ao tipo, recebe uma string e lista de tuplas,
    as tuplas correspondem a chave e valores,
    e retorna a soma dos caminhos"""
    visitados = [nodes[0]]  # Definindo o ponto inicial (temporário)
    nao_visitados = nodes[1:]  # Listando o restante dos pontos (temporário)
    # Lista que guarda keys e as distancias percorridas
    lista_distancias = [(nodes[0][0], 0)]

    # Loop que só para quando todos os pontos forem percorridos
    while nao_visitados != []:
        # Lista temporária das distâncias entre o ponto de partida e todos os não percorridos
        lista_pontos = {}
        for x in nao_visitados:
            # Chamando a função corresponde ao tipo com o inicial e a iteração do for
            if tipo == "EUC_2D":
                distancia = distance_2d(visitados[-1], x)
            elif tipo == "EUC_3D":
                distancia = distance_3d(visitados[-1], x)
            elif tipo == "GEO":
                distancia = distance_geo(visitados[-1], x)
            elif tipo_de_pontos in ("MAN_2D", "MAN_3"):
                pass
            elif tipo_de_pontos in ("MAX_2D", "MAX_3"):
                pass
            elif tipo_de_pontos == "ATT":
                pass
            elif tipo_de_pontos == "CEIL_2D":
                pass
            elif tipo_de_pontos in ("XRAY2", "XRAY3"):
                pass
            # Guardando tds distancias temporariamente
            lista_pontos[distancia[0]] = distancia[1]

        # Após todas as distâncias serem calculadas escolhe a menor
        menor_distancia = min(lista_pontos.values())
        # Encontrando a chave correspondente ao menor valor
        chave_da_menor = [
            x for x, valor in lista_pontos.items() if valor == menor_distancia
        ]
        # Coloca na lista de distâncias o ponto de chegada e a distância para ele
        lista_distancias += [(chave_da_menor[0], menor_distancia)]

        # Adiciona na lista de visitados o ponto que possui a chave correspondente a menor
        visitados += [x for x in nao_visitados if x[0] == chave_da_menor[0]]
        # Remove da lista de nao visitados o ponto que possui menor caminho
        nao_visitados = [x for x in nao_visitados if x[0] != chave_da_menor[0]]

    # Função de somatório para descobrir o caminho total
    soma_caminhos = 0
    for x in lista_distancias:
        soma_caminhos += x[1]

    return soma_caminhos


# Chamada que vai passar uma string com tipo de pontos e uma lista de tuplas
saida = calcular_distancia(tipo_de_pontos, pontos)


print(saida)
print(tipo_de_pontos)
