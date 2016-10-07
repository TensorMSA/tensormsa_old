from tfmsacore import netconf
from tfmsarest import livy
from tfmsacore.utils.logger import tfmsa_logger
import os


def check_requested_nn(nn_id):
    """
    validation checks
    TO-DO : NN name on the list check
    TO-DO : NN model conf on the db check
    TO-DO : NN model trained data on the db check
    """
    conf = netconf.get_network_config(nn_id)

    if(check_nn_exist(conf, nn_id) == False):
        raise SyntaxError("network info not exist")

    if(check_nn_conf_exist(conf, nn_id) == False):
        raise SyntaxError("network configuration not exist")

    if (check_nn_datadesc_exist(conf) == False):
        raise SyntaxError("network column types are not defined")

    if (check_nn_datasets_exist(conf) == False):
        raise SyntaxError("network categorical type list not exists")

    # if(check_nn_data_exist(conf, nn_id) == False):
    #     raise Exception("training data not exist")



def check_nn_exist(conf, nn_id):
    """
    TO-DO : get connection and check id exsit
    :param conf : configuration data on database
    :param nn_id: neural network management id
    :return:
    """
    if(conf['nn_id'] == nn_id):
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
    if(netconf.chk_conf(nn_id) and conf['config'] == "Y"):
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

    if (livy_client.query_stucture(conf['table']) != None):
        return True
    else:
        return False


def check_nn_datadesc_exist(conf):
    """
    check datadesc info is exists
    :param conf : configuration data on database
    :return: Boolean
    """
    if (len(conf['datadesc']) > 0):
        return True
    else:
        return False


def check_nn_datasets_exist(conf):
    """
    check datasets info is exists
    :param conf : configuration data on database
    :return: Boolean
    """
    if (len(conf['datasets']) > 0):
        return True
    else:
        return False