import json, requests, textwrap

# json object hooker class
class JsonObject:
  def __init__(self, d):
    self.__dict__ = d

#json_data = json.loads(data, object_hook=JsonObject)


class LivyClientManager:
    def __init__(self, s_num):
        self.max_sess_num = s_num
        self.host = "http://481bf68ee6d9:8998"
        self.headers = {'Content-Type': 'application/json'}
        self.alive_sess_obj = None
        self.alive_sess_cnt = None
        self.alive_sess_list = []

    def create_session(self):
        """
        create session, get session id form return, run long code with that session
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
        print(r.json())
        print(r.json()['id'])

        return r.json()['id']

    def check_alive_sessions(self):
        """
        check alive sessions info
        :return:
        """
        self.alive_sess_list[:] = []
        self.alive_sess_cnt = 0
        self.alive_sess_obj = None
        resp = requests.get(self.host + "/sessions/" , headers=self.headers)
        print(resp.json())
        self.alive_sess_obj = json.loads(resp.content,  object_hook=JsonObject)
        self.alive_sess_cnt = len(self.alive_sess_obj.sessions)

        print(self.alive_sess_cnt)
        if(self.alive_sess_cnt > 0):
            for i in [0 , self.alive_sess_cnt -1]:
                self.alive_sess_list.append(self.alive_sess_obj.sessions[i].id)

    def delete_all_sessions(self):
        """
        delete all sessions
        :return:
        """
        print(self.alive_sess_list)
        for sess_id in self.alive_sess_list:
            print(sess_id)
            r = requests.delete(self.host + "/sessions/" + str(sess_id), headers=self.headers)
            print(r.json())

    def print_all(self):
        """
        print all values for test
        :return:
        """
        print("host : {0}".format(self.host))
        print("headers : {0}".format(self.headers))
        print("alive_sess_obj : {0}".format(self.alive_sess_obj))
        print("alive_sess_cnt : {0}".format(self.alive_sess_cnt))
        print("alive_sess_list : {0}".format(self.alive_sess_list))