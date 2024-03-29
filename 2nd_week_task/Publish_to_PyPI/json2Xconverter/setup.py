from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Convert Api responst to CSV, XML, PDF or HTML file'
LONG_DESCRIPTION = 'A package that allows to call Api and convert it to CSV, XML, PDF or HTML file '

# Setting up
setup(
    name="json2Xconverter",
    version=VERSION,
    author="Snehal Borkar",
    author_email="borkarsnehal60@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas','json2xml','pdfkit','flatten_json','requests','json2html'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
