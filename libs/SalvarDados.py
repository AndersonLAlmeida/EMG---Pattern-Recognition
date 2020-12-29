# -*- coding: utf-8 -*-

def save_data(data_full, filename_data, filename_movimento, tipo_de_movimento):
    write_data = ""
    for sample in range(0, (len(data_full)-1)):
        write_data += str(data_full[sample]) + ";"
    
    write_data += (str(data_full[-1]) + "\n")
    
    # Salvar os dados
    with open(filename_data, 'a+') as f:
        f.write(write_data)
    
    # SAlvar o tipo de movimento
    with open(filename_movimento, 'a+') as f:
        write_data = str(tipo_de_movimento) + '\n'
        f.write(write_data)

def save_repouso(data_full, filename, tipo_de_movimento):
    write_data = ""
    for sample in range(0, (len(data_full)-1)):
        write_data += str(data_full[sample]) + ";"
    
    write_data += str(data_full[-1]) + "\n"
    
    with open(filename, 'a+') as f:
        f.write(write_data)

def save_data_and_time(time, data, filename):        
    write_data = ""
    for i in range(0, len(data)):  
        aux = (str(data[i])) + ";" + (str(time[i])) + "\n"
        write_data = write_data + aux
    
    with open(filename, 'w+') as f:
        f.write(write_data)