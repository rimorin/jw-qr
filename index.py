import io
import requests
import qrcode
import lxml
import cchardet
from bs4 import BeautifulSoup, SoupStrainer
from PIL import Image, ImageOps, ImageDraw, ImageFont
from flask import Flask, request, render_template, send_file, abort
app = Flask(__name__)

def gen_qr(article_link=""):
    page = requests.get(article_link)
    meta_only = SoupStrainer('meta',{})
    soup = BeautifulSoup(page.text, 'lxml', parse_only=meta_only)
    image_tags = soup.find('meta', property="og:image")
    title_tags = soup.find('meta', property="og:title")
    links = {"image" : image_tags["content"] , "title": title_tags["content"]}
    logo = Image.open("siteLogo-jworg.png")
    basewidth = 140
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    QRcode.add_data(article_link)

    QRcode.make()
    QRimg = QRcode.make_image(back_color=(250,250,250)).convert('RGB')

    pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    response = requests.get(links.get("image"))
    webpage_image_bytes = io.BytesIO(response.content)

    image1 = Image.open(webpage_image_bytes)

    image1 = image1.resize((160, 160))
    image2 = QRimg.resize((180, 180))
    image1 = add_margin(image1, top=0, bottom=15, left=15, right=15, color=(250,250,250))
    image1_size = image1.size

    offset = 45

    new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]+offset), (250,250,250))
    new_image.paste(image1,(0,offset))
    new_image.paste(image2,(image1_size[0],offset - 10))

    font = ImageFont.truetype("Roboto-Bold.ttf", 34)
    draw = ImageDraw.Draw(new_image)

    removed_pipe_text = links.get("title", "").rpartition("|")[0]
    singleline_text(draw, removed_pipe_text, font, xy=(0, 8),
                wh=(2*image1_size[0], 30),
                alignment="center",)

    border = (2, 2, 2, 2)
    new_image = ImageOps.expand(new_image, border=border, fill="black")
    img_io = io.BytesIO()
    new_image.save(img_io, 'JPEG')
    img_io.seek(0)
    return img_io


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result
def singleline_text(
    drawing, text, font_info, xy, wh, fill="#000", alignment=None, decoration=None
):
    x, y = xy
    width, _ = wh
    x_offset = 0
    font = font_info
    fontsize = font.size
    font_path = font.path

    text_width = font.getsize(text)[0]
    while text_width > width:
        # iterate until the text width is smaller than the assigned width of the text area
        fontsize -= 1
        font = ImageFont.truetype(font_path, fontsize)
        text_width = font.getsize(text)[0]

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(font_path, fontsize)
    text_width = font.getsize(text)[0]
    if alignment == "center":
        x_offset = (int(width) / 2) - (text_width / 2)
    elif alignment == "right":
        x_offset = width - text_width

    drawing.text((x + x_offset, y), text, font=font, fill=fill)

@app.route('/', methods =["GET", "POST"])
def index():    
    if request.method == "POST":
       article_link = request.form.get("article-link")
       temp_img_file = gen_qr(article_link=article_link)
       return send_file(temp_img_file, mimetype='image/jpg') 
    return render_template("index.jinja2")
if __name__=='__main__':
   app.run()
