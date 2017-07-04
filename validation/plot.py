import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(2,1,2)
ax2 = fig.add_subplot(2,1,1)
def curveplot(i):
    timestamp = []
    price = []
    signal = []
    wma_signal = []
    
    fo = open('M:/forex/17_06_15_eur_usd.csv','r')
    lines = fo.readlines()[1:]
    for line in lines:
        timestamp.append(datetime.strptime(line.split(',')[3],"%y-%m-%d %H:%M:%S"))
        price.append(float(line.split(',')[1]))
        signal.append(float(line.split(',')[5]))
        wma_signal.append(float(line.split(',')[6]))
    ax1.clear()
    ax1.plot(timestamp,signal,timestamp,wma_signal)
    ax2.plot(timestamp,price,'r')
ani = animation.FuncAnimation(fig,curveplot,interval=100000)
plt.show()
        
