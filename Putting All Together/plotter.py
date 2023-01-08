import csv 
import matplotlib.pyplot as plt
import numpy as np

fil = open("datas.csv", "r")
csv = csv.reader(fil)

xVals = []
yVals = []

for row in csv: 
    xVals.append(row[0])
    yVals.append(row[1])

plt.ylim(ymin=0)
plt.xlim(xmin=0)
fig, (ax1) = plt.subplots(1, figsize=(15, 7))
ax1.plot(np.array(xVals), np.array(yVals), color='g', linestyle='-', lw=2)
ax1.set_ylim(0)
fig.show()
fig.waitforbuttonpress()