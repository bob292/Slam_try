import pickle
import bisect
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import math
import cv2



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
        for i in range(0,1):#(int)(len(estodo)/10)):# plot one measurement in each ten measurements to reduce the time consumption
            o = i * 10
            for dis in range(0,180):
                #################################################
                # pointcloud's coordinate(transformed):
                # xplus = -1 * pointcloud[o][dis * 4 + 3] * np.sin(estodo[o][3]) + pointcloud[o][dis * 4 + 2] * np.cos(estodo[o][3])
                # yplus = pointcloud[o][dis * 4 + 3] * np.cos(estodo[o][3]) + pointcloud[o][dis * 4 + 2] * np.sin(estodo[o][3])
                # if np.sqrt(np.square(xplus) + np.square(yplus)) > distance:
                #     continue
                # poclco[o][dis][0] = estodo[o][1] + xplus
                # poclco[o][dis][1] = estodo[o][2] + yplus
                # xl = poclco[o][dis][0]
                # yl = poclco[o][dis][1]
                #################################################
                # pointcloud's coordinate(not transformed):
                xl = pointcloud[o][dis * 4 + 2]
                yl = pointcloud[o][dis * 4 + 3]
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
    resolution = 0.2


    def makegridmap(data, resolution):
        x = np.arange(start=max(data), stop=min(data) + resolution, step=resolution)
        y = np.arange(start=max(data), stop=min(data) + resolution, step=resolution)
        l = np.full(shape=(len(x),len(y)),fill_value=1)
        return l


    def bresenham(x1,y1,x2,y2,resolution):

        x = (int)(x1 / resolution) * resolution
        y = (int)(y1 / resolution) * resolution
        delta_x = np.abs(x2 -x1)
        delta_y = np.abs(y2 -y1)
        s_x = np.sign(x2 - x1) * resolution
        s_y = np.sign(y2 - y1) * resolution

        if delta_y > delta_x:
            delta_x,delta_y = delta_y,delta_x
            interchange = True
        else:
            interchange = False

        A = 2 * delta_y
        B = 2 * (delta_y - delta_x)
        E = 2 * delta_y -delta_x
        coo_bre = []
        coo_bre.append([x,y])
        for i in range(0 ,(int)(delta_x / resolution)):
            point = []
            if E < 0:
                if interchange:
                    y += s_y
                else:
                    x += s_x
                E = E + A
            else:
                y += s_y
                x += s_x
                E = E + B
            point.append(x)
            point.append(y)
            coo_bre.append(point)
        coo_bre.pop()
        return coo_bre

    def pixelplot(resolution, xldata, yldata, xrdata, yrdata):
        zz = []
        xbre = []
        ybre = []
        gridmap = np.zeros(((int)(35 / resolution), (int)(35 / resolution)))
        for i in range(0, len(xrdata)):
            zi = bresenham(xrdata[i], yrdata[i], xldata[i], yldata[i], resolution)
            zz += zi
        for q in range(0, len(zz)):
            xbre.append(zz[q][0])
            ybre.append(zz[q][1])

        # for i in range(0, len(xbre)): #drawing lines by using bresenham
        #     x = (int)((xbre[i] + 10) / resolution)
        #     y = (int)((ybre[i] + 15) / resolution)
        #     gridmap[y][x] = 0.6

        for q in range(0,len(xldata)): #drawing object detected
            x = (int)((xldata[q] + 10) / resolution)
            y = (int)((yldata[q] + 15) / resolution)
            gridmap[y][x] = 0.6

        im = plt.imshow(gridmap[::-1], cmap = 'gray', interpolation='none')
        #cbar = plt.colorbar(im)
        plt.axis('off')
        plt.savefig('scan.jpg',bbox_inches='tight',pad_inches=0)
        plt.show()

    pixelplot(resolution, xldata, yldata, xrdata, yrdata)
    def houghp():
        img = cv2.imread('scan.jpg',cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,200)
        lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength=10,
                                maxLineGap=250)
        for line in lines:
            print(lines)
            x1,y1,x2,y2 = line[0]
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            cv2.imshow("Result Image",img)
        cv2.waitKey()

    houghp()







