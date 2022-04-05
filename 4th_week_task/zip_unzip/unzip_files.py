# importing required modules
from zipfile import ZipFile
import logging
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/unzip_file.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()
# specifying the zip file name
file_name = "Zip_Generated_files.zip"

# opening the zip file in READ mode
try:
    with ZipFile(file_name, 'r') as zip:
        # printing all the contents of the zip file
        print(zip)
        zip.printdir()

        # extracting all the files
        # print('Extracting all the files now...')
        logger.info("Extracting file all files ...")
        zip.extractall()
        logger.info("%s unzipped successfully",file_name)
        # print('Done!')
except(FileNotFoundError,OSError) as ex:
    logger.error("%s - %s", ex.__class__.__name__, ex)
