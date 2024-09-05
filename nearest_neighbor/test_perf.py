"""Utilitário que será utilizado para medição do tempo de execução dos algoritmos"""

import sys
import importlib
from time import perf_counter_ns

# Para a utilização desse script
# Coloque o arquivo do seu algoritmo que será testado
# no mesmo diretório

# O algoritmo deverá conter uma função chamada "run"
# que irá executá-lo

# Utilize o terminal e execute o script com os
# seguintes argumentos
# >python ./test_perf.py "nome do algoritmo sem extensão" número de testes


def main():
    "Função principal que retorna a média dos tempos de execução em ns"
    # Guarda a string do nome do código que será rodado (vizinho_prox)
    algo_name = sys.argv[1]

    # Guarda a quantidade de vezes que será rodado
    it = int(sys.argv[2])

    # Chama o modulo com a string dada
    algo = importlib.import_module(algo_name)

    total_time = 0
    media = 0
    for _ in range(it):

        # Guarda o instante de início
        start = perf_counter_ns()

        # Chama a função main do código que será testado
        distancia = algo.run()

        # Guarda o instante final
        end = perf_counter_ns()

        # Soma o tempo de cada execução iterada no for
        total_time += end - start

        # Guarda o somatório para a média das distâncias
        media += distancia[1]

    # Calcula a média geral de todas as distâncias
    print(f"A média geral das distâncias : {media/it:.2f}")
    print(f"O tempo em ns : {total_time / it}")


if __name__ == "__main__":
    main()
