from tfmsacore import models
from django.core import serializers as serial
import json

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
        obj.datadesc = "Y"
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
        obj.datadesc = "N"
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

def set_on_train(nn_id):
    """
    set train exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.train = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_off_train(nn_id):
    """
    set train exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.train = "N"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_on_eval(nn_id):
    """
    set train exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.samplenum = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_off_eval(nn_id):
    """
    set train exist flag off
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.samplenum = "N"
        obj.save()

    except Exception as e:
        raise Exception(e)

def set_acc(nn_id, acc):
    """
    set accuracy result of model
    :param nn_id:net id to set flag
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.acc = acc
        obj.save()

    except Exception as e:
        raise Exception(e)

def get_thread_status(nn_id):
    """
       search network eval suummary
       :param net_id:
       :return:
       """
    try:
        result_set = {}
        query_set = models.JobManagement.objects.get(nn_id=str(nn_id))
        result_set['status'] = query_set.status
        result_set['datapointer'] = query_set.datapointer
        result_set['endpointer'] = query_set.endpointer
        result_set['batchsize'] = query_set.batchsize
        result_set['epoch'] = query_set.epoch
        result_set['progress'] = query_set.progress
        return result_set
    except Exception as e:
        return e