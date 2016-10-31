from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
import pandas as pd
import happybase
import json
import struct
import sys
import numpy as np
import tensorflow as tf
import time



class HbaseManager:

    def session_create(self, db_name=None):
        try:
            """
            Hbase Loader Class
            creadted for the purpose of handling Spark Jobs
            """

            tfmsa_logger("Hbase Session Created")
            if db_name is None:
                conn = happybase.Connection(host=settings.HBASE_HOST, port=settings.HBASE_HOST_PORT)
            if db_name is not None:
                conn = happybase.Connection(host=settings.HBASE_HOST, port=settings.HBASE_HOST_PORT, table_prefix=db_name, table_prefix_separator=':')
            #print(conn.__class__)
            return conn
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def search_all_database(self):
        """
        search all databases
        :return: database list
        """
        try:
            conn = self.session_create()
            db_names = []
            t_tables = conn.tables()
            tables = list(map(lambda x : str(x,'utf-8'),t_tables))
            for tb in tables:
                print(tb)
                if (tb.find(":") > 0):
                    db_names.append(tb.split(":")[0])
            #Distict Dbname
            distict_db = set(db_names)
            print(list(distict_db))
            return list(distict_db)#list(map(lambda x: str(x, 'utf-8').split(':')[0],tables))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def create_database(self, db_name):
        """

        :param db_name: target database name
        :return: none
        """
        try:
            print("create hbase database" + db_name)
            raise Exception("Hbase can not make db")
            #conn = self.spark_session_create()
            #conn.table_prefix = db_name
            #conn.table_prefix_separator = ":"
            #print(db_name)
            #table = conn.create_table(db_name,{'data':dict(),})
            #return json.dumps(table)
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
            conn = self.session_create(db_name)
            #conn.table_prefix
            #conn.table_prefix_separator = ":"
            table = conn.tables()
            print(map(lambda x:str(x,'utf-8'), table))
            #results = list(map(lambda x:))
            return list(map(lambda x:str(x,'utf-8') ,table))
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
            conn = self.session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            # DBNAME probably needs
            make_prefix = data_frame + ":"  # python 3.5 change
            table = conn.table(make_prefix + table_name, use_prefix=False) # python 3.5 change

            key = 'columns'  # fix
            print("get columns info")
            column_dtype_key ='columns' #fix
            cf = 'data'
            print("get columns info before get table")
            column_dtype = table.row(column_dtype_key, columns=[cf])
            print(type(column_dtype))
            print(column_dtype)
            print("get columns info after get table")
            #column_dtype35 = dict(map(lambda x : str(x,'utf-8'),column_dtype.items()))#3.5 change
            #print(column_dtype35)
            #columns = {col.split(':')[1]: value for col, value in column_dtype.items()}
            columns = {str(col,'utf-8').split(':')[1]: str(value,'utf-8') for col, value in column_dtype.items()}
            print(columns)
            column_order_key = key + 'column_order'

            print("get columns_order_dict info before get table")
            column_order_dict = table.row(column_order_key, columns=[cf])
            print("get columns_order_dict info after get table")
            column_order = list()
            for i in range(len(column_order_dict)):
                column_order.append(column_order_dict[':'.join((cf, struct.pack('>q', i)))])
            print("column_ordder_dict")
            print(column_order)
            #row_start = key + 'rows' + struct.pack('>q', 0)
            #row_end = key + 'rows' + struct.pack('>q', sys.maxint)
            row_start = "1"
            row_end = str(sys.maxsize)
            #limit check
            #limit_cnt = 0
            rows = dict()
            if limit_cnt == 0:
                rows = table.scan(row_start=row_start, row_stop=row_end)
            elif limit_cnt > 0:
                rows = table.scan(row_start=row_start, row_stop=row_end, limit=limit_cnt)

            df = pd.DataFrame(columns=columns)

            rowcnt = 0 #read row count variable
            for row in rows:
                df_row = {str(key,'utf-8').split(':')[1]: str(value,'utf-8') for key, value in row[1].items()}
                df = df.append(df_row, ignore_index=True)
                rowcnt += 1
                #Print when 1000 rows count
                if rowcnt%1000 == 0:
                    print ("[" + data_frame + "] table_name :" + table_name + " readRows(" + str(rowcnt) + ")")
            for column, data_type in columns.items():
                df[column] = df[column].astype(np.dtype(data_type))
                print (" column :" + column + " data_type(" + str(data_type) + ")")
            if("None" != with_label):
                print("label exsist --> " + with_label)
                #Label auto check
                label_values = df[with_label].unique()
                label_first_value = sorted(label_values)[0]
                print("sorted label value : " + label_first_value)
                df['label'] = (
                    df[with_label].apply(lambda x: label_first_value in x)).astype(int) #16.10.25 auto check label values for 2 type values
            tfmsa_logger("End query data!")
            #print(df)
            print(df.to_string(index=False))
            return json.dumps(df.to_string(index=False))
            #return json.dumps(df)

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
            conn = self.session_create()
            nameSpace_tableName = db_name + ":" + table_name
            cf = {'data': dict(),}

            conn.create_table(nameSpace_tableName, cf)

            # DBNAME probably needs

            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_table(self, db_name, table_name):
        """
        hbase delete table
        :param db_name:target database name
        :param table_name:target table name
        :return:
        """
        try:
            tfmsa_logger("delete table !")
            conn = self.session_create()
            nameSpace_tableName = db_name + ":" + table_name
            print("Delete table" + nameSpace_tableName)

            conn.delete_table(nameSpace_tableName, True)

            # DBNAME probably needs

            return table_name

            #if (self.client.content("{0}{1}/{2}".format(self.root, db_name, table_name), strict=False) == None):
            #    raise Exception("request table : {0} not exist".format(table_name))

            #self.client.delete("{0}{1}/{2}".format(self.root, db_name, table_name), recursive=True)
            #return table_name
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
            print("((To_base )) ###start connection###")
            conn = self.session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            make_prefix = data_frame+":" # python 3.5 change

            table = conn.table(make_prefix + table_name,use_prefix=False) #python 3.5 chagne
            print("((To_base )) ###start batch   1-1###")
            column_dtype_key = 'columns'
            first_col_check_flag = table.scan(row_prefix=b'columns')
            print(len(list(first_col_check_flag)))
            #print(key, data)

            #column_dtype_key = key + 'columns'
            column_dtype_value = dict()
            #print("((To_base )) ###start batch###2###")
            for column in df.columns:
                column_dtype_value[':'.join((cf, column))] = df.dtypes[column].name

            # column_order_key = key + 'column_order'
            # column_order_value = dict()
            # for i, column_name in enumerate(df.columns.tolist()):
            #    order_key = struct.pack('>q', i)
            #    column_order_value[':'.join((cf, order_key))] = column_name
            print("((To_base )) ###start batch###3###")
            row_key_template = key + 'rows'
            rownum = 1
            #with table.batch(transaction=True,) as b:
            b = table.batch(transaction=True)
            #check fist row for exception dupulication of column type
            if 0 == len(list(first_col_check_flag)):
                b.put(column_dtype_key, column_dtype_value)
            print("((To_base )) ###start batch###")
            row_key = '1'
            to_hbase_results = dict()

            #commnet should  be delete
            for row in df.iterrows():
                # row_key = row_key_template + struct.pack('>q', row[0])
                #row_key = row_key_template + str(rownum)
                row_key = self.make_hbasekey() #+ str(rownum)
                row_value = dict()
                #Save first row key for select nextTime
                if rownum == 1:
                    to_hbase_results['firstRowKey'] = row_key
                for column, value in row[1].iteritems():
                    if not pd.isnull(value):
                        row_value[':'.join((cf, column))] = str(value)
                b.put(row_key, row_value)
                rownum += 1
                if rownum%100 == 0:
                    print("Insert Row count      " + str(rownum))
            b.send()
            to_hbase_results['lastRowKey'] = row_key
            to_hbase_results['insertedRows'] = rownum
            print("((To_base)) ###end batch###")
            conn.close()
            #send to  to json string
            return json.dumps(to_hbase_results)
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def make_hbasekey(self):
        """
        make_hbasekey (reverse timestamp key)
        :param net_id:
        :return: unique hbase key (reverse timestamp key)
        """
        #key = str(sys.maxsize - int(time.mktime(time.gmtime())))
        key = str(time.time())
        return key

    def save_csv_to_df(self, data_frame, table_name, csv_file):
        """
        create new table with inserted csv data
        :param net_id:
        :return: rownum
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
            rownum = self.to_hbase(df, data_frame, table_name, 'networkid')

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            tfmsa_logger("stop hbase context")
            return rownum #df.columns.values.tolist()


