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
from libs.SalvarDados import save_data
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
    paciente = f".\\{nome}\\"
    if not os.path.isdir(paciente): # vemos de este diretorio já existe
        diretorios = ["repouso", "flexao_polegar", "flexao_indicador", "flexao_total", "extensao_total"]
        for dir in diretorios:
            dir_movimento = paciente + dir
            os.makedirs(dir_movimento)
            with open((dir_movimento + "\\amostra.txt"), "w+") as f:
                f.write("0")


if __name__ == '__main__':
    # Instância o argparse
    args = parser.parse_args()

    N = 400
    janela = 40
    media_limiar = []
    
    dir_amostra = f".\\{args.nome}\\{args.movimento}\\amostra.txt"
    with open(dir_amostra, "r") as f:
        numero_amostra = f.read()

    for amostra in range(0, args.amostras):
        # Coletar e salvar o sinal Bruto
        time_full, data_full = Coleta(args.porta)
        filename_full = f".\\{args.nome}\\{args.movimento}\\amostra_{numero_amostra}_BRUTO.csv"
        save_data(time_full, data_full, filename_full)

        if args.movimento.lower() == "repouso":
            media_limiar.append(max(data_full))

            if len(media_limiar) == args.amostras:
                limiar = sum(media_limiar)/args.amostras
                limiar = str(limiar)
                filename_limiar = f".\\{args.nome}\\repouso\\limiar.txt"
                with open(filename_limiar, 'w+') as f:
                    f.write(limiar)
        else:
            time_part, data_part = delta_dirac(time_full, data_full, filename_limiar, N, janela)
            try:
                rms_time, Vrms = RMS(time_part, data_part, N, janela)
                x_FFT, y_FFT = FFT(data_part, N)
                filename_part = f".\\{args.nome}\\{args.movimento}\\amostra_{numero_amostra}_part.csv"
                filename_RMS = f".\\{args.nome}\\{args.movimento}\\amostra_{numero_amostra}_RMS.csv"
                filename_FFT = f".\\{args.nome}\\{args.movimento}\\amostra_{numero_amostra}_FFT.csv"
                save_data(time_part, data_part, filename_part)
                save_data(rms_time, Vrms, filename_RMS)
                save_data(x_FFT, y_FFT, filename_FFT)
            except:
                print("Não houve movimento ou não foi forte o suficiente, por gentileza realize novamente")
        
        numero_amostra = int(numero_amostra) + 1

    with open(dir_amostra, "w") as f:
        numero_amostra = str(numero_amostra)
        f.write(numero_amostra)




