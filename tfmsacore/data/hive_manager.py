from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
import pandas as pd
import happybase
import json
import struct
import sys
import numpy as np
import tensorflow as tf


class HiveManager:
    def __init__(self):
        print("Hive file manager")


    def spark_session_create(self):
        """
        Hbase Loader Class
        creadted for the purpose of handling Spark Jobs
        """

        tfmsa_logger("Hbase Session Created")
        conn = happybase.Connection(host=settings.HBASE_HOST, port=settings.HBASE_HOST_PORT)
        #print(conn.__class__)
        return conn

    def search_all_database(self):
        """
        search all databases
        :return: database list
        """
        try:
            conn = self.spark_session_create()
            db_names = []
            tables = conn.tables()
            for tb in tables:
                print(tb)
                if (tb.find(":") > 0):
                    db_names.append(tb.split(":")[0])
            distict_db = set(db_names)
            return json.dumps(distict_db)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def search_database(self, db_name):
        """
        return all tables names
        :param db_name: target database name
        :return: table list
        """
        try:
            conn = self.spark_session_create()
            conn.table_prefix = db_name
            conn.table_prefix_separator = ":"
            print(db_name)
            table = conn.tables()
            return json.dumps(table)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def query_data(self, data_frame, table_name, query_str, limit_cnt=0, with_label = "None"):
        """
        get query data from spark
        :param data_fream(database), table_name,
        :param limit cnt
        :param label columns if you need
        :return: pandas dataframe object
        """
        try:
            tfmsa_logger("start query data !")
            conn = self.spark_session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            # DBNAME probably needs

            table = conn.table(table_name)

            key = 'networkid'  # shoud be chaned when producing.

            column_dtype_key = key + 'columns'
            cf = 'data'
            column_dtype = table.row(column_dtype_key, columns=[cf])
            columns = {col.split(':')[1]: value for col, value in column_dtype.items()}

            column_order_key = key + 'column_order'
            column_order_dict = table.row(column_order_key, columns=[cf])
            column_order = list()
            for i in range(len(column_order_dict)):
                column_order.append(column_order_dict[':'.join((cf, struct.pack('>q', i)))])

            row_start = key + 'rows' + struct.pack('>q', 0)
            row_end = key + 'rows' + struct.pack('>q', sys.maxint)

            #limit check
            rows = dict()
            if limit_cnt == 0:
                rows = table.scan(row_start=row_start, row_stop=row_end)
            elif limit_cnt > 0:
                rows = table.scan(row_start=row_start, row_stop=row_end, limit=limit_cnt)

            df = pd.DataFrame(columns=columns)

            rowcnt = 0 #read row count variable
            for row in rows:
                df_row = {key.split(':')[1]: value for key, value in row[1].items()}
                df = df.append(df_row, ignore_index=True)
                rowcnt += 1
                #Print when 1000 rows count
                if rowcnt%1000 == 0:
                    print ("[" + data_frame + "] table_name :" + table_name + " readRows(" + str(rowcnt) + ")")
            for column, data_type in columns.items():
                df[column] = df[column].astype(np.dtype(data_type))
            if("None" != with_label):
                print("no label")
                #label_name = label_with
                df['label'] = (
                    df[with_label].apply(lambda x: ">50K" in x)).astype(int)

            tfmsa_logger("End query data!")
            return df

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        #finally:
        #    df.unpersist()
        #    self.sc.stop()

    def create_table(self, db_name, table_name):
        """
        create table
        :param db_name:target database name on Hbase
        :param table_name:target table name on Hbase
        :return: tableName
        """
        try:
            tfmsa_logger("start query data !")
            conn = self.spark_session_create()
            nameSpace_tableName = db_name + ":" + table_name
            cf = {'data': dict(),}

            conn.create_table(nameSpace_tableName, cf)

            # DBNAME probably needs

            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def to_hbase(self, df, data_frame, table_name, key, cf='data'):
        """Write a pandas DataFrame object to HBase table.
        :param df: pandas DataFrame object that has to be persisted
        :param data_frame : database
        :param table_name: HBase table name to which the DataFrame should be written
        :param key: network id is key, but now is hardcode(networdid) should change later
        :param cf: Column Family name
        :type cf: str
        """
        try:
            conn = self.spark_session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            conn.timeout = None

            table = conn.table(table_name)

            column_dtype_key = key + 'columns'
            column_dtype_value = dict()
            for column in df.columns:
                column_dtype_value[':'.join((cf, column))] = df.dtypes[column].name

            # column_order_key = key + 'column_order'
            # column_order_value = dict()
            # for i, column_name in enumerate(df.columns.tolist()):
            #    order_key = struct.pack('>q', i)
            #    column_order_value[':'.join((cf, order_key))] = column_name

            row_key_template = key + 'rows'
            rownum = 1
            #with table.batch(transaction=True,) as b:
            b = table.batch(transaction=True)
            b.put(column_dtype_key, column_dtype_value)
            print("((To_base )) ###start batch###")
            #print(df.count())

            for row in df.iterrows():
                # row_key = row_key_template + struct.pack('>q', row[0])
                row_key = row_key_template + str(rownum)
                row_value = dict()
                for column, value in row[1].iteritems():
                    if not pd.isnull(value):
                        row_value[':'.join((cf, column))] = str(value)
                b.put(row_key, row_value)
                rownum += 1
                #print(row[1])
                print("Insert Row count      " + str(rownum))
            b.send()
            print("((To_base)) ###start batch###")
            conn.close()
        except Exception as e:
            tfmsa_logger(e)
            #raise Exception(e)


    def save_csv_to_df(self, data_frame, table_name, csv_file):
        """
        create new table with inserted csv data
        :param net_id:
        :return:
        """
        try:
            print("hbase_save_csv_to_df")
            print(settings.FILE_ROOT)
            print(data_frame)
            print(table_name)
            print(csv_file)

            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            print(file_path)
            df = pd.read_csv(
                 tf.gfile.Open(file_path),
                 # names=COLUMNS,
                 skipinitialspace=True,
                 engine="python")
            #when data insert to hbase, It occurs error about time out. I just pass the error
            self.to_hbase(df, data_frame, table_name, 'networkid')

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            tfmsa_logger("stop hbase context")
            return df.columns.values.tolist()


