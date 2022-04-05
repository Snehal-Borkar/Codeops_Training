import logging
import pandas
from json2xml import json2xml
from json2xml.utils import readfromstring
import json
import pdfkit

logger = logging.getLogger()


class XConverter:
    """
    This class converts provided dataframe to csv, xml, html, pdf file.

    Attributes:
        df (pandas.Dataframe): Pandas dataframe as input to converter methods
        file_name (str): Name of output file.
    """

    def __init__(self, df, file_name):
        """
        The constructor for class XConverter to initialize attributes.
        :param df: Pandas dataframe as input to converter methods
        :param file_name: Name of output file.
        """
        self.df = df
        self.file_name = file_name
        self.validate_param()

    def validate_param(self):
        """
        Validates the initialize parameters
        :return: None
        """
        if not isinstance(self.df, pandas.DataFrame):
            logger.error("df is not instance of pandas.DataFrame, not %s", type(self.df))
            raise TypeError("df must be an instance of pandas.DataFrame, not %s" % type(self.df))

        if self.df.empty:
            logger.error("Dataframe pass must not be empty")
            raise ValueError("Dataframe pass must not be empty")

        if not isinstance(self.file_name, str):
            logger.error("Type of file_name must be of <class: str>, not %s", type(self.file_name))
            raise TypeError("Type of file_name must be of <class: str>. not %s" % type(self.file_name))

    def df_csv(self):
        """
        Generates csv file from pandas Dataframe to provided file name.
        :return: None
        """
        ext = self.file_name.split(".")
        if ext[-1] == "csv":
            try:
                logger.info("Generating %s...", self.file_name)
                self.df.to_csv(self.file_name, index=False, encoding='utf-8-sig')
                logger.info("%s file generated successfully", self.file_name)
            except PermissionError as ex:
                logger.error("%s : %s , cannot write in already opened file", ex.__class__.__name__, ex)
                raise PermissionError("%s :  cannot write in already opened file" % ex)
        else:
            logger.error("csv_file must have .csv extention and not %s", ext[-1])
            raise ValueError("csv_file_name must ends with .csv extension, not %s" % ext[-1])

    def df_xml(self):
        """
        Converts pandas dataframe to xml file.
        :return: None
        """

        un_flat_dict = self.df.to_dict(orient='records')
        json_str = json.dumps(un_flat_dict)

        data = readfromstring(json_str)

        logger.info("Converting to xml...")
        xml_data = json2xml.Json2xml(data).to_xml()  # get the xml from a json string

        ext = self.file_name.split(".")
        if ext[-1] != "xml":
            logger.error("xmlfile must have .xml extention and not %s", ext[-1])
            raise ValueError("xmlfile_name must ends with .xml extension, not %s" % ext[-1])

        try:
            logger.info("Writing to %s...", self.file_name)
            with open(self.file_name, "w") as xml_file:
                xml_file.write(xml_data)
            logger.info("%s file generated successfully", self.file_name)
        except (IOError, OSError) as ex:
            logger.error("%s - %s", ex.__class__.__name__, ex)
            raise IOError("%s - %s" % ex.__class__.__name__ % ex)

    def df_html(self, render_images=None):
        """
        Converts pandas dataframe to table html file.
        :param render_images: (list) list of df column name to render images in HTML page
        :return: None
        """
        def path_to_image_html(path):
            """
            Values from dataframe are edited or changes format.
            :param path: url for image.
            :return: Renderable html element.
            """

            return '<img src="' + path + '" width="60" >'

        if render_images is not None:
            value = path_to_image_html
            formatter_dict = {}
            for key in render_images:
                formatter_dict.update({key: value})
        else:
            formatter_dict = None

        ext = self.file_name.split(".")
        if ext[-1] == "html":
            try:
                logger.info("Generating %s...", self.file_name)
                self.df.to_html(self.file_name, escape=False, index=False, encoding="utf-8-sig",
                           formatters=formatter_dict)
                logger.info("%s file generated successfully", self.file_name)
            except (IOError, OSError) as ex:
                logger.error("%s-%s", ex.__class__.__name__, ex)
                raise IOError("%s-%s", ex.__class__.__name__, ex)
        else:
            logger.error("htmlfile must have .html extention and not %s", ext[-1])
            raise ValueError("htmlfile_name must ends with .html extension, not %s" % ext[-1])

    options = {
        'page-height': '400',
        'page-width': '2000',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
    }

    def df_pdf(self, htmlfile_name=None, options=options, wkhtmltopdf_path=None):
        """
        Reads html file and converts it to pdf file.
        :param htmlfile_name: File to read HTML source.
        :param options: Size of output pdf file.
        :param wkhtmltopdf_path: path of the wkhtmltopdf.exe file
        :return: None
        """

        import os.path

        file_exists = os.path.exists(htmlfile_name)
        if file_exists:
            ext = self.file_name.split(".")
            if ext[-1] == "pdf":
                try:
                    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

                    logger.info("Reading HTML file")
                    # converts html page to pdf document
                    pdfkit.from_file(htmlfile_name, self.file_name, options=options, configuration=config)
                    logger.info("pdf file Generted Successfully")

                except (IOError, OSError) as ex:
                    logger.error("%s - %s", ex.__class__.__name__, ex)
                    raise IOError("Error occured: %s:" % ex)
            else:
                logger.error("pdffile must have .pdf extention and not %s", ext[-1])
                raise ValueError("pdffile_name must ends with .pdf extension, not %s" % ext[-1])
        else:
            logger.error("%s-File Not Found", htmlfile_name)
            raise FileNotFoundError("%s-File Not Found", htmlfile_name)
