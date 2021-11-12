import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def cluster(center, radius=15, n=200):
    c = np.r_[center]
    r = np.r_[radius]
    x, y, z = np.random.uniform(c-r, c+r, size=(n, 3)).T
    return x, y, z

# create random cluster
x1, y1, z1 = cluster((25, 15,  5))
x2, y2, z2 = cluster(( 5,  5, 20))

fig = plt.figure()
ax = Axes3D(fig)
ax.grid(False)

def init():
    ax.scatter(x1, y1, z1, c='r', marker='o', alpha=0.5)
    ax.scatter(x2, y2, z2, c='g', marker='d', alpha=0.5)
    return fig,

def update_func(i):
    ax.view_init(elev=10.0, azim=i)
    return fig,

movie = FuncAnimation(fig,
                      update_func, 
                      init_func=init,
                      frames=360, 
                      interval=20, 
                      blit=False)

if(0):
    movie.save('clusters.mp4')

plt.show(block=False)

if(0): # generate .gif
    cmd =  'ffmpeg -i ./clusters.mp4 '
    cmd += '-vf "fps=10,scale=640:-1" ' 
    cmd += '-loop 0 ./clusters.gif'
    os.system(cmd)
