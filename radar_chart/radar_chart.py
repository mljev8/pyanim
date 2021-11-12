"""
Make small animation showing a radar chart
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
rand = np.random.random
randn = np.random.standard_normal

plt.rcParams['font.size'] = 10.
plt.rcParams['figure.autolayout'] = True

r_max = 100.
f_sweeper = 1/100.

# prep animation with two views
fig = plt.figure() # figsize=(6.,6.)
ax0 = fig.add_subplot(121, projection='polar')
ax1 = fig.add_subplot(122)

# lhs view: radar chart
sweeper, = ax0.plot([],[]) # <-- notice the trailing comma
points,  = ax0.plot([],[],'r.')
ax0.set_rmax(r_max)
ax0.set_rticks([0.,r_max/2,r_max])
ax0.set_rlabel_position(-22.5) # rotate radial labels a bit
#ax0.set_theta_zero_location()
ax0.set_thetagrids(45.*np.arange(8),labels=['','','N']+5*[''])
ax0.grid(True)

# rhs view: height profiles
ax1.plot(np.arange(10)-5., np.arange(10)-5.)
artist1, = ax1.plot([], [], color='r')
artist2, = ax1.plot([], [], color='k', marker='o')

def update_func(i, sweeper, points, artist1, artist2):
    # random data
    rot = -2.*np.pi*f_sweeper*i
    n = int(50.*rand())
    angles = 2.*np.pi*rand(size=n)
    radii = 30.*np.abs(randn(size=n))
    # apply
    sweeper.set_data(np.r_[rot,rot],np.r_[0.,r_max])
    if(i%5 == 0):
        points.set_data(angles,radii)
    artist1.set_data(randn(size=5),randn(size=5))
    artist2.set_data(randn(size=15),randn(size=15))
    return sweeper,points,artist1,artist2,

print('Creating animation')
movie = FuncAnimation(fig, 
                      update_func, 
                      frames = range(600), # for i in iterable  
                      fargs = (sweeper,points,artist1,artist2),
                      interval = 100, # [ms]
                      blit = False)

if(0):
    print('Saving animation (could take a while...)')
    movie.save('radar_chart.mp4')

# 
plt.show(block=False)

#