from tfmsacore.train.conv_train import train_conv_network
from tfmsacore.evaluation import eval_conv_network
from tfmsacore.train.wdnn_estimator import wdnn_train
from tfmsacore.evaluation.wdnn_eval import wdnn_eval
from tfmsacore import netconf
from TensorMSA import const
from tfmsacore import data
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
            if(JobStateLoader().check_running(nnid) == '3'):
                tfmsa_logger("==REJECT==")
                raise Exception ("reject")

            # get current running tasks from management db
            num_running = JobStateLoader().create(nnid, type, param)

            # check if there is a avail capacity for tfmsa
            if(int(const.MAX_JOB_CAPA) > num_running):
                tfmsa_logger("==RUN==")
                self.invoke_job()
                return "run"
            else :
                tfmsa_logger("==PEND==")
                raise Exception("pend")

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
            type = next.type
            nnid = next.nn_id
            epoch = next.epoch
            testsets = next.testsets
            JobStateLoader().set_run(nnid)

            """
            TO-DO: check server state
            """
            # check server state and raise error when server is not ok
            ServerStateChecker().check_servers()

            # run real jobs
            if(type == const.JOB_TYPE_CNN_TRAIN):
                netconf.set_off_train(nnid)
                train_conv_network(nnid, epoch, testsets)
                netconf.set_on_train(nnid)
            elif(type == const.JOB_TYPE_CNN_EVAL):
                netconf.set_off_eval(nnid)
                eval_conv_network(nnid)
                netconf.set_on_eval(nnid)
            elif (type == const.JOB_TYPE_WDNN_TRAIN):
                JobStateLoader().init_job_info(nnid)
                netconf.set_off_train(nnid)
                wdnn_train().run_wdd_train(nnid)
                netconf.set_on_train(nnid)
            elif (type == const.JOB_TYPE_WDNN_EVAL):
                netconf.set_off_eval(nnid)
                wdnn_eval().wdd_eval(nnid)
                netconf.set_on_eval(nnid)
            else :
                raise Exception("not defined task type!!")

            JobStateLoader().set_finish(nnid)

        except Exception as e :
            JobStateLoader().set_error(nnid)
            tfmsa_logger("invoke_job : {0}".format(e))
            raise Exception(e)

    def dataframe_pre_process(self, nnid):
        """
        dataframe_pre_process
        :param nnid:
        :return:
        """
        # run dataframe data preprocess
        nn_info = netconf.get_network_config(nnid)

        json_obj = json.loads(str(nn_info['datadesc']).replace("'", "\""))
        cate_column_list = []
        for column in json_obj.keys():
            if (json_obj[column] == 'cate' or json_obj[column] == 'tag' or json_obj[column] == 'rank'):
                cate_column_list.append(column)

        nninfo = netconf.get_network_config(nnid)
        dist_col_list = data.DataMaster().get_distinct_dataframe(nninfo['dir'], nninfo['table'], cate_column_list)
        netconf.set_train_datasets(nnid, str(json.dumps(dist_col_list)))


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