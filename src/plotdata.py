###To use this file, the only thing you need to change is the variable path1
path1 = "C:\\Users\\chris\\Hybrid-Control\\src\\05 high dip tube.csv"

###If you want to plot multiple files one after another, build this list of pathoffsets and paths
##Changing the pathoffset cuts the plotted data at the end by that amount, can be used to remove the 
##impact of disconnecting electronics on the graph
##To change the smoothing amount, adjust wind and order (see savitzky_golay documentation)
wind = 21
order = 3
path1offset = 1
PATHS = [[path1offset, path1]]# [path2offset, path2], [path3offset, path3], [path4offset, path4]]

import csv
import numpy as np
import matplotlib.pyplot as plt

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(int(window_size))
        order = np.abs(int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

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
    v_c = 4.84 #TODO implement this
    alpha = 0.00392 # Ohms/Ohms/ºC
    r_nom = 100

    r_rtd = (r_ref * (v_c - V))/(V)
    delta_temp = (1/alpha) * ((r_rtd/r_nom) - 1)
    return (9/5) * delta_temp + 32 #return in *F



sense_names = ["PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PT7", "PT8", "TC1", "TC2", "TC3", "FM1", "LD1", "LD2"]

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
            sensors[1].append(PT3kConv(float(row[1])))
            sensors[2].append(PT3kConv(float(row[2])))
            sensors[3].append(PT3kConv(float(row[3])))
            sensors[4].append(PT15kconv(float(row[4])))
            sensors[5].append(PT2kConv(float(row[5])))
            sensors[6].append(PT2kConv(float(row[6])))
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
            #axs[row][col].plot(numPoints[:-offset], sensors[row*4+col][:-offset])
            axs[row][col].plot(numPoints[:-offset], savitzky_golay(np.array(sensors[row*4+col][:-offset]), wind, order), color='red')
            axs[row][col].title.set_text(sense_names[row*4+col])
        else:
            axs[row][col].set_visible(False)
    fig.suptitle(pathtoFilename(path))
    plt.show()

