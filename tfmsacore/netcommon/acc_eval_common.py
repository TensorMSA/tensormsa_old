from TensorMSA import const
from tfmsacore import netconf
from tfmsacore.utils.json_conv import JsonDataConverter as jc

class AccStaticResult():
    """
    {1 : {1:30, 2:30}, 2 : {1:30, 2:30}}
    """
    #
    def __init__(self):
        self._acc_result_list = {}
        self._chk_steps = 0
        self._prd_success = 0
        self._prd_fail = 0

    @property
    def acc_result_list(self):
        return self._acc_result_list

    @acc_result_list.setter
    def acc_result_list(self, value):
        self._acc_result_list = value

    @property
    def chk_steps(self):
        return self._chk_steps

    @chk_steps.setter
    def chk_steps(self, value):
        self._chk_steps = value

    @property
    def prd_success(self):
        return self._prd_success

    @prd_success.setter
    def prd_success(self, value):
        self._prd_success = value

    @property
    def prd_fail(self):
        return self._prd_fail

    @prd_fail.setter
    def prd_fail(self, value):
        self._prd_fail = value

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

    def set_result(self, result_obj ,real_result, prd_result):
        """
        get one predict and real and update
        :param prd_result:model predicted result
        :param real_result:real result we know
        :return:
        """
        if real_result not in result_obj.acc_result_list.keys():
            result_obj.acc_result_list[real_result] = {}

        result_obj.acc_result_list[real_result] = \
        self.set_guess(result_obj.acc_result_list[real_result], prd_result)
        result_obj.chk_steps = result_obj.chk_steps + 1

        if(real_result == prd_result):
            result_obj.prd_success = result_obj.prd_success + 1
        else :
            result_obj.prd_fail = result_obj.prd_fail + 1

        if (result_obj.chk_steps % self.steps_put_db == 0):
            self.save_result(result_obj, result_obj.acc_result_list)

        return result_obj

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

    def save_result(self, result_obj, train_result):
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
        jd.testpass = result_obj.prd_success
        jd.testfail = result_obj.prd_fail
        jd.acc = result_obj.prd_success / (result_obj.prd_success + result_obj.prd_fail)
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