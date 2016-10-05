from tfmsacore import train
from tfmsacore import netconf
from tfmsarest import livy
from tfmsacore.service import JobStateLoader,ServerConfLoader,ServerStateChecker
from tfmsacore.utils.logger import tfmsa_logger
import json

class JobManager:
    def __init__(self):
        tfmsa_logger("initialize JobManager!!")

    def regit_job(self, nnid, type, param = {'epoch' : '10', 'testset' : '100'}):
        """
        regist task on job manager
        :return:
        """
        try:
            # get server config information from db
            server_conf = ServerConfLoader().get()

            # get current running tasks from management db
            num_running = JobStateLoader().create(nnid, type, param)

            # check if there is a avail capacity for tfmsa
            if(int(server_conf['fw_capa']) > num_running):
                tfmsa_logger("Invoking next prority job")
                self.invoke_job()
                return "Run Next"
            else :
                tfmsa_logger("Job Pool is full now")
                return "Pend"

        except Exception as e:
            tfmsa_logger("regit_job : {0}".format(e))
            raise Exception (e)

    def invoke_job(self):
        """
        invoke job from job manager pool
        :return:
        """
        try :
            # find next job to run
            next = JobStateLoader().get_next()
            type = next['type']
            nnid = next['nn_id']
            epoch = next['epoch']
            testsets = next['testsets']

            print(nnid)
            print(type)
            JobStateLoader().set_run(nnid)

            """
            TO-DO: check server state
            """
            # check server state and raise error when server is not ok
            ServerStateChecker().check_servers()

            # run real jobs
            if(type == '1'):
                # run dataframe data preprocess
                nn_info = netconf.get_network_config(nnid)
                livy_client = livy.LivyDfClientManager()
                livy_client.create_session()
                print(nn_info)
                json_obj = json.loads(str(nn_info['datadesc']).replace("'", "\""))
                cate_column_list = []
                for column in json_obj.keys():
                    if (json_obj[column] == 'cate' or json_obj[column] == 'tag' or json_obj[column] == 'rank'):
                        cate_column_list.append(column)

                nninfo = netconf.get_network_config(nnid)
                dist_col_list = livy_client.get_distinct_column(nninfo['dir'], nninfo['table'], cate_column_list)
                netconf.set_train_datasets(nnid, str(dist_col_list))

            elif(type == '2'):
                # run neural network training
                train.train_conv_network(nnid, epoch, testsets)

            else :
                raise Exception("not defined task type!!")

            JobStateLoader().set_finish(nnid)

        except Exception as e :
            JobStateLoader().set_error(nnid)
            tfmsa_logger("invoke_job : {0}".format(e))
            raise Exception(e)

    def set_job_state(self, nn_id, state):
        """

        :return:
        """
        """
        TO-DO : find next job to run
        """

    def set_job_progress(self, nn_id, progress):
        """

        :return:
        """
        """
        TO-DO : find next job to run
        """