arquivo = open("mapa.txt", encoding="utf-8")
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
        tipo_de_pontos = linha[1]
    elif linha[0] == "EDGE_DATA_FORMAT":
        tipo_de_pontos = linha[1]
    elif linha[0] == "NODE_COORD_TYPE:":
        tipo_de_pontos = linha[1]
    elif linha[0] == "DISPLAY_DATA_TYPE:":
        tipo_de_pontos = linha[1]
    linha = arquivo.readline().split()

pontos = []
linha = arquivo.readline().split()
while linha[0] != "EOF":
    pontos += [tuple(linha)]
    linha = arquivo.readline().split()


print(tipo_de_pontos)
print(pontos[0][1])
