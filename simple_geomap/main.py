import numpy as np
import matplotlib.pyplot as plt

plt.close('all')
plt.rcParams['figure.autolayout'] = True

def make_bbox(x0,y0,x1,y1):
    return (x0,x0,x1,x1,x0),(y0,y1,y1,y0,y0)

def latlon_sinusoidal(lat, lon, lambda0=8.5, phi0=55.0):
    """ 
    Projection, 2D visualization on a planar map
    https://en.wikipedia.org/wiki/World_Geodetic_System
    https://en.wikipedia.org/wiki/Sinusoidal_projection 
    """
    r = 6371. # WGS84 mean Earth radii
    deg2rad = np.pi/180.
    x = r * deg2rad * (lon-lambda0) * np.cos(deg2rad * lat)
    y = r * deg2rad * (lat-phi0)
    return x,y

#https://hub.arcgis.com/datasets/UIA::uia-world-countries-boundaries
#https://opendata.arcgis.com/datasets/252471276c9941729543be8789e06e12_0.geojson
geojson = 'country_boundaries.geojson'
def get_boundary_from_file(country='DK', fname=geojson):
    """ 
    Collect (lon,lat) coordinates from file 
    Get correct line by matching against "ISO": "DK", "ISO": "FR", ... 
    """
    assert isinstance(country, str)
    assert len(country) == 2
    with open(fname, 'r') as infile:
        matchcase = '"ISO": "{}"'.format(country)
        while(True):
            line = infile.readline()
            if(len(line) == 0):
                raise IOError(f'Country {country} not found!')
            if(line.count(matchcase)):
                break
    line = line.replace('}','').replace(',\n','') # EOL trimming
    idx = line.find('"coordinates": ')
    coordinates = eval( line[idx+14:] ) # list of lists
    #coordinates = [a[0] for a in coordinates]
    coordinates = [np.round(np.array(a[0]),8) for a in coordinates]
    print(f'{len(coordinates):>3} distinct polygons found for {country}')
    return coordinates
#

apply_map_projection = False
country_list = ['DK','DE','SE','NO','FR','GB','ES']

# Read country boundaries and assign as two-letter objects
for XX in country_list:
    exec('{} = get_boundary_from_file(country=XX)'.format(XX))

# Create figure 
fig,ax = plt.subplots()
for XX in country_list:
    data = eval(XX)
    n_polygons = len(data)
    for i in range(n_polygons):
        p = data[i]
        x,y = p[:,0],p[:,1] # lon,lat
        if(apply_map_projection == True):
            x,y = latlon_sinusoidal(p[:,1],p[:,0])
        ax.plot(x,y,'g')

bbox_x,bbox_y = make_bbox(10.6-3.,57.75+1.25,10.6+3.,57.75-1.25)
ax.plot(bbox_x,bbox_y,'r')

# Display some DK cities
dtype_ = [('name','<U30'),('lat','float32'),('lon','float32')]
city = np.genfromtxt('cities_dk.csv', names=True, dtype=dtype_)

x0,y0 = city['lon'],city['lat']
if(apply_map_projection == True):
    x0,y0 = latlon_sinusoidal(city['lat'],city['lon'])
ax.plot(x0,y0,'ro')

m = len(city)
for i in range(m):
    ax.text(x0[i],y0[i],city['name'][i])

ax.set_aspect('equal')
plt.show(block=False)
