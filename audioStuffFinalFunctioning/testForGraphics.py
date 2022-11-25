import matplotlib.pyplot as plt
import numpy as np
import time


fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
fig.show()

xf = np.linspace(0, 100, 50)     # frequencies (spectrum)
arr = []
for i in range(50):
    arr.append(i)

line_fft, = ax2.semilogx(xf, np.array(arr), '-', lw=2)
fig.canvas.draw()

fig.canvas.flush_events()


time.sleep(30)