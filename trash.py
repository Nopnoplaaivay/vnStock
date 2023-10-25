import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

data1 = np.random.rand(10, 10)
data2 = np.random.rand(10, 10)

fig = plt.figure(figsize=(8, 4))
gs = fig.add_gridspec(1, 2)

fig_left = fig.add_subfigure(gs[:, 0])
fig_right = fig.add_subfigure(gs[:, 1])

fig_left.set_facecolor("red")
ax_left = fig_left.subplots()
ax_left.set_title("red")
# img_left = ax_left.imshow(data1, aspect="equal")

fig_right.set_facecolor("blue")
ax_right = fig_right.subplots()
ax_right.set_title("blue")
# img_right = ax_right.imshow(data2, aspect="equal")

plt.show()