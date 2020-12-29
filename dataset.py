# -*- coding: utf-8 -*-
import numpy as np
from timeit import default_timer as timer
import random
import serial
import serial.tools.list_ports
import os
from math import sqrt
import argparse
import matplotlib.pyplot as plt

from datetime import datetime
from scipy.fft import fft
from libs.DadosBrutos import Serial_connection, Coleta
from libs.SalvarDados import save_data, save_repouso
from libs.ExtrairDados import delta_dirac, RMS, FFT


### Implementação do argparse ###

# Criando o parser
parser = argparse.ArgumentParser(description="Parâmetros para coleta de dados")

# Adicionar argumentos
parser.add_argument("-n", "--nome", type=str, required=True, help="Nome do paciente")
parser.add_argument("-m", "--movimento", type=str, required=True, help="Movimento realizado, opções: repouso, flexao_total ou extensao_total")
parser.add_argument("-a", "--amostras", type=int, default=10, help="Quantidade de amostras coletadas, por padrão são 10")
parser.add_argument("-p", "--porta", type=str, default="COM5", help="Porta a qual está conectada o conversor ADC")

### Fim da implementação do argparse ###

### Implementar estrutura do DATASET ###
def criando_paciente(nome):
    paciente = f"Dataset\\{nome}\\"
    if not os.path.isdir(paciente): # vemos de este diretorio já existe
        os.makedirs(paciente)


if __name__ == '__main__':
    # Instância o argparse
    args = parser.parse_args()

    criando_paciente(args.nome)

    # Declarando quais movimentos foram realizados
    relacao_de_movimentos = {
    'repouso':'repouso',
    'flexao_total':'0;1',
    'extensao_total':'1;0',
    'flexao_polegar':'0;0;1;0;0',
    'flexao_indicador':'0;0;0;1;0',
    'flexao_medio':'0;0;0;0;1',
}

    N = 400
    janela = 40

    filename_limiar = f"Dataset\\{args.nome}\\limiar.txt"
    filename_data = f"Dataset\\{args.nome}\\dados_classificacao.csv"
    filename_movimento = f"Dataset\\{args.nome}\\movimentos_classificacao.csv"
    filename_auxiliares = f"Dataset\\{args.nome}\\dados_auxiliares.csv"
    filename_movimento_aux = f"Dataset\\{args.nome}\\movimentos_auxiliares.csv"

    for amostra in range(0, args.amostras):
        # Coletar e salvar o sinal Bruto
        data_full = Coleta(args.porta)

        if args.movimento.lower() == "repouso":
            limiar = sum(data_full)/len(data_full)

            limiar = str(limiar)
            with open(filename_limiar, 'w+') as f:
                f.write(limiar)
        if args.movimento.lower() == "flexao_polegar" or args.movimento.lower() == "flexao_indicador" or args.movimento.lower() == "flexao_medio" or args.movimento.lower() == "repouso":
            save_data(data_full, filename_auxiliares, filename_movimento_aux, relacao_de_movimentos[f'{args.movimento}'])
        if args.movimento.lower() == "flexao_total" or args.movimento.lower() == "extensao_total":
            save_data(data_full, filename_data, filename_movimento, relacao_de_movimentos[f'{args.movimento}'])
        print(f"Amostra {amostra + 1} coletada")

        x = np.array(range(len(data_full)))

        plt.plot( x, data_full, 'k:', color='orange') # linha pontilha orange

        #plt.axis([0, 6000, 0, 2])
        plt.title("EMG")

        plt.grid(True)
        plt.xlabel("Pontos")
        plt.ylabel("Amplitude")
        plt.show()
        

