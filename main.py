from PIL import ImageDraw, Image, ImageFont
import qrcode
from uuid import uuid4
from flask import Flask, request
from json import loads
app=Flask(__name__)
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
products=loads(open('products.json', 'r', encoding='utf8').read())
@app.route("/")
def application():
    product_name=request.args.get("name")
    product_price=int(request.args.get("price"))
    gst=product_price/10
    total_price=product_price=gst
    font=ImageFont.truetype('font/tenor-sans.ttf', size=100)
    img=Image.open('invoice.png')
    code=qrcode.QRCode(box_size=10)
    code.add_data("https://paytm.com")
    img_qr = code.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(93,71,62)))
    draw=ImageDraw.Draw(img)
    draw.text((700, 180), product_name, font=font, fill="#000000")
    draw.text((700, 480), f"{product_price} Rs", font=font, fill="#000000")
    draw.text((700, 780), f"{gst} Rs", font=font, fill="#000000")
    draw.text((880, 1080), f"{total_price} Rs", font=font, fill="#000000")
    img.paste(img_qr, (1100, 1700))
    uu=uuid4()
    img.save(f"static/edit{uu}.png")
    return f"static/edit{uu}.png"
@app.route("/products")
def product():
    return {'products':products}
if __name__=="__main__":
    app.run(host="0.0.0.0")