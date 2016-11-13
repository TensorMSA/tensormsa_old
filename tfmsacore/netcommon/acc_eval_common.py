from TensorMSA import const
from tfmsacore import netconf
from tfmsacore.utils.json_conv import JsonDataConverter as jc

class AccStaticResult:
    """
    {1 : {1:30, 2:30}, 2 : {1:30, 2:30}}
    """
    #
    acc_result_list = {}
    chk_steps = 0
    prd_success = 0
    prd_fail = 0

class AccEvalCommon():
    """
    manage train result
    """

    def __init__(self,  net_id):
        """
        set network id on init
        :param net_id:
        """
        self.nn_id = net_id
        self.steps_put_db = const.ACC_OUT_STEPS


    def set_result(self, real_result, prd_result):
        """
        get one predict and real and update
        :param prd_result:model predicted result
        :param real_result:real result we know
        :return:
        """
        if real_result not in AccStaticResult.acc_result_list.keys():
            AccStaticResult.acc_result_list[real_result] = {}

        AccStaticResult.acc_result_list[real_result] = \
            self.set_guess(AccStaticResult.acc_result_list[real_result], prd_result)
        AccStaticResult.chk_steps = AccStaticResult.chk_steps + 1

        if(real_result == prd_result):
            AccStaticResult.prd_success = AccStaticResult.prd_success + 1
        else :
            AccStaticResult.prd_fail = AccStaticResult.prd_fail + 1

        if (AccStaticResult.chk_steps % self.steps_put_db == 0):
            self.save_result(AccStaticResult.acc_result_list)

    def set_guess(self, guess_set, prd_result):
        """
        set each label's result
        :param guess_set:each label's result set
        :param prd_result:predict result
        :return:
        """
        if prd_result not in guess_set.keys():
            guess_set[prd_result] = 1
        else :
            guess_set[prd_result] = guess_set[prd_result] + 1
        return guess_set

    def save_result(self, train_result):
        """
        save result on db
        :param train_result:
        :return:
        """
        netconf.delete_train_acc(self.nn_id)
        for prd_id in train_result.keys():
            save_set = {}
            save_set['nn_id'] = self.nn_id
            save_set['label'] = prd_id
            for acc_result in train_result[prd_id].keys():
                save_set['guess'] = acc_result
                save_set['ratio'] = train_result[prd_id][acc_result]
                netconf.post_train_acc(save_set)

        jd = jc.load_obj_json("{}")
        jd.nn_id = self.nn_id
        jd.testpass = AccStaticResult.prd_success
        jd.testfail = AccStaticResult.prd_fail
        jd.acc = AccStaticResult.prd_success / (AccStaticResult.prd_success + AccStaticResult.prd_fail)
        netconf.update_network(jd)


    def reverse_result(self):
        """
        reverse db stored data to view usable json
        :param nn_id:
        :return:
        """
        return_data = {}
        result_data = netconf.get_train_acc(self.nn_id)
        for raw in result_data:
            if raw['fields']['label'] not in return_data.keys() :
                return_data[raw['fields']['label']] = {}

            guess_set = return_data[raw['fields']['label']]
            guess_set[raw['fields']['guess']] = raw['fields']['ratio']
        return return_data