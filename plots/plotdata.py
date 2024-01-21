import csv
import numpy as np
import matplotlib.pyplot as plt

def pathtoFilename(path):
    lastslash = path.rfind('\\') + 1
    scvindex = path.find('.csv')
    return path[lastslash:scvindex]

def FMconv(V): 
    return (V/430 - (4/1000))/(16/1000) * 29
 
def LD1conv(V): #2k
    return 1000 * ((60.25906654 * float(V)) - 0.2654580671)

def LD2conv(V): #1k
    return 1000 * ((31.27993035*float(V)) - 0.2654580671)

def PT2kConv(V):
    return ((float(V)) * (2000)) / (12)

def PT3kConv(V):
    return ((float(V)) * (3000)) / (12)

def PT15kconv(V):
    return ((float(V)) * (1500)) / (12)

def TCConv(V):
    if V == 0:
        return 0
    r_ref = 15000
    v_c = 5 #TODO implement this
    alpha = 0.00392 # Ohms/Ohms/ºC
    r_nom = 100

    r_rtd = (r_ref * (v_c - V))/(V)
    delta_temp = (1/alpha) * ((r_rtd/r_nom) - 1)
    return (9/5) * delta_temp + 32 #return in *F



sense_names = ["PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PT7", "PT8", "TC1", "TC2", "TC3", "FM1", "LD1", "LD2"]

path1 = "/Users/nissiragland/Documents/CRT/Hybrid Control/Hybrid-Control/labjackcoldflow_data.csv"
path1offset = 10000
path2 = "/Users/nissiragland/Documents/CRT/Hybrid Control/Hybrid-Control/plots/hotfire_data_1-15-2024.csv"
path2offset = 10

PATHS = [[path2offset, path2]]#[[path1offset, path1], [path2offset, path2]]

#Plot individually
for offset, path in PATHS:
    sensors = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) < 14:
                break #Cut off incomplete data from crashing etc
            else:
                numpoints = len(sensors[0])
            sensors[0].append(PT2kConv(float(row[0])))
            sensors[1].append(PT2kConv(float(row[1])))
            sensors[2].append(PT3kConv(float(row[2])))
            sensors[3].append(PT3kConv(float(row[3])))
            sensors[4].append(PT15kconv(float(row[4])))
            sensors[5].append(PT2kConv(float(row[5])))
            sensors[6].append(PT3kConv(float(row[6])))
            sensors[7].append(PT2kConv(float(row[7])))
            sensors[8].append(TCConv(float(row[8])))
            sensors[9].append(TCConv(float(row[9])))
            sensors[10].append(TCConv(float(row[10])))
            sensors[11].append(FMconv(float(row[11])))
            sensors[12].append(LD1conv(float(row[12])))
            sensors[13].append(LD2conv(float(row[13])))
    file.close()

    numPoints = np.linspace(0,numpoints * 1/100, numpoints + 1)
    
    fig, axs = plt.subplots(4, 4)
    for row, col in np.ndindex((4, 4)):
        if (row*4 + col) < 14:
            axs[row][col].plot(numPoints[:-offset], sensors[row*4+col][:-offset])
            axs[row][col].title.set_text(sense_names[row*4+col])
        else:
            axs[row][col].set_visible(False)
    fig.suptitle(pathtoFilename(path2))
    plt.show()

