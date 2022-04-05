import requests
import unittest
import logging
import filecmp
import os.path
import os
from json2Xconverter.x_converter import XConverter

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/file_converter_unit.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()


class TestCSVFileGen(unittest.TestCase):
    """ Tests unittest for the file generated from json2Xconverter module successfull """

    def test_api_gives_data_successfull(self):
        """tests the json  response from api is not empty"""
        url = "https://fakestoreapi.com/products/"
        response = requests.get(url)
        data_dict = response.json()
        self.assertNotEqual(len(data_dict), 0)

    def setUp(self):
        """generate dataframe before generating file"""
        import pandas as pd
        from json2Xconverter.api_call_flat import ApiCall, Flatten

        dfs = []
        for i_d in range(1, 20):
            url = "https://fakestoreapi.com/products/" + str(i_d)
            data = ApiCall.api_call(url)
            flatten_df = Flatten.flatten_json(data)
            dfs.append(flatten_df)
        df_data = pd.concat(dfs, axis=1)

        self.trans_dataframe = df_data.transpose()

    def test_csv_gen_successfull(self):
        """tests if csv generation from dataframe is successfull"""
        file_path_test_generated = (os.path.dirname(__file__)) + "./Test_generated/fakestore.csv"
        file_path2_truthfolder = (os.path.dirname(__file__)) + "./TruthFolder/fakestore.csv"

        XConverter(self.trans_dataframe, file_path_test_generated).df_csv()
        self.assertTrue(filecmp.cmp(file_path_test_generated, file_path2_truthfolder))

    def test_xml_gen_successfull(self):
        """tests if xml generation from dataframe is successfull"""
        file_path_test_generated = (os.path.dirname(__file__)) + "./Test_generated/fakestore.xml"
        file_path2_truthfolder = (os.path.dirname(__file__)) + "./TruthFolder/fakestore.xml"
        XConverter(self.trans_dataframe, file_path_test_generated).df_xml()
        self.assertTrue(filecmp.cmp(file_path_test_generated, file_path2_truthfolder, shallow=False))

    def test_html_gen_successfull(self):
        """tests if html generation from dataframe is successfull"""
        file_path_test_generated = (os.path.dirname(__file__)) + "./Test_generated/fakestore.html"
        file_path2_truthfolder = (os.path.dirname(__file__)) + "./TruthFolder/fakestore.html"
        XConverter(self.trans_dataframe, file_path_test_generated).df_html(['image'])
        self.assertTrue(filecmp.cmp(file_path_test_generated, file_path2_truthfolder, shallow=False))

    def test_pdf_gen_successfull(self):
        """tests if pdf generation from dataframe is successfull"""
        options = {
            'page-height': '500',
            'page-width': '500',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
        }
        path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        file_path_test_generated = (os.path.dirname(__file__)) + "./Test_generated/fakestore.pdf"
        file_path_test_generated_html = (os.path.dirname(__file__)) + "./Test_generated/fakestore.html"
        XConverter(self.trans_dataframe, file_path_test_generated).df_pdf(htmlfile_name=file_path_test_generated_html,
                                                                          options=options, wkhtmltopdf_path=path)

        self.assertIsNotNone(os.path.exists("./Test_generated/fakestore.pdf"))

        with open(file_path_test_generated, 'rb') as file_tested:
            file_tested = file_tested.read()
        self.assertIsNotNone(file_tested)


if __name__ == '__main__':
    unittest.main()
