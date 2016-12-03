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
from TensorMSA import const


class HbaseManager:

    def session_create(self, db_name=None):
        try:
            """
            Hbase Loader Class
            creadted for the purpose of handling Spark Jobs
            """

            tfmsa_logger("Hbase Session Created")
            if db_name is None:
                conn = happybase.Connection(host=settings.HBASE_HOST, port=settings.HBASE_HOST_PORT, )
            if db_name is not None:
                conn = happybase.Connection(host=settings.HBASE_HOST, port=settings.HBASE_HOST_PORT, table_prefix=db_name, table_prefix_separator=':')
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
                if (tb.find(":") > 0):
                    db_names.append(tb.split(":")[0])
            #Distict Dbname
            distict_db = set(db_names)
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
            table = conn.tables()
            return list(map(lambda x:str(x,'utf-8') ,table))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def __get_hbase_data(self, data_frame, table_name, use_df, row_start = '1', limit_cnt=10):
        try :
            tfmsa_logger("[1] Create Hbase Session")
            conn = self.session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"

            # DBNAME probably needs
            make_prefix = data_frame + ":"
            table = conn.table(make_prefix + table_name, use_prefix=False)
            column_dtype = table.row('columns', columns=['data'])
            columns = {str(col, 'utf-8').split(':')[1]: str(value, 'utf-8') for col, value in column_dtype.items()}

            tfmsa_logger("[2] Hbase Scan Table")
            rows = dict()
            if(isinstance(row_start, (str))):
                row_start = row_start
            elif(isinstance(row_start, (bytes))):
                row_start = str(row_start, 'utf-8')
            else:
                row_start = str(row_start)

            if (use_df == True) :
                rows = table.scan(row_start=row_start, row_stop=str(sys.maxsize), limit=limit_cnt)
            else :
                rows = table.scan(row_start=row_start, row_stop=str(sys.maxsize), limit=15)

            return rows, columns
        except Exception as e:
            tfmsa_logger(e)


    def query_data(self, data_frame, table_name, query_str, use_df= None, limit_cnt=0, with_label = "None", start_pnt='1'):
        """
        get query data from spark
        :param data_fream(database), table_name,
        :param limit cnt
        :param label columns if you need
        :return: pandas dataframe object
        """
        try:
            last_key = ""
            rows, columns = self.__get_hbase_data(data_frame, table_name, use_df, start_pnt, limit_cnt)

            tfmsa_logger("[3] Convert to DataFrame")
            rowcnt = 0
            df = pd.DataFrame(columns=columns)
            for row in rows:
                df_row = {str(key,'utf-8').split(':')[1]: bytes.decode(value) for key, value in row[1].items()}
                last_key = row[0]
                df = df.append(df_row, ignore_index=True)
                rowcnt += 1

                if rowcnt%100 == 0:
                    tfmsa_logger ("[" + data_frame + "] table_name :" + table_name + " readRows(" + str(rowcnt) + ")")

            tfmsa_logger("[4] Sort & Type Convert DataFrame")
            for column, data_type in sorted(columns.items()): # can i sorted??? 11.11.21
                try:
                    column_name = str(column)
                    if "int" in data_type:
                        df[column_name] = df[column_name].astype("float").astype(np.dtype(data_type))
                    elif "float" in data_type:
                        df[column_name] = df[column_name].astype(np.dtype(data_type))
                    else:
                        df[column_name] = df[column_name].astype("str")
                except Exception as ex:
                    tfmsa_logger(ex)

            tfmsa_logger("[5] Set Label Data")
            if("None" != with_label):
                df['label'] = df[with_label]

            if use_df is None:
                tfmsa_logger("[6] Return Data to View")
                resultList = df.values.tolist()
                resultList.insert(0,df.columns.values.tolist())
                result = json.loads(json.dumps(resultList))
                return result
            else:
                tfmsa_logger("[6] Return Data to Train Neural Network")
                result = df
                return result, last_key

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)


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
            test_nameSpace_tableName = "test_schema_" + db_name + ":" + table_name
            cf = {'data': dict(),}

            conn.create_table(nameSpace_tableName, cf)
            conn.create_table(test_nameSpace_tableName, cf)

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
            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            df = pd.read_csv(
                 tf.gfile.Open(file_path),
                 skipinitialspace=True,
                 engine="python")
            train_set = df.sample(frac= const.TRAIN_DATA_PORTION, random_state=200)
            test_set = df.drop(train_set.index)
            rownum = self.to_hbase(train_set, data_frame, table_name, 'networkid')
            rownum = self.to_hbase(test_set, 'test_schema_' + data_frame, table_name, 'networkid')
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            tfmsa_logger("stop hbase context")
            return rownum #df.columns.values.tolist()


