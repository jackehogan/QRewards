import qrcode
from PIL import Image

img = qrcode.make('https://qrewards.herokuapp.com/qrewards')
img.save("sample.png")