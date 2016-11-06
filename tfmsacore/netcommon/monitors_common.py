import tensorflow as tf
import tensorflow.contrib.learn.python.learn.monitors as monitors
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore import netconf
import json
import datetime
from tfmsacore import utils


class MonitorCommon(monitors.EveryN):

    def __init__(self, p_nn_id, p_max_steps, p_every_n_steps = 100):

        utils.tfmsa_logger(" ## MonitorCommon Class Init ##")
        monitors.EveryN.__init__(self,every_n_steps=p_every_n_steps)
        self.max_steps =  p_max_steps
        self.nn_id = p_nn_id
        #self.every_n_steps = every_n_steps
        #print("event_n_Stop " + str(self.every_n_steps))
        #print(super._max_steps)
        #print("init MinoterCommon")
        #monitors.BaseMonitor.EveryN.__init__(self,every_n_steps = every_n_steps_v )
        #m.
        print
        'Init Monitors######################'


    def end(self):
        utils.tfmsa_logger("MonitorCommon.end --> Completed run.")
        #print("Completed run.")


    def every_n_step_begin(self, step):
        #utils.tfmsa_logger("MonitorCommon.every_n_step_begin")
        print("About to run step")
        #print(step)
        #'About to run step %d...' % step
        return ['loss_1:0']

    def every_n_step_end(self, step, outputs):
        #print("MonitorCommon.every_n_step_end ---> Loggin")
        utils.tfmsa_logger("MonitorCommon.every_n_step_end ---> Loggin "+ str(step))
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
        #print(nowDate)
        #print("max_step!!!!!!")
        #print(self.max_steps)
        logInfoData = dict()
        logInfoData["nn_id"] = self.nn_id
        logInfoData["loss"] = str(outputs['loss_1:0'])
        logInfoData["step"] = str(step)
        logInfoData["max_step"] = self.max_steps
        logInfoData["trainDate"] = nowDate
        logInfoData["testsets"] = "1"

        print(outputs['loss_1:0'])
        self.monitors_update(logInfoData)


    def monitors_update(self,logInfoData):
        """ Monitor update
            :param nnid
            :param model_dir : directory of chkpoint of wdnn model
        """
        try:
            """
                             "nn_id": "nn0000100",
                             "loss": "0.001",
                             "step": "100",
                             "max_step": "1000",
                             "trainDate": "2013-01-29",
                             "testsets": "1"
            """
            utils.tfmsa_logger("MonitorCommon.monitors_update_end ---> postgres" )
            body=json.loads(json.dumps(logInfoData));
            print(body)
            return_data = netconf.insert_train_results(body)
            print(return_data)
            #return_data =  "1"

        except Exception as e:
            print("Error Message : {0}".format(e))
            raise Exception(e)
        finally:
            return return_data