# -*- coding: utf-8 -*-

def save_data(data_full, data_part, data_RMS, data_FFT, freq_FFT, filename):
    write_data = str(data_full) + ';' + str(data_part) + ';' + str(data_RMS) + ";" + str(data_FFT) + ";" + str(freq_FFT) + '\n'
    
    with open(filename, 'a+') as f: 
        f.write(write_data)

def save_repouso(data_full, filename):
    write_data = str(data_full) + '\n'
    
    with open(filename, 'a+') as f:
        f.write(write_data)

def save_data_and_time(time, data, filename):        
    write_data = ""
    for i in range(0, len(data)):  
        aux = (str(data[i])) + ";" + (str(time[i])) + "\n"
        write_data = write_data + aux
    
    with open(filename, 'w+') as f:
        f.write(write_data)