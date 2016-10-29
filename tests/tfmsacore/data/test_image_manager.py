import unittest
from tfmsacore.data import ImageManager
from pyspark.context import SparkContext
from tfmsacore.utils.logger import tfmsa_logger
from django.core.files.uploadedfile import TemporaryUploadedFile

class TestImageManager(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsacore/data/ --enable-coverage
    ./manage.py jenkins ./tests/tfmsacore/data/
    """

    def test_search_all_database(self):
        """
        test search all database works correctly
        :return:
        """
        self.assertIsInstance(ImageManager().search_all_database(), (list))
        tfmsa_logger("==========PASS==========")

    def test_create_database(self):
        """
        test create_database works correctly
        :return:
        """
        base_list = ImageManager().search_all_database()
        if "test" in base_list:
            self.assertEqual(ImageManager().delete_database("test"), "test")
        self.assertEqual(ImageManager().create_database("test"), "test")

        load_base = ImageManager().search_all_database()
        if "test" not in load_base:
            raise Exception ("creation fail ")

        self.assertEqual(ImageManager().delete_database("test"), "test")

        load_base = ImageManager().search_all_database()
        if "test" in load_base:
            raise Exception ("deletion fail ")

            tfmsa_logger("==========PASS==========")

    def test_create_table(self):
        """
        test test_create_table works correctly
        :return:
        """
        base_list = ImageManager().search_all_database()
        if "test" not in base_list:
            self.assertEqual(ImageManager().create_database("test"), "test")

        table_list = ImageManager().search_database("test")
        if "test_table" in table_list:
            self.assertEqual(ImageManager().delete_table("test", "test_table"), "test_table")
        self.assertEqual(ImageManager().create_table("test", "test_table"), "test_table")

        load_table = ImageManager().search_database("test")
        if "test_table" not in load_table:
            raise Exception ("creation fail ")

        self.assertEqual(ImageManager().delete_table("test", "test_table"), "test_table")


        load_table = ImageManager().search_database("test")
        if "test_table" in load_table:
            raise Exception ("deletion fail ")

        ImageManager().delete_database("test")

        tfmsa_logger("==========PASS==========")

    def test_create_label(self):
        """
        test test_create_label works correctly
        :return:
        """
        ImageManager().create_database("test")
        ImageManager().create_table("test", "test_table")
        ImageManager().create_label("test", "test_table", "1")
        label_list = ImageManager().search_table("test", "test_table")

        if "1" not in label_list:
            raise Exception ("Label creation failed")
        else :
            ImageManager().delete_label("test", "test_table", "1")

        label_list = ImageManager().search_table("test", "test_table")

        if "1" in label_list:
            raise Exception ("Label deletion failed")

        ImageManager().delete_database("test")

        tfmsa_logger("==========PASS==========")


    def test_put_data(self):
        """

        :return:
        """
        base_list = ImageManager().search_all_database()
        if "test" not in base_list:
            self.assertEqual(ImageManager().create_database("test"), "test")

        load_table = ImageManager().search_database("test")
        if "test_table" not in load_table:
            ImageManager().create_table("test", "test_table")

        label_list = ImageManager().search_table("test", "test_table")
        if "1" not in label_list:
            ImageManager().create_label("test", "test_table", "1")

        temp_file = TemporaryUploadedFile("img_test_data", "UTF-8", 66666, "xxxxxxxxxxxxxxxxxx")
        self.assertEqual(ImageManager().put_data("test", "test_table", "1", temp_file, "img_test_data"),"img_test_data")

        ImageManager().load_data("test", "test_table", "1")
        tfmsa_logger("==========PASS==========")
