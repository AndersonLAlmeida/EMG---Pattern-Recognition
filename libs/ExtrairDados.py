# -*- coding: utf-8 -*-
import numpy as np

from math import sqrt
from scipy.fft import fft
import matplotlib.pyplot as plt

# Obtém o RMS de um conjunto de pontos
def f_rms(data, size):    
    soma = 0

    for i in data:
        soma = soma + (i ** 2) 

    Vrms = sqrt(soma/size)

    return Vrms

# Detecta o impulso baseado no ruído em repouso do músculo
def delta_dirac(data_full, filename_limiar, N, janela):
    # Valor obtido empiricamente utilizando o repouso
    with open(filename_limiar, 'r') as l:
        limiar = l.read()
    
    limiar = float(limiar)
    
    # Compara se algum dos valores é maior que o limiar, caso sim efetua o RMS
    # dos próximos 40 pontos (baseado em Rodrigo Ortolan)
    # Se o RMS desses 40 pontos for maior que o limiar considera este o inicio da contração 
    # E retorna 400 pontos referentes aos 200ms do começo do sinal
    for row in range(0, len(data_full)):
        if data_full[row] > limiar:
            rms = f_rms(data_full[row:(row + janela)], janela)
            if rms > limiar:
                data_part = data_full[row:(row + N)]
                
                return data_part

def RMS(data_part, N, janela):
    # Calcula tensão RMS móvel de acordo com a janela definida anteriormente
    aux = []
    Vrms = []

    for i in range(0, N):
        aux.append(data_part[i])
        if (len(aux) % janela == 0):
            Vrms.append(f_rms(aux, janela))
            aux = []
        
    return Vrms

def FFT(data_part, N):
    # Numero de pontos
    #N = 400 # 200ms
    # Espaçamento da amostra
    T = 1.0 / 800.0

    # FFT
    yf = fft(data_part)
    #print(f"FFT: {yf}")
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
    plt.axis([0, 150, 0, 0.025])
    plt.title("FFT")

    plt.grid(True)
    plt.xlabel("Freq")
    plt.ylabel("Amplitude")
    plt.show()

    return xf, yf