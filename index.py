import io
import requests
import qrcode
import lxml
import cchardet
import re
import pyshorteners
from random import randint
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
from PIL import Image, ImageOps, ImageDraw, ImageFont
from flask import Flask, request, render_template, send_file, abort
from docx import Document
from docx.shared import Inches, Mm


app = Flask(__name__)
shortener = pyshorteners.Shortener()

IMAGE_TAG = "og:image"
TITLE_TAG = "og:title"
IMAGE_OFFSET = 45
ARTICLE_IMAGE_SIZE = (160, 160)
ARTICLE_QR_SIZE = (180, 180)
TITLE_Y_POS = 8
TITLE_IGNORE_KEYS = ["awake", "watchtower", "videos"]
EXPECTED_DOMAIN = "www.jw.org"
TITLE_LENGTH_THRESHOLD = 60
DEFAULT_FONT = "assets/fonts/NotoSans-Bold.ttf"
URL_LENGTH_THRESHOLD = 200

DOC_ROWS = 9
DOC_COLUMNS = 4

WEB_HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"}

def gen_doc(img):
    document = Document()
    section = document.sections[0]
    section.header.is_linked_to_previous = True
    section.footer.is_linked_to_previous = True
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Mm(10.4)
    section.right_margin = Mm(10.4)
    section.top_margin = Mm(10.4)
    section.bottom_margin = Mm(10.4)
    table = document.add_table(rows=DOC_ROWS, cols=DOC_COLUMNS)
    for row in range(len(table.rows)):
        for col in range(len(table.columns)):
            paragraph = table.cell(row, col).paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(img, height=Inches(1))
    word_file = io.BytesIO()
    document.save(word_file)
    word_file.seek(0)
    return word_file

def gen_qr(article_link=""):
    if not article_link:
        return

    result = urlparse(article_link)
    if result.netloc.casefold() != EXPECTED_DOMAIN:
        abort(404, description=f"Please enter a link from {EXPECTED_DOMAIN}.")
    links = {}
    try:
        links = scrape_article(article_link=article_link)
    except Exception as er:
        print(er)
        abort(404, description=f"Opps!! Something is wrong somewhere. Please try another link.")
    left_image = get_article_image(image_url=links.get("image", ""))
    right_image = get_qr_image(article_link=article_link)
    article_size = left_image.size
    complete_qr_image = Image.new('RGB',(2*article_size[0], article_size[1]+IMAGE_OFFSET), (250,250,250))
    complete_qr_image.paste(left_image,(0,IMAGE_OFFSET))
    complete_qr_image.paste(right_image,(article_size[0],IMAGE_OFFSET - 10))

    draw_title(image=complete_qr_image, width=article_size[0], title=links.get("title", ""), lang=links.get("lang", "en"))
    complete_qr_image = draw_border(image=complete_qr_image)
    qr_file = io.BytesIO()
    complete_qr_image.save(qr_file, 'JPEG', quality=95)
    qr_file.seek(0)
    return qr_file

def scrape_article(article_link):
    page = requests.get(article_link, headers=WEB_HEADERS)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer(["meta", "link"]))
    image_tag = soup.find('meta', property=IMAGE_TAG)
    title_tag = soup.find('meta', property=TITLE_TAG)
    link_tag = soup.find('link', rel="alternate")
    return {"image" : image_tag["content"] , "title": title_tag["content"], "lang": link_tag.get("hreflang", "en")}

def get_article_image(image_url):
    response = requests.get(image_url, headers=WEB_HEADERS)
    webpage_image_bytes = io.BytesIO(response.content)
    article_image = Image.open(webpage_image_bytes)
    article_image = article_image.resize(ARTICLE_IMAGE_SIZE, Image.ANTIALIAS)
    article_image = add_margin(article_image, top=0, bottom=15, left=15, right=15, color=(250,250,250))
    return article_image

def prepare_logo():
    logo = Image.open("assets/images/siteLogo-jworg.png")
    basewidth = 140
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    return logo

def prepare_link(article_link):
    if len(article_link) > URL_LENGTH_THRESHOLD:
        article_link = shortener.tinyurl.short(article_link)
    return article_link

def get_qr_image(article_link):
    logo = prepare_logo()
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(prepare_link(article_link=article_link))
    QRcode.make()
    QRimg = QRcode.make_image(back_color=(250,250,250)).convert('RGB')

    pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    QRimg = QRimg.resize(ARTICLE_QR_SIZE, Image.ANTIALIAS)
    return QRimg

def draw_border(image):
    return ImageOps.expand(image, border=(2, 2, 2, 2), fill="black")

def get_language(lang):

    font_size = 34
    font_type = DEFAULT_FONT

    if "cmn" in lang:
        font_size = 28
        font_type = "assets/fonts/NotoSansSC-Bold.otf"

    if "ta" in lang:
        font_type = "assets/fonts/NotoSansTamil.ttf"
        
    if "my" in lang:
        font_size = 28
        font_type = "assets/fonts/NotoSansMyanmar-Bold.ttf"

    if "ja" in lang:
        font_size = 28
        font_type = "assets/fonts/NotoSansJP-Bold.otf"

    return font_type, font_size

def draw_title(image, width, title, lang):
    font_type, font_size = get_language(lang=lang)
    font = ImageFont.truetype(font_type, font_size)
    draw = ImageDraw.Draw(image)
    singleline_text(draw, process_title(title=title), font, xy=(0, TITLE_Y_POS),
                wh=(2*width, 30),
                alignment="center",)

def process_title(title):
    if "|" in title:
        partition = title.rpartition("|")
        if any(ext in partition[0].casefold() for ext in TITLE_IGNORE_KEYS):
            return partition[2]
        return partition[0]
    elif "—" in title:
        title = title.rpartition("—")[0]
    elif ":" in title:
        title = title.rpartition(":")[2]


    if len(title) > TITLE_LENGTH_THRESHOLD:
        first_non_alphanumeric_char = re.search(r'\W\s+', title).start()
        title = title[0 : first_non_alphanumeric_char + 1]
    
    return title

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
    container_width, container_height = wh
    x_offset = 0
    y_offset = 0
    font = font_info
    fontsize = font.size
    font_path = font.path

    text_width = font.getsize(text)[0]
    while text_width > container_width:
        # iterate until the text width is smaller than the assigned width of the text area
        fontsize -= 1
        font = ImageFont.truetype(font_path, fontsize)
        text_width = font.getsize(text)[0]

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(font_path, fontsize)
    updated_font_size = font.getsize(text)
    text_width = updated_font_size[0]
    text_height = updated_font_size[1]
    y_offset = (int(container_height) / 2) - (text_height / 2)
    if alignment == "center":
        x_offset = (int(container_width) / 2) - (text_width / 2)
    elif alignment == "right":
        x_offset = container_width - text_width

    drawing.text((x + x_offset, y + y_offset), text, font=font, fill=fill)

@app.route('/', methods =["GET", "POST"])
def index():    
    if request.method == "POST":
       article_link = request.form.get("article-link", "")
       img_file = gen_qr(article_link=article_link)
       word_doc = gen_doc(img=img_file)
       return send_file(word_doc, download_name=f"article-doc-{randint(10000, 99990)}.docx",as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document") 
    return render_template("index.jinja2")
if __name__=='__main__':
   app.run()
