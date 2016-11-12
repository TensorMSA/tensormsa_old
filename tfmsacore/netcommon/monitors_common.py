import tensorflow as tf
import tensorflow.contrib.learn.python.learn.monitors as monitors
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore import netconf
import json
import datetime
from tfmsacore import utils
from TensorMSA import const

class MonitorCommon(monitors.EveryN):

    def __init__(self, p_nn_id, p_max_steps, p_every_n_steps = const.LOG_OUT_STEPS):

        utils.tfmsa_logger(" ## MonitorCommon Class Init ##")
        monitors.EveryN.__init__(self,every_n_steps=p_every_n_steps)
        self.max_steps =  p_max_steps
        self.nn_id = p_nn_id

    def end(self):
        utils.tfmsa_logger("MonitorCommon.end --> Completed run.")

    def every_n_step_begin(self, step):
        return []

    def every_n_step_end(self, step, outputs):
        utils.tfmsa_logger("MonitorCommon.every_n_step_end ---> Loggin "+ str(step))
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
        logInfoData = dict()
        logInfoData["nn_id"] = self.nn_id
        logInfoData["loss"] = str(self.get_loss(outputs))
        logInfoData["step"] = str(step)
        logInfoData["max_step"] = self.max_steps
        logInfoData["trainDate"] = nowDate
        logInfoData["testsets"] = "1"
        self.monitors_update(logInfoData)


    def monitors_update(self, logInfoData):
        """ Monitor update
            :param nnid
            :param model_dir : directory of chkpoint of wdnn model
        """
        try:
            utils.tfmsa_logger("MonitorCommon.monitors_update_end ---> postgres" )
            body=json.loads(json.dumps(logInfoData))
            return_data = netconf.post_train_loss(body)
        except Exception as e:
            print("Error Message : {0}".format(e))
            raise Exception(e)
        finally:
            return return_data


    def get_loss(self, outputs):
        """
        find loss column and return
        :param outputs: dict type value
        :return:
        """
        key_list = outputs.keys()
        for key in key_list:
            if(isinstance(key, (str))):
                return outputs[key]
