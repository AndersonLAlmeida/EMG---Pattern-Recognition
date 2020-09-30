# -*- coding: utf-8 -*-
import numpy as np
import serial

# Estabelecer Conexão Serial
def Serial_connection(porta, baudrate = 115200):
    while True:
        try:
            arduinoData = serial.Serial(porta, baudrate)
            print("Sucesso na conexão!")
            break
        except:
            print("Erro ao conectar com o Arduíno!")
    
    return arduinoData


def Coleta(porta):
    time_full = []
    data_full = []
    diff_time = 0
    pontos_totais = 4000

    serial_connection = Serial_connection(porta)

    # Envia a informação via serial para iniciar a coleta dos dados
    serial_connection.write(str.encode(input("Deseja iniciar? ")))

    # Fica no looping senão receber os dados
    while serial_connection.inWaiting() == 0:
        pass

    # Varia de 0.0005 segundos em 0.0005 segundos até 2 segundos
    # Mais propriamente dito, varia de 500us em 500us
    # Cada conversão leva em média 500us
    #4000 pontos e 400 pontos realmente representam o total de 2 segundso de coleta?
    while (diff_time < pontos_totais):
        time_full.append(diff_time)
        data_full.append(float(serial_connection.readline().decode("ascii")))  
        diff_time = diff_time + 0.5
    
    return time_full, data_full

