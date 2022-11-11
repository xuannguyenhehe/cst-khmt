from PIL import Image

basewidth = 1000
img = Image.open('bien_so.jpg')
print(img.size)
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
# img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
img = img.resize((1024,1024), Image.Resampling.LANCZOS)
print(img.size)
img.save('bien_so_2.png')