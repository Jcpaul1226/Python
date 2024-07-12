#blurs an image
from PIL import Image,ImageFilter #imports modules image and imagefilter from library PIL

before = Image.open("bridge.jpg")
after = before.filter(ImageFilter.BoxBlur(1))
after.save("out.bmp")

#finds edges
after = before.filter(ImageFilter.FIND_EDGES)
after.save("edges.bmp")