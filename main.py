# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import bisect
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
#import pyqtgraph as pg



#def plotdata():



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f' {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Start reading dataset')
    # with open(r'C:\Users\shenx\Downloads\localized.data','r') as f1:
    #     list1 = f1.readlines()
    #     pointcloud = [[0] * 180] * (int)(len(list1)/5)
    #     estodo = [[0] * 3] * (int)(len(list1)/5)
    # j = k = 0
    # #print(len(list1))
    # #print(type(list1))
    # for i in range(0,len(list1)):
    #     if list1[i][0] == 'L':
    #         pointcloud[j] = [float(i) for i in list1[i][1:].split()]
    #         j = j + 1
    #
    #     if list1[i][0] == 'E':
    #         estodo[k] = [float(i) for i in list1[i][1:].split()]
    #         k = k + 1
    #
    # f1.closed
    ####################################################################################################################
    # trace_x = []
    # trace_y = []
    # fig = plt.figure()
    # #plt.xlim(-8, 20)
    # #Splt.ylim(-8, 8)
    # for q in range(0,len(estodo)):
    #     trace_x.append(estodo[q][1])
    #     trace_y.append(estodo[q][2])
    #     #plt.clf()
    #     #plt.scatter(trace_x[q],trace_y[q])
    #     #print(trace_x)
    #     temp = ax.scatter(trace_x[q],trace_y[q])
    #     tmp.append(temp)
    #
    # ani = animation.FuncAnimation(fig,)
    # ani.save('path.gif')
    # plt.show


    # app = pg.mkQApp()
    # win = pg.GraphicsWindow()
    # p = win.addPlot()
    # p.setRange(xRange = [-10.0,10.0], yRange = [-10.0,10.0], padding= 0)
    # curve = p.plot(pen = 'y')



    #plt.plot(trace_x,trace_y)

    #####################################################################################
    # def data_gen():
    #     for cnt in range(500):
    #         t = cnt / 10
    #         yield t, np.sin(2 * np.pi * t) * np.exp(-t / 10.)

    def data_gen():
        with open(r'C:\Users\shenx\Downloads\localized.data', 'r') as f1:
            list1 = f1.readlines()
            pointcloud = [[0] * 180] * (int)(len(list1) / 5)
            estodo = [[0] * 3] * (int)(len(list1) / 5)
        j = k = 0
        # print(len(list1))
        # print(type(list1))
        for i in range(0, len(list1)):
            if list1[i][0] == 'L':
                pointcloud[j] = [float(i) for i in list1[i][1:].split()]
                j = j + 1
            if list1[i][0] == 'E':
                estodo[k] = [float(i) for i in list1[i][1:].split()]
                k = k + 1
        f1.closed
        poclco = [[[0] * 2] * 180] * (int)(len(list1) / 5)
        print(np.sin(math.pi/2))
        for o in range(0,len(pointcloud)):
            for dis in range(0,180):
                poclco[o][dis][0] = estodo[o][1] + pointcloud[o][dis] * np.cos(estodo[o][3] + (dis + 1) / 180 * math.pi - math.pi/2)
                poclco[o][dis][1] = estodo[o][2] + pointcloud[o][dis] * np.sin(estodo[o][3] + (dis + 1) / 180 * math.pi - math.pi/2)
                x = poclco[o][dis][0]
                y = poclco[o][dis][1]
                yield x,y
        trace_x = []
        trace_y = []
        # for q in range(0, len(estodo)):
        #     t = estodo[q][1]
        #     y = estodo[q][2]
        #     ang = estodo[q][3]
        #     yield t,y





    def init():
        del xdata[:]
        del ydata[:]
        for i in range(1):
            ax.set_ylim(-20, 5)
            ax.set_xlim(-10, 20)
            # line.append(ax[i].plot([],[],lw=2))
        return line


    def run(data):
        # update the data
        t, y = data
        xdata.append(t)
        ydata.append(y)
        for i in range(1):
            xmin, xmax = ax.get_xlim()
            if t >= xmax:
                ax.set_xlim(xmin, 2 * xmax)
                ax.figure.canvas.draw()
            line[i].set_data(xdata, ydata)
        return line


    fig, ax = plt.subplots(1,1)
    line = []  # 存储plot()返回的lines对象，需要作为全局变量，
    for i in range(1):
        line.extend(ax.plot([], [],"ro",markersize = 1))
        ax.grid()
    xdata, ydata = [], []
    # 由于传入的frames参数是一个generator，save()不能探知到要存储的帧数，所以只默认保存100帧，通过save_count参数来指定正确的保存帧数。
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=1, repeat=False, init_func=init,
                                  save_count=500)
    ani.save("dubwave.gif", writer='pillow')
    plt.show()

#######################################################################################################################
    # x = np.random.rand(40)
    # y = np.random.rand(40)
    #
    # plt.figure(1)
    # plt.scatter(x, y, s=60)
    # plt.axis([0, 1, 0, 1])
    # plt.show()
    #
    # # animation of a scatter plot using x, y from above
    # # ------------------------------------------------------------------------------
    #
    # fig = plt.figure(2)
    # ax = plt.axes(xlim=(0, 1), ylim=(0, 1))
    # scat = ax.scatter([], [], s=60)
    #
    #
    # def init():
    #     scat.set_offsets([])
    #     return scat,
    #
    #
    # def animate(i):
    #     data = np.hstack((x[:i, np.newaxis], y[:i, np.newaxis]))
    #     scat.set_offsets(data)
    #     return scat,
    #
    #
    # anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x) + 1,
    #                                interval=200, blit=False, repeat=False)
    # anim.save('animation.mp4')

#alireza.asvadi
#formulate quiver







