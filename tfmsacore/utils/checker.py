from tfmsacore import netconf
from tfmsarest import livy
import os

def check_requested_nn(nn_id):
    """
    validation checks
    TO-DO : NN name on the list check
    TO-DO : NN model conf on the db check
    TO-DO : NN model trained data on the db check
    """
    try :
        conf = netconf.get_network_config(nn_id)
        if(check_nn_exist(conf, nn_id) == False):
            return "network info not exist"

        if(check_nn_conf_exist(conf, nn_id) == False):
            return "network configuration not exist"

        if(check_nn_data_exist(conf, nn_id) == False):
            return "training data not exist"

        return "ok"

    except SyntaxError as e:
        return e

def check_nn_exist(conf, nn_id):
    """
    TO-DO : get connection and check id exsit
    :param conf : configuration data on database
    :param nn_id: neural network management id
    :return:
    """
    if(conf.nn_id != nn_id):
        return True
    else :
        return False




def check_nn_conf_exist(conf, nn_id):
    """
    TO-DO : get connection and check id exsit
    :param conf : configuration data on database
    :param nn_id: neural network management id
    :return:
    """
    if(netconf.chk_conf(nn_id) & conf.config == "Y"):
        return True
    else:
        return False


def check_nn_data_exist(conf, nn_id):
    """
    TO-DO : get connection and check id exsit
    :param conf : configuration data on database
    :param nn_id: neural network management id
    :return:
    """
    livy_client = livy.LivyDfClientManager(2)
    livy_client.create_session()

    if (livy_client.query_stucture(conf.table) != None):
        return True
    else:
        return False