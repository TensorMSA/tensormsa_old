from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger
from django.core import serializers as serial
import json

def get_category_list():
    """
    get category list
    :param nn_id: serarch condition nn_id
    :return : all column data from nn_info as dic format
    """
    try:
        query_set = models.MetaCategory.objects.all()
        query_set = serial.serialize("json", query_set)
        json_object = []
        for set in json.loads(query_set) :
            print(set)
            json_object.append(set['fields']['category_name'])
        return json_object
    except Exception as e:
        raise Exception(e)

def get_subcategory_list(category):
    """
    query all eval result
    :param nn_id:
    :return:
    """
    try:
        query_set = models.MetaSubCategory.objects.filter(category_id=category).select_related()
        query_set = serial.serialize("json", query_set)
        json_object = []
        for set in json.loads(query_set) :
            json_object.append(set['fields']['subcategory_name'])
        return json_object
    except Exception as e:
        raise Exception(e)

def get_namespace(datatype, datastep, category, subcate):
    """
    get namespace name managed on hbase
    :param datatype: image, dataframe, rawtext
    :param datastep: raw, pre
    :param category: mes, scm, erp
    :param subcategory: chains
    :return:
    """
    try:
        query_set = models.DataSchemaCategory.objects.filter(filetype= datatype, \
                                                             datastep = datastep, \
                                                             category = category, \
                                                             subcate = subcate)
        query_set = serial.serialize("json", query_set)
        return query_set[0]['pk']
    except Exception as e:
        raise Exception(e)