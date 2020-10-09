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
parser.add_argument("-m", "--movimento", type=str, required=True, help="Movimento realizado")
parser.add_argument("-a", "--amostras", type=int, default=10, help="Quantidade de amostras coletadas, por padrão são 10")
parser.add_argument("-p", "--porta", type=str, default="COM5", help="Porta a qual está conectada o conversor ADC")

### Fim da implementação do argparse ###

### Implementar estrutura do DATASET ###
def criando_paciente(nome):
    paciente = f"Dataset\\{nome}\\"
    if not os.path.isdir(paciente): # vemos de este diretorio já existe
        diretorios = ["repouso", "flexao_polegar", "flexao_indicador", "flexao_total", "extensao_total"]
        for dir in diretorios:
            dir_movimento = paciente + dir
            os.makedirs(dir_movimento)


if __name__ == '__main__':
    # Instância o argparse
    args = parser.parse_args()

    criando_paciente(args.nome)

    N = 400
    janela = 40
    media_limiar = []

    filename_limiar = f"Dataset\\{args.nome}\\repouso\\limiar.txt"
    filename_data = f"Dataset\\{args.nome}\\{args.movimento}\\dados_{args.movimento}.csv"

    for amostra in range(0, args.amostras):
        # Coletar e salvar o sinal Bruto
        data_full = Coleta(args.porta)

        if args.movimento.lower() == "repouso":
            media_limiar.append(max(data_full))

            if len(media_limiar) == args.amostras:
                limiar = sum(media_limiar)/args.amostras
                limiar = str(limiar)
                with open(filename_limiar, 'w+') as f:
                    f.write(limiar)
            save_repouso(data_full, filename_data)
        else:
            data_part = delta_dirac(data_full, filename_limiar, N, janela)

            try:
                data_RMS = RMS(data_part, N, janela)
                freq_FFT, data_FFT = FFT(data_part, N)
                save_data(data_full, data_part, data_RMS, list(data_FFT), list(freq_FFT), filename_data)
            except:
                print("Não houve movimento ou não foi forte o suficiente, por gentileza realize novamente")

        print(f"Amostra {amostra + 1} coletada")




