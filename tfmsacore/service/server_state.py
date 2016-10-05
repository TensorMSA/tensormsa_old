from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger

class ServerStateChecker:
    def __init__(self):
        tfmsa_logger("initialize serverStateChecker!!")

    def check_servers(self):
        if(self.get_spark_state() == False):
            raise Exception ("Spark Server state not nomal")
        if (self.get_livy_state() == False):
            raise Exception("Spark Server state not nomal")
        if (self.get_hdfs_state() == False):
            raise Exception("Spark Server state not nomal")
        if (self.get_s3_state() == False):
            raise Exception("Spark Server state not nomal")

    def get_spark_state(self):
        """

        :return:
        """
        return True

    def get_livy_state(self):
        """

        :return:
        """
        return True


    def get_hdfs_state(self):
        """

        :return:
        """
        return True

    def get_s3_state(self):
        """

        :return:
        """
        return True