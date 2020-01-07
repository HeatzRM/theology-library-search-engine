try:
    import Image
except ImportError:
    import PIL
    from PIL import Image
    from PIL import ImageFilter
import pytesseract
from app.models import Article, Page
from app import db
import os
from .textsanitizer import TextSanitizer

"""
function that calls the pytesseract to convert image into text
and inserts into the database
"""


def convert_list_img_to_txt(
    list_of_image_directory, list_of_page_image_names, input_journal
):
    os.chdir(os.path.dirname(__file__))
    i = 0
    for image_url in list_of_image_directory:
        text = pytesseract.image_to_string(Image.open(image_url))
        converted_text = TextSanitizer().sanitize(text)
        insert_page_into_database(
            text, converted_text, image_url, list_of_page_image_names[i], input_journal
        )
        db.session.commit()
        i = i + 1


def insert_page_into_database(
    text, converted_text, image_url, image_name, input_journal
):
    page = Page(
        text=text,
        converted_text=converted_text,
        page_url=image_url,
        journal=input_journal,
        page_name=image_name,
    )
    db.session.add(page)
    db.session.commit()
    print("page uploaded")
