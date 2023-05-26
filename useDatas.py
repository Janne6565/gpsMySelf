import numpy as np
import matplotlib.pyplot as plot

datas = """0.67, 2.17;0.68, 2.32;0.78, 2.31;1.03, 2.44;0.93, 2.33;1.13, 2.65;0.92, 2.49;1.39, 4.7;1.57, 4.91;1.53, 4.8;1.73, 4.92;1.74, 5.08;1.89, 5.21;1.65, 5.08;3.39, 4.79;3.5, 5;3.55, 4.92;3.74, 5.17;3.71, 4.99;3.58, 5.1;3.01, 7.9;3.08, 7.85;2.94, 7.81;3.2, 8.06;3.31, 7.95;3.2, 7.88;3.32, 8.15;3.45, 8.06;3.39, 8.3;7.25, 10.56;7.51, 10.77;7.48, 10.93;7.35, 10.83;7.19, 10.71;7.36, 10.69;5.81, 8.52;6.08, 8.75;5.95, 8.63;5.92, 8.73;5.76, 8.62;3.41, 10.59;3.29, 10.49;3.18, 10.38;3.37, 10.36;3.5, 10.5;3.26, 10.3"""

infos = datas.split(";")

values = []

for info in infos: 
    values.append(info.split(","))

for value in values:
    for i in range(len(value)):
        if (value[i] != ''):
            value[i] = float(value[i])
        else:
            value[i] = None

abweichungen = []
xVal = []
yVal = []
for value in values: 
    abweichungen.append(value[1] - value[0])
    xVal.append(value[0])
    yVal.append(value[1])


x = [i / 4 for i in range(len(abweichungen))]


y = np.array(abweichungen)

plot.axis("equal")
plot.xlim(0, 8)
plot.ylim(0, 8) 
plot.plot(x, y, 'bo')
# plot.plot(np.array(xVal), np.array(yVal), 'ro')

plot.waitforbuttonpress()

print(abweichungen)