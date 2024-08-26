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


# Definindo as funções que calcula as distâncias
def euclidean_distance(tipo, nodes):
    """Faz o cálculo da distancia euclidiana, seja 2D ou 3D"""
    visitados = [nodes[0]]
    nao_visitados = [nodes[1:]]
    return visitados, nao_visitados
    # if tipo == "EUC_2":
    #     pass
    # else:
    #     pass


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
print(pontos[0][1])
