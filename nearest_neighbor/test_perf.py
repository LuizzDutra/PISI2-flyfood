"""Utilitário que será utilizado para medição do tempo de execução dos algoritmos"""
import sys
import importlib
from time import perf_counter_ns

#Para a utilização desse script
#Coloque o arquivo do seu algoritmo que será testado
#no mesmo diretório

#O algoritmo deverá conter uma função chamada "run"
#que irá executá-lo

#Utilize o terminal e execute o script com os
#seguintes argumentos
#>python ./test_perf.py "nome do algoritmo sem extensão" número de testes


def main():
    "Função principal que retorna a média dos tempos de execução em ns"
    algo_name = sys.argv[1]

    it = int(sys.argv[2])
    algo = importlib.import_module(algo_name)

    total_time = 0
    for _ in range(it):
        start = perf_counter_ns()
        algo.run()
        end = perf_counter_ns()
        total_time += end - start

    print(total_time/it)


if __name__ == "__main__":
    main()
