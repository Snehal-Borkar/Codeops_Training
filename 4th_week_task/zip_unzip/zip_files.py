# importing required modules
from zipfile import ZipFile
import os
import logging
import sys

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/zip_file.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    print(file_paths)
    return file_paths


def main():
    # path to folder which needs to be zipped
    directory = './Generated_files'

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
    logger.info("%s is filepaths", file_paths)
    if not file_paths:
        logger.info("%s is empty",file_paths)
        sys.exit(1)
    # printing the list of all files to be zipped
    else :

        print('Following files will be zipped:')
        for file_name in file_paths:
            print(file_name)
            logger.info("%s will be zipped",file_name)

        # writing files to a zipfile
        with ZipFile('Zip_Generated_files.zip', 'w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)

        print('All files zipped successfully!')


if __name__ == "__main__":
    main()
