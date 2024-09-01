from random import randint
import time
tic = time.perf_counter()
def main():
    """Função principal que executa o código"""
    arquivo = open("mapa.txt", 'r', encoding="utf-8")
    linhas_temp = arquivo.read().splitlines() # lê todas as linhas e as separa em uma lista
    linhas_temp = linhas_temp[6:-1:] # armazena todas as linhas do problema euclidiano_2d com exceção do cabeçalho e da linha final
    arquivo.close()
    
    lista_pontos, dict_coordenadas, qtde_pontos = organiza_dados(linhas_temp)
    
    caminho_final, distancia_final = gerar_caminho(dict_coordenadas, lista_pontos, qtde_pontos)
    print(caminho_final)
    print(distancia_final)
    toc = time.perf_counter()
    print(f'Tempo de execução: {toc-tic}')       
def calcular_distancia_euc2d(ponto1, ponto2):
    """Função que calcula a distância entre 2 pontos euclidianos fornecida pelo tslib"""
    xd = float(ponto1[0]) - float(ponto2[0])
    yd = float(ponto1[1]) - float(ponto2[1])
    dist = round((xd**2 + yd**2) ** 0.5)
    return dist
def organiza_dados(temp):
    contador=0
    lista=[]
    dict={}
    for l in temp:
        if l != "EOF": # se n tiver chegado ao final do arquivo
            linha_atual = tuple(l.split())
            lista += [linha_atual] # guarda o indice do ponto, e as coordenadas da linha
            dict[linha_atual[0]] = float(linha_atual[1]), float(linha_atual[2])
            contador+=1
    return lista, dict, contador
def gerar_caminho(dict_coordenadas, lista_pontos, qtde_pontos):
    """Calcula e retorna o menor caminho"""
    ponto_aleatorio = randint(1, qtde_pontos)
    lista_pontos.pop(ponto_aleatorio-1)
    lista_n_visitados = lista_pontos[:]

    contador_pontos = 0
    menor_distancia = 0
    menor_caminho = []
    
    while lista_n_visitados != []:
        if (len(lista_n_visitados) - (qtde_pontos-1)) == contador_pontos: # se for a 1a vez
            ponto_anterior = ponto_aleatorio
            menor_caminho += [str(ponto_aleatorio)] # add o ponto aleatorio no início
            contador_pontos+=1
            
        elif contador_pontos == qtde_pontos: # se for a última vez
            lista_n_visitados = []
            dist_atual = calcular_distancia_euc2d(dict_coordenadas[str(ponto_anterior)], dict_coordenadas[str(ponto_aleatorio)])
            menor_caminho += [ponto_aleatorio] # add o ponto aleatorio no final
            menor_distancia += dist_atual
            return menor_caminho, menor_distancia
            
        else: # vezes comuns
            lista_n_visitados.remove(melhor_ponto)
        
        menor_dist_temp = 1000000.0
        for p in lista_n_visitados:
            dist_atual = calcular_distancia_euc2d(dict_coordenadas[str(ponto_anterior)], dict_coordenadas[str(p[0])])
            if dist_atual < menor_dist_temp:
                menor_dist_temp = dist_atual
                melhor_ponto = p
        ponto_anterior = melhor_ponto[0]
        menor_caminho += [melhor_ponto[0]]
        menor_distancia += menor_dist_temp
        
        contador_pontos+=1
if __name__ == "__main__":
    main()

