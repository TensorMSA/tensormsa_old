from tfmsacore import models


def set_on_data(nn_id):
    """
    set data exist flag on
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.datavaild = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)


def set_off_data(nn_id):
    """
    set data exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.datavaild = "N"
        obj.save()

    except Exception as e:
        raise Exception(e)


def set_on_data_conf(nn_id):
    """
    set data conf exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.datavaild = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_off_data_conf(nn_id):
    """
    set data conf exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.datavaild = "N"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_on_net_conf(nn_id):
    """
    set data conf exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.config = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_off_net_conf(nn_id):
    """
    set data conf exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.config = "N"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_on_net_vaild(nn_id):
    """
    set net vaild flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.confvaild = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_off_net_vaild(nn_id):
    """
    set net vaild flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.confvaild = "N"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_on_train(nn_id, acc):
    """
    set train exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.train = "Y"
        obj.acc = acc
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_off_train(nn_id, acc):
    """
    set train exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.train = "N"
        obj.acc = ""
        obj.save()

    except Exception as e:
        raise Exception(e)