import qrcode
from PIL import Image

img = qrcode.make('https://qrewards.herokuapp.com/qrewards/LA')
img.save("LA_QR_Code.png")

img = qrcode.make('https://qrewards.herokuapp.com/qrewards/TLV')
img.save("TelAviv_QR_Code.png")