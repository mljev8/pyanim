"""
Generic templates, copy-paste
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

n = 100
grid = np.arange(n)
data = 2. + 5.*np.random.standard_normal(size=n)

# animation with two views
fig = plt.figure(figsize=(6.,6.))
ax0 = fig.add_subplot(121, projection='polar')
ax1 = fig.add_subplot(122)

# lhs view
sweeper, = ax0.plot([],[]) # <-- notice the trailing comma
points,  = ax0.plot([],[],'r.')

# rhs view
ax1.plot(grid, data, '.', ms=2.) # static
artist1, = ax1.plot([], [], color='r') # <-- notice the trailing comma
artist2, = ax1.plot([], [], color='k', marker='o')
ax1.legend(['Data (static)','Artist 1', 'Artist 2'], fontsize=10)

# manipulator / updater
def update_func(i, artist1, artist2, data, ax1):
    artist1.set_data()
    artist2.set_data()
    ax1.set_xlim()
    ax1.set_ylim()
    return artist1,artist2, # note: blit=True requires iterable

print('Creating animation')
movie = FuncAnimation(fig, 
                      update_func, 
                      frames = range(40,70,2), # for i in iterable  
                      fargs = (artist1,artist2,data,ax),
                      interval = 25, # [ms]
                      blit = False)

if(0):
    print('Saving animation (could take a while...)')
    movie.save('test_movie.mp4')

# 
plt.show(block=False)

#