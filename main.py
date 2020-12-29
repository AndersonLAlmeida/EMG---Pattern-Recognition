# -*- coding: utf-8 -*-
from timeit import default_timer as timer
import random
import serial
import serial.tools.list_ports
import os
from math import sqrt
import argparse
import numpy as np
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

    for amostra in range(0, args.amostras):
        
        
        # Coletar e salvar o sinal Bruto
        data_full = Coleta(args.porta)

        x = np.array(range(len(data_full)))

        plt.plot( x, data_full, 'k:', color='orange') # linha pontilha orange

        plt.axis([0, 6000, 1.3, 2])
        plt.title("EMG")

        plt.grid(True)
        plt.xlabel("Pontos")
        plt.ylabel("Amplitude")
        plt.show()

        xf, yf = FFT(data_full, 6000)

        print(f"Amostra {amostra + 1} coletada")
        




