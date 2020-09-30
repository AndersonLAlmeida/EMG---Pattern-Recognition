# -*- coding: utf-8 -*-

def save_data(time, data, filename):        
    write_data = ""
    for i in range(0, len(data)):  
        aux = (str(data[i]).replace(".", ",")) + ";" + (str(time[i]).replace(".", ",")) + "\n"
        write_data = write_data + aux
    
    with open(filename, 'w+') as f:
        f.write(write_data)