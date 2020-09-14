# -*- coding: utf-8 -*-
import numpy as np
from timeit import default_timer as timer
import random
import serial
import serial.tools.list_ports
import os
from math import sqrt
import argparse

from scipy.fft import fft
import matplotlib.pyplot as plt


### Implementação do argparse ###

parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")



### Fim da implementação do argparse ###


# Estabelecer Conexão Serial
def Serial_connection():
    # Lista as portas possiveis
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(port)

    # Estabelece comunicação serial
    while True:
        port = input("Entre com a porta a ser conectada \n>>")
        baudrate = 115200
        try:
            arduinoData = serial.Serial(port, baudrate)
            print("Sucesso na conexão!")
            break
        except:
            print("Erro ao conectar com o Arduíno!")
            pass
    return arduinoData

# Receber e salvar os pontos em formato csv
def save_data( time, data, nome, movimento, amostra, points):

    filename = nome + "_" + movimento + "_" + amostra + ".csv"

    i = 0
    write_data = ""
    while (i < points):
        aux = str(data[i]) + ";" + str(time[i]) + "\n"
        write_data = write_data + aux
        i = i + 1
    
    with open(filename, 'w+') as f:
        f.write(write_data)
        if points == 4000:
            print("Onda completa")
        if points == 400:
            print("200ms")
        else:
            print("RMS")


# Receber os pontos
def get_data(arduinoData):
    y = []
    x = []
    time = 0.5

    # Envia a informação via serial para iniciar a coleta dos dados
    inicio = input("Deseja iniciar? ")
    arduinoData.write(str.encode(inicio))

    # Fica no looping senão receber os dados
    while arduinoData.inWaiting() == 0:
        pass
    
    # Varia de 0.0005 segundos em 0.0005 segundos até 2 segundos
    # Mais propriamente dito, varia de 500us em 500us
    # Cada conversão leva em média 500us
    while (time <= 2000):
        y.append(float(arduinoData.readline().decode("ascii")))
        x.append(time)
        time = time + 0.5
    
    # Retorna os valores, respectivamente de tempo e tensão
    return x, y

# Após a coleta das 25 repetições fazer uma média com os maiores valores de cada repouso
def repouso():
    pass
    
# Obtém o RMS de um conjunto de pontos
def f_rms(x, size):    
    soma = 0

    for i in x:
        soma = soma + (i ** 2) 
    
    Vrms = sqrt(soma/size)

    return Vrms

# Detecta o impulso baseado no ruído em repouso do músculo
def delta_dirac(x, y):
    limiar = 2.20 # Valor obtido empiricamente, acredito que seja o ruido em repouso
    maximum_points = 4000 # quantidade de pontos equivalentes a 2 segundos

    # Compara se algum dos valores é maior que o limiar, caso sim efetua o RMS
    # dos próximos 40 pontos (baseado em Rodrigo Ortolan)
    # Se o RMS desses 40 pontos for maior que o limiar considera este o inicio da contração 
    # E retorna 400 pontos referentes aos 200ms do começo do sinal
    for row in range(0, maximum_points):
        if y[row] > limiar:
            print (y[row])
            rms = f_rms(y[row:(row+40)], 40)
            if rms > limiar:
                return x[row:(row+400)], y[row:(row+400)]

def FFT(x, y):
    # Number of sample points
    N = 400 # Two hundred ms
    # sample spacing
    T = 1.0 / 800.0

    # FFT
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
    plt.grid()
    plt.show()




if __name__ == '__main__':
    # Comunicação Serial
    arduinoData = Serial_connection()

    # Recebe as informações do arduino; x -> TEMPO (ms); y -> TENSÃO (V)
    x, y = get_data(arduinoData)

    # Coleta os dados do paciente
    nome = input("Digite o nome do pasciente: ")
    movimento = input("Qual movimento será realizado? ")
    amostra = input("Numero da amostra: ")

    # Salva a onda completa
    save_data(x, y, "ANDERSON", "FLEXOR", "0", points=4000)

    try:
        # Extrai os pontos correspondentes aos 200ms e salva
        time, data = delta_dirac(x, y)
        save_data(time, data, "ANDERSON", "FLEXOR", "1", points=400)
    except:
        print("O musculo esta em repouso")

    # Calcula tensão RMS móvel de 40 em 40 pontos
    Vrms = []
    aux = []
    rms_time = []
    for i in range(0,400):
        aux.append(data[i])
        if (len(aux) % 40 == 0):
            Vrms.append(f_rms(aux, 40))
            rms_time.append(time[i])
            aux = []
    
    save_data(rms_time, Vrms, "ANDERSON", "FLEXOR", "RMS", points=len(Vrms))

    print (Vrms, rms_time)

    FFT(time, data)

    ### Implementar estrutura do DATASET
    