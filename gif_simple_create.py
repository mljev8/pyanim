import glob
from PIL import Image

path = '/path/to/some/pictures'
fp_in = path + "/*.png"
fp_out = path + "/image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=200, loop=0)
