from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter, TextConverter, XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
from app.models import Article, PDFFile
from app import db
from .textsanitizer import TextSanitizer


def convert_pdf_to_text(pdf_destination, pdf_name, input_journal, pages=None):
    case = "pdf"
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    manager = PDFResourceManager()
    codec = "utf-8"
    caching = True
    output = io.StringIO()
    converter = TextConverter(manager, output, codec=codec, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(pdf_destination, "rb")
    for page in PDFPage.get_pages(
        infile, pagenums, caching=caching, check_extractable=True
    ):
        interpreter.process_page(page)

    convertedPDF = output.getvalue()
    infile.close()
    converter.close()
    output.close()
    converted_text = TextSanitizer().sanitize(convertedPDF)

    insert_pdf_into_database(
        convertedPDF, converted_text, pdf_destination, pdf_name, input_journal
    )
    print("pdf uploaded")


def insert_pdf_into_database(
    convertedPDF, converted_text, pdf_destination, pdf_name, input_journal
):
    pdf = PDFFile(
        text=convertedPDF,
        converted_text=converted_text,
        pdf_url=pdf_destination,
        pdf_name=pdf_name,
        journal=input_journal,
    )
    db.session.add(pdf)
    db.session.commit()
