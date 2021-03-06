import json, requests, textwrap, time, random, os
from django.conf import settings
#from tfmsacore.data.hdfs_manager import HadoopManager

class JsonObject:
    """
    json object hooker class
    """
    def __init__(self, d):
        self.__dict__ = d

    def __getitem__(self, item):
        return self.__dict__[item]


class LivyDfClientManager:
    def __init__(self):
        self.max_sess_num = int(settings.LIVY_SESS)
        self.headers = {'Content-Type': 'application/json'}
        self.alive_sess_obj = None
        self.alive_sess_cnt = None
        self.alive_sess_list = []
        self.alive_sess_state = []
        self.avail_sess_list = []

    def create_session(self):
        """
        create session is required before any actions
        :return:
        """
        self.check_alive_sessions()
        if(self.max_sess_num < self.alive_sess_cnt):
            print("exceed max session number")
            return False

        data = {'kind': 'pyspark',
                "name": "tensormsa",
                "executorCores": int(settings.SPARK_WORKER_CORE),
                "executorMemory": settings.SPARK_WORKER_MEMORY,
                "driverCores": int(settings.SPARK_CORE),
                "driverMemory": settings.SPARK_MEMORY}
        r = requests.post("http://" + settings.LIVY_HOST + "/sessions", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(r.json()['id']), None)
        return result

    def check_alive_sessions(self):
        """
        check alive sessions info
        :return:
        """
        self.alive_sess_list[:] = []
        self.alive_sess_cnt = 0
        self.alive_sess_obj = None
        resp = requests.get("http://" + settings.LIVY_HOST + "/sessions/" , headers=self.headers)
        self.alive_sess_obj = json.loads(resp.content,  object_hook=JsonObject)
        self.alive_sess_cnt = len(self.alive_sess_obj.sessions)

        if(self.alive_sess_cnt > 0):
            for i in range(0 , self.alive_sess_cnt):
                self.alive_sess_list.append(self.alive_sess_obj.sessions[i].id)

    def get_available_sess_id(self):
        """
        get random one available (state is idle) session
        :return:
        """
        self.avail_sess_list[:] = []

        resp = requests.get("http://" + settings.LIVY_HOST + "/sessions/" , headers=self.headers)
        self.alive_sess_obj = json.loads(resp.content,  object_hook=JsonObject)
        self.alive_sess_cnt = len(self.alive_sess_obj.sessions)

        if(self.alive_sess_cnt > 0):
            for i in range(0 , self.alive_sess_cnt):
                if(self.alive_sess_obj.sessions[i].state == 'idle'):
                    self.avail_sess_list.append(self.alive_sess_obj.sessions[i].id)

    def delete_all_sessions(self):
        """
        delete all sessions
        :return: None
        """
        self.check_alive_sessions()
        for sess_id in self.alive_sess_list:
            print(sess_id)
            r = requests.delete("http://" + settings.LIVY_HOST + "/sessions/" + str(sess_id), headers=self.headers)
            print(r.json())

    def print_all(self):
        """
        print all conifg vales of Class
        :return: None
        """
        print("host : {0}".format(self.host))
        print("headers : {0}".format(self.headers))
        print("alive_sess_obj : {0}".format(self.alive_sess_obj))
        print("alive_sess_cnt : {0}".format(self.alive_sess_cnt))
        print("alive_sess_list : {0}".format(self.alive_sess_list))


    def create_table(self, data_frame, table_name, json_data):
        """
        create table with json data
        :param table_name: name of table want to create
        :param json_data: json form schema data
        :return: success or failure
        """
        self.get_available_sess_id()
        data = {
            'code': ''.join(['from pyspark.sql import SQLContext, DataFrameWriter, DataFrame\n',
                             'sqlContext = SQLContext(sc)\n',
                             'df_writer = sqlContext.createDataFrame(', str(json_data)  ,').write\n',
                             'df_writer.parquet("hdfs://', settings.HDFS_HOST ,"/", settings.HDFS_DF_ROOT, "/", data_frame,
                             "/", table_name ,'", mode="append", partitionBy=None)'
                             ])
        }
        resp = requests.post("http://" + settings.LIVY_HOST + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        temp_resp = json.loads(resp.content, object_hook=JsonObject)
        result = self.get_response(str(min(self.avail_sess_list)), temp_resp.id)
        return result

    def append_data(self, data_frame, table_name, json_data):
        """
        append data on exist table
        :param table_name: name of table want to add data
        :param json_data: json form schema data
        :return: success or failure
        """

        self.get_available_sess_id()
        data = {
            'code': ''.join(['from pyspark.sql import SQLContext, DataFrameWriter, DataFrame\n',
                             'sqlContext = SQLContext(sc)\n',
                             'df = sqlContext.read.load("hdfs://', settings.HDFS_HOST ,"/", settings.HDFS_DF_ROOT
                                , "/", data_frame,"/", table_name, '" , "parquet" )\n',
                             'df_writer = sqlContext.createDataFrame(', str(json_data)  ,')\n',
                             'df.unionAll(df_writer)\n',
                             'df.write.parquet("hdfs://', settings.HDFS_HOST ,"/", settings.HDFS_DF_ROOT, "/", table_name,
                             '", mode="append", partitionBy=None)\n'
                             ])
        }
        resp = requests.post("http://" + settings.LIVY_HOST + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        temp_resp = json.loads(resp.content, object_hook=JsonObject)
        result = self.get_response(str(min(self.avail_sess_list)), temp_resp.id)


    def get_response(self, session_id, statements_id):
        """
        wait for Livy running and get return when finished
        :param session_id:session id used on request
        :param statements_id: statements id used on request
        :return: response result from livy
        """
        if(statements_id == None):
            resp = requests.get("http://" + settings.LIVY_HOST + "/sessions/" + str(session_id)  \
                                , headers=self.headers)
        else:
            resp = requests.get("http://" + settings.LIVY_HOST + "/sessions/" + str(session_id) +  \
                                "/statements/" + str(statements_id), \
                                headers=self.headers)

        response_obj = json.loads(resp.content, object_hook=JsonObject)

        if(response_obj.state == 'running'):
            time.sleep(2)
            return self.get_response(session_id, statements_id)
        elif(response_obj.state == 'starting'):
            time.sleep(2)
            return self.get_response(session_id, statements_id)
        else:
            print("Response : {0}".format(resp.json()))
            return resp.json()



    def query_data(self, data_frame, table_name, query_str):
        """
        get query data from spark
        :param table_name: name of table you want to get data
        :param query_str: sql strings
        :return: query result as json Object
        """
        self.get_available_sess_id()

        data = {
            'code': ''.join(['from pyspark.sql import SQLContext\n',
                             'import json\n',
                             'sqlContext = SQLContext(sc)\n',
                             'rows = sqlContext.read.load("hdfs://', settings.HDFS_HOST ,"/", settings.HDFS_DF_ROOT,
                             "/", data_frame, "/" ,table_name , '" , "parquet" )\n',
                             'tbl = rows.registerTempTable("' , table_name , '")\n',
                             'result = sqlContext.sql("' , str(query_str) ,
                             '").toJSON(False).map(lambda x : x).collect()\n',
                             'result'
                             ])
        }

        resp = requests.post("http://" + settings.LIVY_HOST + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(min(self.avail_sess_list)), \
                                          json.loads(resp.content, object_hook=JsonObject).id)

        return result["output"]["data"]["text/plain"].replace("'", "")


    def query_stucture(self, data_frame, table_name):
        """
        return parqueet data strucure stored on spark
        :param table_name: table name you request
        :return: JSON
        """
        self.get_available_sess_id()

        data = {
            'code': ''.join(['from pyspark.sql import SQLContext\n',
                             'sqlContext = SQLContext(sc)\n',
                             'rows = sqlContext.read.load("hdfs://', settings.HDFS_HOST ,"/", settings.HDFS_DF_ROOT,
                             "/", data_frame, "/" , table_name, '" , "parquet" ).schema.json()\n',
                             'rows'
                             ])
        }

        resp = requests.post("http://" + settings.LIVY_HOST + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(min(self.avail_sess_list)), \
                                          json.loads(resp.content, object_hook=JsonObject).id)
        return result["output"]["data"]["text/plain"].replace("'", "")

    def get_distinct_column(self, data_frame, table_name, columns):
        """
        get distinct list of selected table's column
        :return:
        """
        self.get_available_sess_id()
        query_str = "select * from " + table_name

        data = {
            'code': ''.join(['from pyspark.sql import SQLContext\n',
                             'import json, unicodedata\n',
                             'sqlContext = SQLContext(sc)\n',
                             'rows = sqlContext.read.load("hdfs://', settings.HDFS_HOST , "/" , settings.HDFS_DF_ROOT,
                             "/" , data_frame, "/" ,table_name , '" , "parquet" )\n',
                             'tbl = rows.registerTempTable("' , table_name , '")\n',
                             'result = sqlContext.sql("' , str(query_str) ,
                             '")\n',
                             'columns = ' ,  str(columns) , '\n' ,
                             'type(columns)\n',
                             'return_data = {}\n',
                             'for column in columns :\n',
                              '  return_data[column.encode("UTF8")] = result.select(column).map(lambda x : str(x[0]).encode("UTF8")).distinct().collect()\n',
                             'str(return_data)'
                             ])
        }

        resp = requests.post("http://" + settings.LIVY_HOST + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(min(self.avail_sess_list)), \
                                          json.loads(resp.content, object_hook=JsonObject).id)

        return result["output"]["data"]["text/plain"].replace("\"", "")


    def delete_all_session(self):
        """
        delete all alive sessions on livy
        :return:
        """
        self.get_available_sess_id()
        for sess_id in self.alive_sess_list:
            requests.delete("http://" + settings.LIVY_HOST + "/sessions/" + str(sess_id), headers=self.headers)

        while(self.alive_sess_cnt == 0):
            self.check_alive_sessions()

    def save_csv_to_df(self, data_frame, table_name, csv_file):
        """
        create new table with inserted csv data
        :param net_id:
        :return:
        """
        self.get_available_sess_id()

        try:
            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            hdfs_path =  "hdfs://" + settings.HDFS_HOST + settings.HDFS_DF_ROOT + "/" + data_frame + "/" + table_name
            data = {
                'code': ''.join(['from pyspark.sql import SQLContext\n',
                                 'import pandas as pd\n',
                                 'sqlContext = SQLContext(sc)\n',
                                 'tp = pd.read_csv("' , str(file_path) , '")\n',
                                 'df_writer = sqlContext.createDataFrame(data=tp).write\n',
                                 'df.write.parquet("', str(hdfs_path) ,'" ,mode="append", partitionBy=None)\n',
                                 ])
            }
            resp = requests.post("http://" + settings.LIVY_HOST + "/sessions/" + str(min(self.avail_sess_list)) + \
                                 "/statements", data=json.dumps(data), headers=self.headers)
            result = self.get_response(str(min(self.avail_sess_list)), \
                                       json.loads(resp.content, object_hook=JsonObject).id)
            return result["output"]["data"]["text/plain"].replace("'", "")

        except Exception as e:
            raise Exception(e)
