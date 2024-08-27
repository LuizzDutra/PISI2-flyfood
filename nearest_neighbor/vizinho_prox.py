arquivo = open("PISI2-flyfood/nearest_neighbor/mapa.txt", encoding="utf-8")
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


# Definindo as funções que calcula as distâncias
def euclidean_distance(tipo, nodes):
    """Faz o cálculo da distancia euclidiana, seja 2D ou 3D,
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
            # INCOMPLETO - Falta adicionar a condição da chamada da função com base no tipo
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


# Verificar e chamar a função de calculo da distância correspondente ao tipo
if tipo_de_pontos in ("EUC_2D", "EUC_3"):
    saida = euclidean_distance(tipo_de_pontos, pontos)
elif tipo_de_pontos in ("MAN_2D", "MAN_3"):
    pass
elif tipo_de_pontos in ("MAX_2D", "MAX_3"):
    pass
elif tipo_de_pontos == "GEO":
    pass
elif tipo_de_pontos == "ATT":
    pass
elif tipo_de_pontos == "CEIL_2D":
    pass
elif tipo_de_pontos in ("XRAY2", "XRAY3"):
    pass

print(saida)
print(tipo_de_pontos)
