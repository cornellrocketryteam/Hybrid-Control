import csv
import numpy as np
import matplotlib.pyplot as plt

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
    return 0

#{0: pt2000, 1: pt2000, 2: pt3000, 3: pt3000, 4: pt1500, 5: pt2000, 6: pt3000, 7: pt2000,
 ##               8: tc, 9: tc, 10: tc,
   #             11: fm,
    #            12: lc1000, 13: lc2000}


sense_names = ["PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PT7", "PT8", "TC1", "TC2", "TC3", "FM1", "LD1", "LD2"]
sensors = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
path = "labjackcoldflow_data.csv"
with open(path, 'r') as file:
    csv_reader = csv.reader(file)
    accum = 0
    for row in csv_reader:
        accum += 1
        if len(row) < 14:
            break
        else:
            numpoints = len(sensors[0])
        sensors[0].append(PT2kConv(row[0]))
        sensors[1].append(PT2kConv(row[1]))
        sensors[2].append(PT3kConv(row[2]))
        sensors[3].append(PT3kConv(row[3]))
        sensors[4].append(PT15kconv(row[4]))
        sensors[5].append(PT2kConv(row[5]))
        sensors[6].append(PT3kConv(row[6]))
        sensors[7].append(PT2kConv(row[7]))
        sensors[8].append(float(row[8]))
        sensors[9].append(float(row[9]))
        sensors[10].append(float(row[10]))

        sensors[11].append(FMconv(float(row[11])))

        sensors[12].append(float(row[12]))
        sensors[13].append(float(row[13]))
for i in range(14):
    plt.clf()
    plt.plot(np.linspace(0,numpoints * 1/100, numpoints + 1), sensors[i])
    plt.title(sense_names[i])
    plt.show()
