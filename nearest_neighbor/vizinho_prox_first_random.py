from random import randint
import time
tac = time.perf_counter() # recebe o tempo do inicio da execução

def calcular_distancia_euc2d(ponto1, ponto2):
    """Função que calcula a distância entre 2 pontos euclidianos fornecida pelo tslib"""
    xd = float(ponto1[0]) - float(ponto2[0])
    yd = float(ponto1[1]) - float(ponto2[1])
    dist = round((xd**2 + yd**2) ** 0.5)
    return dist

def organiza_dados(linhas_do_arquivo):
    """Recebe as linhas do arquivo, e as organiza na estrutura de dados exigida"""
    contador=0
    lista=[]
    dicio={}
    for l in linhas_do_arquivo:
        if l != "EOF": # se n tiver chegado ao final do arquivo
            # recebe a linha, splita nos espaços e a transforma em tupla. Ex.: (1, 1234.1, 5678.2)
            linha_atual = tuple(l.split())
            # guarda o indice do ponto, e as coordenadas da linha na lista
            lista += [linha_atual]
            # guarda o indice como chave e as coordenadas como valores de suas respectivas chaves
            dicio[linha_atual[0]] = float(linha_atual[1]), float(linha_atual[2]) 
            contador+=1
    return lista, dicio, contador

def gerar_caminho(dict_coordenadas, lista_pontos, qtde_pontos):
    """Calcula e retorna o menor caminho e a menor distancia"""
    # determina o ponto de saida e chegada aleatoriamente
    ponto_aleatorio = randint(1, qtde_pontos)
    # remove ele da lista de pontos para gerar uma lista de pontos ainda não visitados
    lista_pontos.pop(ponto_aleatorio-1)
    lista_n_visitados = lista_pontos[:]

    contador_pontos = 0
    menor_distancia = 0
    menor_caminho = []
    lista_coord = []

    while lista_n_visitados != []:
        if contador_pontos == 0: # se for a 1a vez

            # determina o ponto_anterior para calcular a distancia entre os pontos
            ponto_anterior = ponto_aleatorio
            menor_caminho += [str(ponto_aleatorio)] # add o ponto aleatorio no início
            # adiciona na lista de coordenadas o indice, e as coordenadas. Ex.: ('1', 123.1, 456.2)
            lista_coord += [tuple([str(ponto_aleatorio), dict_coordenadas[str(ponto_aleatorio)][0], dict_coordenadas[str(ponto_aleatorio)][1]])]
            contador_pontos+=1

        elif contador_pontos == qtde_pontos: # se for a última vez
            lista_n_visitados = []
            dist_atual = calcular_distancia_euc2d(dict_coordenadas[str(ponto_anterior)], dict_coordenadas[str(ponto_aleatorio)])
            menor_caminho += [str(ponto_aleatorio)] # add o ponto aleatorio no final do caminho

            # adiciona na lista de coordenadas o indice, e as coordenadas. Ex.: ('1', 123.1, 456.2)
            lista_coord += [tuple([str(ponto_aleatorio), dict_coordenadas[str(ponto_aleatorio)][0], dict_coordenadas[str(ponto_aleatorio)][1]])]

            # soma a distancia atual calculada na var da menor_distancia do menor caminho
            menor_distancia += dist_atual

            return lista_coord, menor_caminho, menor_distancia

        else: # vezes comuns
            lista_n_visitados.remove(melhor_ponto) # remove o ponto calculado da ultima vez da list

        menor_dist_temp = float('inf') # inicia a var em infinito
        for p in lista_n_visitados: # testa para todos que ainda não foram visitados
            dist_atual = calcular_distancia_euc2d(dict_coordenadas[str(ponto_anterior)], dict_coordenadas[str(p[0])])

            if dist_atual < menor_dist_temp: # se a atual for menor do que a guardada
                menor_dist_temp = dist_atual # guarda a atual distancia como a melhor da vez
                melhor_ponto = p # guarda o atual ponto da interação como o melhor da vez

        # determina o ponto_anterior para calcular a distancia entre os pontos
        ponto_anterior = melhor_ponto[0]
        menor_caminho += [melhor_ponto[0]] # guarda o indice do ponto na lista do menor_caminho

        lista_coord += [tuple([str(melhor_ponto[0]), float(melhor_ponto[1]), float(melhor_ponto[2])])]

        # soma a distancia atual calculada na var da menor distancia do melhor caminho
        menor_distancia += menor_dist_temp
        contador_pontos+=1

def run():
    """Função principal que executa o código"""
    with open("nearest_neighbor/mapa.txt", 'r', encoding="utf-8") as arquivo:
        linhas_temp = arquivo.read().splitlines() # lê todas as linhas e as separa em uma lista

        # armazena todas as linhas do problema euclidiano_2d
        # com exceção das do cabeçalho e da final
        linhas_temp = linhas_temp[6:-1:]

    # retorna uma lista com tuplas dos pontos, um dict com as coordenadas, e a qtde de pontos
    lista_pontos, dict_coordenadas, qtde_pontos = organiza_dados(linhas_temp)

    # com os dados acima, calcula o menor caminho, e retorna ele mais a sua distancia
    lista_coord, caminho_final, distancia_final = gerar_caminho(dict_coordenadas, lista_pontos, qtde_pontos)

    print(caminho_final)
    print(distancia_final)

    tic = time.perf_counter() # recebe o tempo atual
    print(f'Tempo de execução: {tic-tac}') # subtrai os tempos e printa o tempo de execução

    return lista_coord # retorna para poder utilizar na plot_map

if __name__ == "__main__":
    run()
