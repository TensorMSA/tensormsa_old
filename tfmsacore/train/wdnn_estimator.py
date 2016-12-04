# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
from tfmsacore import data
from tfmsacore import netconf
from tfmsacore.netcommon.wdnn_common import WdnnCommonManager
import json, math
from tfmsacore.netcommon import monitors_common as Monitors
from tfmsacore.utils.logger import tfmsa_logger
from tfmsacore.service.job_state import JobStateLoader

class wdnn_train(WdnnCommonManager):
    def __init__(self):
        tfmsa_logger("[1] Create wdnn_train ")
        WdnnCommonManager.__init__(self)

    def run_wdd_train(self, nnid, start_pnt=1, batch_size = 1000):
        """
                Wide & Deep Network Training
                :param nnid : network id in tfmsacore_nninfo
                :return: acturacy
        """
        try:
            tfmsa_logger("[2] start run wdd_Train " + nnid)
            #make wide & deep model
            wdnn_model = WdnnCommonManager.wdnn_build(self, nnid = nnid)

            #get json from postgres by nnid
            json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
            database = json_string["dir"]
            table_name = json_string["table"]

            #Make NetworkConfiguration Json Objct
            json_string = netconf.load_ori_format(nnid)
            json_ob = json.loads(json_string)

            #get label column from hbase nn config json
            t_label = json_ob["label"]
            label_column = list(t_label.keys())[0]

            #get train hyper param
            job_parm = JobStateLoader().get_selected_job_info(nnid)
            batch_size = int(job_parm.batchsize)
            model_lint_cnt = int(job_parm.epoch)

            tfmsa_logger("[3] Get Dataframe from Hbase ##Start## {0},{1},{2},{3} ".format(start_pnt,database,table_name,label_column))
            df, pnt = data.DataMaster().query_data(database, table_name, "a", use_df=True,limit_cnt=batch_size,with_label=label_column, start_pnt = start_pnt)
            df_eval = df.copy()

            tfmsa_logger("[4] Get Dataframe from Hbase ##End## (" + str(batch_size) + ")")

            ##MAKE MONITOR
            tfmsa_logger("[5] Make Monitor Class")
            customsMonitor = Monitors.MonitorCommon(p_nn_id = nnid, p_max_steps=model_lint_cnt, p_every_n_steps=1000)

            tfmsa_logger("[6] start fitting")
            wdnn_model.fit(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid), steps=model_lint_cnt, monitors=[customsMonitor])

            if(start_pnt == pnt):
                tfmsa_logger("[7] Train Result")
                results = wdnn_model.evaluate(input_fn=lambda: WdnnCommonManager.input_fn(self, df_eval, nnid), steps=1)
                for key in sorted(results):
                    tfmsa_logger("%s: %s" % (key, results[key]))
                return nnid
            else:
                JobStateLoader().inc_job_data_pointer(nnid)
                self.run_wdd_train(nnid = nnid , start_pnt = pnt)

            return nnid
        except Exception as e:
            print ("Error Message : {0}".format(e))
            raise Exception(e)

