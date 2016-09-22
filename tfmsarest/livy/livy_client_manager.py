import json, requests, textwrap, time, random, os


class JsonObject:
    """
    json object hooker class
    """
    def __init__(self, d):
        self.__dict__ = d

    def __getitem__(self, item):
        return self.__dict__[item]


class LivyDfClientManager:
    def __init__(self, s_num):
        self.max_sess_num = s_num
        self.host = ""
        self.hdfs_path = ""
        self.headers = {'Content-Type': 'application/json'}
        self.alive_sess_obj = None
        self.alive_sess_cnt = None
        self.alive_sess_list = []
        self.alive_sess_state = []
        self.avail_sess_list = []

        self.load_conf()

    def load_conf(self):
        """
        load livy config from file
        :return: None
        """
        try :
            livy_conf = open("/home/dev/TensorMSA/TensorMSA/tfmsa_settings.json" , 'r')
            json_data = json.loads(livy_conf.read(), object_hook=JsonObject)
            self.host = "http://" + json_data.livy.ip + ":" + json_data.livy.port
            self.hdfs_path = json_data.hdfs.path
            livy_conf.close()
        except IOError as e:
            return e


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
                "executorCores": 1,
                "executorMemory": "512m",
                "driverCores": 1,
                "driverMemory": "512m"}
        r = requests.post(self.host + "/sessions", data=json.dumps(data), headers=self.headers)
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
        resp = requests.get(self.host + "/sessions/" , headers=self.headers)
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

        resp = requests.get(self.host + "/sessions/" , headers=self.headers)
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
            r = requests.delete(self.host + "/sessions/" + str(sess_id), headers=self.headers)
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


    def create_table(self, table_name, json_data):
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
                             'df_writer.parquet("' , str(self.hdfs_path), "/", table_name ,
                             '", mode="overwrite", partitionBy=None)'
                             ])
        }
        resp = requests.post(self.host + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        temp_resp = json.loads(resp.content, object_hook=JsonObject)
        result = self.get_response(str(min(self.avail_sess_list)), temp_resp.id)
        return result

    def append_data(self, table_name, json_data):
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
                             'df = sqlContext.read.load("', str(self.hdfs_path),
                                                  "/", table_name, '" , "parquet" )\n'
                             'df_writer = sqlContext.createDataFrame(', str(json_data)  ,')\n',
                             'df.unionAll(df_writer)\n',
                             'df.write.parquet("', str(self.hdfs_path), "/", table_name,
                             '", mode="append", partitionBy=None)\n'
                             ])
        }

        print("request codes : {0} ".format(data))
        resp = requests.post(self.host + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        temp_resp = json.loads(resp.content, object_hook=JsonObject)
        result = self.get_response(str(min(self.avail_sess_list)), temp_resp.id)
        print("result : {0} ".format(result))

    def get_response(self, session_id, statements_id):
        """
        wait for Livy running and get return when finished
        :param session_id:session id used on request
        :param statements_id: statements id used on request
        :return: response result from livy
        """
        if(statements_id == None):
            resp = requests.get(self.host + "/sessions/" + str(session_id)  \
                                , headers=self.headers)
        else:
            resp = requests.get(self.host + "/sessions/" + str(session_id) +  \
                                "/statements/" + str(statements_id), \
                                headers=self.headers)

        response_obj = json.loads(resp.content, object_hook=JsonObject)

        if(response_obj.state == 'running'):
            time.sleep(1)
            return self.get_response(session_id, statements_id)
        elif(response_obj.state == 'starting'):
            time.sleep(1)
            return self.get_response(session_id, statements_id)
        else:
            print("Response : {0}".format(resp.json()))
            return resp.json()



    def query_data(self, table_name, query_str):
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
                             'rows = sqlContext.read.load("' , str(self.hdfs_path),
                             "/" ,table_name , '" , "parquet" )\n',
                             'tbl = rows.registerTempTable("' , table_name , '")\n',
                             'result = sqlContext.sql("' , str(query_str) ,
                             '").toJSON(False).map(lambda x : x).collect()\n',
                             'result'
                             ])
        }

        resp = requests.post(self.host + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(min(self.avail_sess_list)), \
                                          json.loads(resp.content, object_hook=JsonObject).id)

        return result["output"]["data"]["text/plain"].replace("'", "")


    def query_stucture(self, table_name):
        """
        return parqueet data strucure stored on spark
        :param table_name: table name you request
        :return: JSON
        """
        self.get_available_sess_id()

        data = {
            'code': ''.join(['from pyspark.sql import SQLContext\n',
                             'sqlContext = SQLContext(sc)\n',
                             'rows = sqlContext.read.load("', str(self.hdfs_path),
                              "/" , table_name, '" , "parquet" ).schema.json()\n',
                             'rows'
                             ])
        }

        resp = requests.post(self.host + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(min(self.avail_sess_list)), \
                                          json.loads(resp.content, object_hook=JsonObject).id)
        return result["output"]["data"]["text/plain"].replace("'", "")

    def get_distinct_column(self, table_name, columns):
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
                             'rows = sqlContext.read.load("' , str(self.hdfs_path),
                             "/" ,table_name , '" , "parquet" )\n',
                             'tbl = rows.registerTempTable("' , table_name , '")\n',
                             'result = sqlContext.sql("' , str(query_str) ,
                             '")\n',
                             'columns = ' ,  str(columns) , '\n' ,
                             'type(columns)\n'
                             'return_data = {}\n'
                             'for column in columns :\n'
                             '  return_data[column.encode("UTF8")] = result.select(column).map(lambda x : x[0].encode("UTF8")).distinct().collect()\n',
                             'str(return_data)'
                             ])
        }

        resp = requests.post(self.host + "/sessions/" + str(min(self.avail_sess_list)) + \
                             "/statements", data=json.dumps(data), headers=self.headers)
        result = self.get_response(str(min(self.avail_sess_list)), \
                                          json.loads(resp.content, object_hook=JsonObject).id)

        return result["output"]["data"]["text/plain"].replace("\"", "")