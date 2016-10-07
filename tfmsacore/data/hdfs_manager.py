#https://hdfscli.readthedocs.io/en/latest/quickstart.html#configuration
#setting : ~/.hdfscli.cfg

from hdfs import Config
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings

class HadoopManager:
    """
    HdfsManager : mainly manageing hdfs folders
    lv1 : image, raw rext, parquet types
    lv2 : category
    lv3 : sub category
    lv4 : real files
    """
    def __init__(self):
        """
        create non exist essential directories
        """
        self.client = Config().get_client()
        if(self.client.content("{0}/".format(settings.HDFS_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_DF_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_DF_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_CONF_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_CONF_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_MODEL_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_MODEL_ROOT), permission=777)

        self.root = "{0}/".format(settings.HDFS_DF_ROOT)

    def search_all_database(self):
        """
        search all databases
        :return: database list
        """
        try:
            databases = self.client.list("{0}".format(self.root))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)
        return databases

    def create_database(self, db_name):
        """

        :param db_name: target database name
        :return: none
        """
        try:
            if (self.client.content("{0}{1}".format(self.root,db_name), strict=False) != None):
                raise Exception("Data Base {0} Already Exist!!".format(db_name))

            self.client.makedirs("{0}{1}".format(self.root,db_name), permission=777)
            return db_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_database(self, db_name):
        """

        :param db_name: target database name
        :return: none
        """
        try:
            self.client.delete("{0}{1}".format(self.root,db_name), recursive=True)
        except Exception as e:
            raise Exception(e)

    def search_database(self, db_name):
        """
        return all tables names
        :param db_name: target database name
        :return: table list
        """
        try:
            return self.client.list("{0}{1}".format(self.root, db_name), status=False)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def rename_database(self, db_name, change_name):
        """
        rename database
        :param db_name: as-is database name
        :param change_name: tb-be data base name
        :return:
        """
        try:
            self.client.rename("{0}{1}".format(self.root, db_name), "{0}{1}".format(self.root, change_name))
            return change_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def create_table(self, db_name, table_name):
        """
        create table
        :param db_name:target database name
        :param table_name:target table name
        :return:
        """
        try:
            if (self.client.content("{0}{1}/{2}".format(self.root, db_name, table_name), strict=False) != None):
                tfmsa_logger("Warning DataBase not exist, auto create : {0}".format(db_name))
                self.create_database(db_name)

            self.client.makedirs("{0}{1}/{2}".format(self.root, db_name, table_name) , permission=777)
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_table(self, db_name, table_name):
        """
        delete table
        :param db_name:target database name
        :param table_name:target table name
        :return:
        """
        try:
            if (self.client.content("{0}{1}/{2}".format(self.root, db_name, table_name), strict=False) == None):
                raise Exception("request table : {0} not exist".format(table_name))

            self.client.delete("{0}{1}/{2}".format(self.root, db_name, table_name), recursive=True)
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def rename_table(self, db_name, table_name, rename_table):
        """
        rename table
        :param db_name:target database name
        :param table_name:target table name
        :param rename_table:to-be table name
        :return:
        """
        try:
            self.client.rename("{0}{1}/{2}".format(self.root, db_name, table_name), \
                               "{0}{1}/{2}".format(self.root, db_name, rename_table))
            return rename_table
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def hdfs_get(self, root, nn_id):
        """
        manage configration data
        :param category: business category
        :param subcate: business subcategory
        :param nn_id: nerual network id
        :return:
        """
        try:
            return self.client.read("/{0}/{1}".format(root, nn_id))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def hdfs_chk(self, root, nn_id):
        """
        check if nn_id exist
        :param category: business category
        :param subcate: business subcategory
        :param nn_id: nerual network id
        :return:
        """
        try:
            if (self.client.content("/{0}/{1}".format(root, nn_id), strict=False) == None):
                return True
            else :
                return False

        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def hdfs_put(self, root, nn_id, records):
        """
        manage configration data
        :param category: business category
        :param subcate: business subcategory
        :param nn_id: nerual network id
        :return:
        """
        try:
            self.client.write("/{0}/{1}".format(root, nn_id), data=records, encoding='utf-8')
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def hdfs_del(self, root, nn_id):
        """
        manage configration data
        :param category: business category
        :param subcate: business subcategory
        :param nn_id: nerual network id
        :return:
        """
        try:
            self.client.delete("/{0}/{1}".format(root, nn_id), recursive=False)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)
