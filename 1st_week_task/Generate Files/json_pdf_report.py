# Read html file and converts to pdf

import pdfkit
import logging
import os.path

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/json_pdf_report.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

options = {
    'page-height': '400',
    'page-width': '2000',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
}

try:
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    try:
        logger.info("Reading HTML file")
        # converts html page to pdf document
        pdfkit.from_file('./files/json_html.html', 'files/json_html.pdf', options=options, configuration=config)
        logger.info("pdf file Generted Successfully")
    except Exception as ex:
        logger.error("Error occured %s---%s", ex, ex.__class__.__name__)

except (NotADirectoryError, FileNotFoundError, IOError) as ex:
    logger.error("wkhtmltopdf.exe confiquration fail-%s ---%s", ex, ex.__class__.__name__ )






