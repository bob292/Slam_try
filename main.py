import bisect
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math




def print_hi(name):
    print(f' {name}')


if __name__ == '__main__':
    print_hi('Start reading dataset')

    def data_gen(): #generator for the Funcanimation
        #reading dataset from file:
        with open(r'C:\Users\shenx\Downloads\localized.data', 'r') as f1:
            list1 = f1.readlines()
            pointcloud = [[0] * 180] * (int)(len(list1) / 5)
            estodo = [[0] * 3] * (int)(len(list1) / 5)
        j = k = 0
        for i in range(0, len(list1)):
            if list1[i][0] == 'L': #pointcloud data
                pointcloud[j] = [float(i) for i in list1[i][1:].split()][1:]
                j = j + 1
            if list1[i][0] == 'E': #robots location data
                estodo[k] = [float(i) for i in list1[i][1:].split()]
                k = k + 1
        f1.closed

        # generate the coordinate of the pointcloud and the robot
        poclco = [[[0] * 2] * 180] * (int)(len(list1) / 5)
        for i in range(0,int(len(pointcloud)/10)):# plot one measurement in each ten measurements to reduce the time consumption
            o = i * 10
            for dis in range(0,180):
                xplus = -1 * pointcloud[o][dis * 4 + 3] * np.sin(estodo[o][3]) + pointcloud[o][dis * 4 + 2] * np.cos(estodo[o][3])
                yplus = pointcloud[o][dis * 4 + 3] * np.cos(estodo[o][3]) + pointcloud[o][dis * 4 + 2] * np.sin(estodo[o][3])
                if np.sqrt(np.square(xplus) + np.square(yplus)) > distance:
                    continue
                poclco[o][dis][0] = estodo[o][1] + xplus
                poclco[o][dis][1] = estodo[o][2] + yplus
                #pointcloud's coordinate:
                xl = poclco[o][dis][0]
                yl = poclco[o][dis][1]
                #robot's coordinate:
                xr = estodo[o][1]
                yr = estodo[o][2]
                yield xr,yr,xl,yl





    def init():
        del xrdata[:]
        del yrdata[:]
        del xldata[:]
        del yldata[:]
        for i in range(1):
            ax.set_ylim(-20, 20)
            ax.set_xlim(-20, 20)
            # line.append(ax[i].plot([],[],lw=2))
        return line


    def run(data):
        # update the data
        xr, yr,xl,yl = data
        xrdata.append(xr)
        yrdata.append(yr)
        xldata.append(xl)
        yldata.append(yl)
        for i in range(2):
            xmin, xmax = ax.get_xlim()
            if xl >= xmax:
                ax.set_xlim(xmin, 2 * xmax)
                ax.figure.canvas.draw()
            if i == 0:
                line[i].set_data(xrdata, yrdata)
            if i == 1:
                line[i].set_data(xldata, yldata)
        return line

    distance = 30
    fig, ax = plt.subplots(1,1)
    line = []

    line.extend(ax.plot([], [],"ro",markersize = 0.3))
    line.extend(ax.plot([], [],"bo",markersize = 0.3))
    ax.grid()
    xrdata, yrdata, xldata, yldata = [], [], [], []
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=0.01, repeat=False, init_func=init,
                                  save_count=500)
    ani.save("dubwave.gif", writer='pillow')
    plt.show()







