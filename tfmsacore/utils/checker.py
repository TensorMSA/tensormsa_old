

def check_requested_nn(nn_id):
    """
    validation checks
    TO-DO : NN name on the list check
    TO-DO : NN model conf on the db check
    TO-DO : NN model trained data on the db check
    """
    try :
        check_nn_exist(nn_id)
        check_nn_conf_exist(nn_id)
        check_nn_data_exist(nn_id)

        return "ok"

    except SyntaxError as e:
        return e

def check_nn_exist(nn_id):
    """
    TO-DO : get connection and check id exsit
    :param nn_id:
    :return:
    """
    if(nn_id == "sample"):
        return True
    else :
        raise SyntaxError("network id you request do not exist")




def check_nn_conf_exist(nn_id):
    """
    TO-DO : get connection and check id exsit
    :param nn_id:
    :return:
    """
    if (nn_id == "sample"):
        return True
    else:
        raise SyntaxError("network conf of id you request do not exist")


def check_nn_data_exist(nn_id):
    """
    TO-DO : get connection and check id exsit
    :param nn_id:
    :return:
    """
    if (nn_id == "sample"):
        return True
    else:
        raise SyntaxError("network data of id you request do not exist")