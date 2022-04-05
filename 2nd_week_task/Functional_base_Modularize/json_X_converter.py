
import pandas
import logging
from json2xml import json2xml
from json2xml.utils import readfromstring
import json
import pdfkit


logger = logging.getLogger( )


def df_csv(df, csv_file_name):
    """
    Generates csv file from pandas Dataframe to provided file name.

    Parameters:
        df (pandas.Dataframe): Dataframe provided by user from API fetched json
        csv_file_name (.csv): File name to store csv data
        index (bool): should csv file includes Dataframe index (default False) .
        encoding (str): encoding to which user need to convert (default 'utf-8-sig')

    Returns:
        None

    """

    if isinstance(df, pandas.DataFrame):
        if not df.empty:
            if isinstance(csv_file_name, str):
                ext = csv_file_name.split(".")
                if ext[-1] == "csv":
                    try:
                        logger.info("Generating CSV...")
                        df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
                        logger.info("CSV file generated successfully")
                    except PermissionError as ex:
                        logger.error("%s : %s , cannot write in already opened file", ex.__class__.__name__, ex)
                        raise PermissionError("%s :  cannot write in already opened file" % ex)
                else:
                    logger.error("csv_file must have .csv extention and not %s", ext[-1])
                    raise ValueError("csv_file_name must ends with .csv extension, not %s" % ext[-1])
            else:
                logger.error("Type of csv_file_name must be of <class: str>, not %s", type(csv_file_name))
                raise TypeError("Type of csv_file_name must be of <class: str>. not %s" % type(csv_file_name))
        else:
            logger.error("Dataframe pass must not be empty")
            raise ValueError("Dataframe pass must not be empty")

    else:
        logger.error("df is not instance of pandas.DataFrame, not %s",  type(df))
        raise TypeError("df must be an instance of pandas.DataFrame, not %s" % type(df))


def df_html(df, htmlfile_name, render_images=None):
    """
    Converts pandas dataframe to table html file.

    Parameters:
    df (pandas.Dataframe): pandas dataframe.
    htmlfile_name (str): html file to render as web page
    render_images (list): list of dataframe column indices name contains image url (default: None)

    Returns:
    None

    """
    def path_to_image_html(path):
        """Values from dataframe are edited or changes format."""

        return '<img src="' + path + '" width="60" >'

    if render_images is not None:
        value = path_to_image_html
        formatter_dict = {}
        for key in render_images:
            formatter_dict.update({key: value})
    else:
        formatter_dict = None

    if isinstance(df, pandas.DataFrame):
        if not df.empty:
            if isinstance(htmlfile_name, str):
                ext = htmlfile_name.split(".")
                if ext[-1] == "html":
                    try:
                        logger.info("Converting to HTML.")
                        df.to_html(htmlfile_name, escape=False, index=False, encoding="utf-8-sig",
                                   formatters=formatter_dict)
                        logger.info("HTML file generated Successfully.")
                    except (IOError, OSError) as ex:
                        logger.error("%s-%s", ex.__class__.__name__, ex)
                        raise IOError("%s-%s", ex.__class__.__name__, ex)
                else:
                    logger.error("htmlfile must have .html extention and not %s", ext[-1])
                    raise ValueError("htmlfile_name must ends with .html extension, not %s" % ext[-1])
            else:
                logger.error("Type of htmlfile_name must be of <class: str>, not %s", type(htmlfile_name))
                raise TypeError("Type of htmlfile_name must be of <class: str>. not %s" % type(htmlfile_name))
        else:
            logger.error("Dataframe pass must not be empty")
            raise ValueError("Dataframe pass must not be empty")
    else:
        logger.error("df is not instance of pandas.DataFrame, not %s", type(df))
        raise TypeError("df must be an instance of pandas.DataFrame, not %s" % type(df))


def df_pdf(htmlfile_name, pdf_file_name, options=None, wkhtmltopdf_path=None):
    """ Reads html file and converts it to pdf file. """

    import os.path

    file_exists = os.path.exists(htmlfile_name)
    if file_exists:
        if isinstance(pdf_file_name, str):
            ext = pdf_file_name.split(".")
            if ext[-1] == "pdf":
                try:
                    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

                    logger.info("Reading HTML file")
                    # converts html page to pdf document
                    pdfkit.from_file(htmlfile_name, pdf_file_name, options=options, configuration=config)
                    logger.info("pdf file Generted Successfully")

                except (IOError, OSError) as ex:
                    logger.error("%s - %s", ex.__class__.__name__, ex)
                    raise IOError("Error occured: %s:" % ex)
            else:
                logger.error("pdffile must have .pdf extention and not %s", ext[-1])
                raise ValueError("pdffile_name must ends with .pdf extension, not %s" % ext[-1])
        else:
            logger.error("Type of pdf_file_name must be of <class: str>, not %s", type(pdf_file_name))
            raise TypeError("Type of pdf_file_name must be of <class: str>. not %s" % type(pdf_file_name))
    else:
        logger.error("%s-File Not Found", htmlfile_name)
        raise FileNotFoundError("%s-File Not Found", htmlfile_name)


def df_xml(df, xmlfile_name):
    """
    Converts pandas dataframe to xml file.

    Parameters:
    unflat_df (pandas.Dataframe): pandas dataframe.

    Returns:
    json_xml.xml file

    """

    if not df.empty:
        un_flat_dict = df.to_dict(orient='records')
    else:
        logger.error("Dataframe pass must not be empty")
        raise ValueError("Dataframe pass must not be empty")

    json_str = json.dumps(un_flat_dict)

    data = readfromstring(json_str)

    logger.info("Converting to xml...")
    xml_data = json2xml.Json2xml(data).to_xml()  # get the xml from a json string

    if type(xmlfile_name) != str:
        raise TypeError("Type of xmlfile_name must be of <class: str>. not %s" % type(xmlfile_name))
    ext = xmlfile_name.split(".")
    if ext[-1] != "xml":
        logger.error("xmlfile must have .xml extention and not %s", ext[-1])
        raise ValueError("xmlfile_name must ends with .xml extension, not %s" % ext[-1])

    try:
        logger.info("Writing to xml...")
        with open(xmlfile_name, "w") as xml_file:
            xml_file.write(xml_data)
        logger.info("xml file Generated Successfully")
    except (IOError, OSError) as ex:
        logger.error("%s - %s", ex.__class__.__name__, ex)
        raise IOError("%s - %s" % ex.__class__.__name__ % ex)




