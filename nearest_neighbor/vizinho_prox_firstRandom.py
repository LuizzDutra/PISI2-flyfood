from random import randint
import time
tac = time.perf_counter()
 
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
    dict={}
    for l in linhas_do_arquivo:
        if l != "EOF": # se n tiver chegado ao final do arquivo
            linha_atual = tuple(l.split()) # recebe a linha, splita nos espaços e a transforma em tupla. Ex.: (1, 1234.1, 5678.2)
            lista += [linha_atual] # guarda o indice do ponto, e as coordenadas da linha na lista
            dict[linha_atual[0]] = float(linha_atual[1]), float(linha_atual[2]) # guarda o indice como chave e as coordenadas como valores de suas respectivas chaves
            contador+=1
    return lista, dict, contador

def gerar_caminho(dict_coordenadas, lista_pontos, qtde_pontos):
    """Calcula e retorna o menor caminho e a menor distancia"""
    ponto_aleatorio = randint(1, qtde_pontos)
    lista_pontos.pop(ponto_aleatorio-1)
    lista_n_visitados = lista_pontos[:]

    contador_pontos = 0
    menor_distancia = 0
    menor_caminho = []

    while lista_n_visitados != []:
        if contador_pontos == 0: # se for a 1a vez
            ponto_anterior = ponto_aleatorio # determina o ponto_anterior para calcular a distancia entre os pontos
            menor_caminho += [str(ponto_aleatorio)] # add o ponto aleatorio no início
            contador_pontos+=1

        elif contador_pontos == qtde_pontos: # se for a última vez
            lista_n_visitados = []
            dist_atual = calcular_distancia_euc2d(dict_coordenadas[str(ponto_anterior)], dict_coordenadas[str(ponto_aleatorio)])
            menor_caminho += [ponto_aleatorio] # add o ponto aleatorio no final
            menor_distancia += dist_atual # soma a distancia atual desses pontos calculada à var da menor_distancia do caminho
            return menor_caminho, menor_distancia

        else: # vezes comuns
            lista_n_visitados.remove(melhor_ponto) # remove o ponto calculado da ultima vez da lista

        menor_dist_temp = 1000000.0
        for p in lista_n_visitados: # testa para todos que ainda não foram visitados
            dist_atual = calcular_distancia_euc2d(dict_coordenadas[str(ponto_anterior)], dict_coordenadas[str(p[0])])
            if dist_atual < menor_dist_temp:
                menor_dist_temp = dist_atual # guarda a atual distancia dos pontos como a melhor da vez
                melhor_ponto = p # guarda o atual ponto do for como o melhor da vez
        ponto_anterior = melhor_ponto[0] # determina o ponto_anterior para calcular a distancia entre os pontos
        menor_caminho += [melhor_ponto[0]] # guarda o indice do ponto na lista do menor_caminho
        menor_distancia += menor_dist_temp # soma a distancia atual desses pontos calculada à var da menor_distancia do caminho

        contador_pontos+=1
        
def main():
    """Função principal que executa o código"""
    arquivo = open("mapa.txt", 'r', encoding="utf-8")
    linhas_temp = arquivo.read().splitlines() # lê todas as linhas e as separa em uma lista
    linhas_temp = linhas_temp[6:-1:] # armazena todas as linhas do problema euclidiano_2d com exceção do cabeçalho e da linha final
    arquivo.close()
    
    lista_pontos, dict_coordenadas, qtde_pontos = organiza_dados(linhas_temp) # retorna uma lista com tuplas dos pontos, um dict com as coordenadas, e a qtde de pontos
    
    caminho_final, distancia_final = gerar_caminho(dict_coordenadas, lista_pontos, qtde_pontos) # com os dados acima, calcula o menor caminho, e retorna ele mais a sua distancia
    print(caminho_final)
    print(distancia_final)
    tic = time.perf_counter()
    print(f'Tempo de execução: {tic-tac}')      

if __name__ == "__main__":
    main()

