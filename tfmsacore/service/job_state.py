from tfmsacore import models
from tfmsacore.utils import serializers
from django.core import serializers as serial
from datetime import datetime
from tfmsacore.utils.logger import tfmsa_logger
from tfmsacore import netconf
import json


class JobStateLoader:

    def create(self, nn_id, job_type, param):
        """
        set new server configuration
        :param net_id:
        :return:
        """
        try:
            current_time = datetime.now()
            obj, created = models.JobManagement.objects.get_or_create(nn_id=nn_id)

            if created :
                tfmsa_logger("create new with state ready")
                #obj.nn_id = nn_id
                obj.type = job_type
                obj.status = "1"
                obj.request = current_time
                obj.start = None
                obj.end = None
                obj.progress = "0"
                obj.epoch = param['epoch']
                obj.testsets = param['testset']
                obj.save()
            else :
                tfmsa_logger("update finished state to ready")
                obj = models.JobManagement.objects.get(nn_id__contains=nn_id, status__in = ['5','7','9'])
                obj.type = job_type
                obj.status = "1"
                obj.request = current_time
                obj.start = None
                obj.end = None
                obj.progress = "0"
                obj.epoch = param['epoch']
                obj.testsets = param['testset']
                obj.save()

            return len(models.JobManagement.objects.filter(status__in=['3']))

        except Exception as e:
            tfmsa_logger(e)
            return len(models.JobManagement.objects.filter(status__in=['3']))

    def set_run(self, nn_id):
        """
        set run flag
        :param nnid:
        :return:
        """
        try:
            current_time = datetime.now()
            obj = models.JobManagement.objects.get(nn_id=str(nn_id))
            obj.start =  current_time
            obj.status = '3'
            obj.progress = '0'
            obj.save()
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def set_finish(self, nn_id):
        """
        set finish flag
        :param nnid:
        :return:
        """
        try:
            current_time = datetime.now()
            obj = models.JobManagement.objects.get(nn_id=str(nn_id))
            obj.start =  current_time
            obj.status = '5'
            obj.progress = '100'
            obj.save()
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def set_error(self, nn_id):
        """
        set error flag
        :param nnid:
        :return:
        """
        try:
            current_time = datetime.now()
            obj = models.JobManagement.objects.get(nn_id=str(nn_id))
            obj.end =  current_time
            obj.status = '9'
            obj.progress = '50'
            obj.save()
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def get_all(self):
        """
        get all requested jobs
        :param net_id:
        :return:
        """
        try:
            data_set = models.JobManagement.objects.filter(status__in=["1","3","5","7","9"]).order_by('request')
            return data_set
        except Exception as e:
            raise Exception(e)

    def get_next(self):
        """
        get first priority job info
        :param net_id:
        :return:
        """
        try:
            tfmsa_logger("get_next Task Job!")
            data_set = models.JobManagement.objects.filter(status__contains="1").order_by('request')
            if(len(data_set) > 0):
                return data_set[0]
            else :
                return None
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)


    def set_request_time(self, nn_id, time):
        """
        update request time for job execute priority
        :param net_id:
        :return:
        """
        try:
            # example :.datetime(2013, 6, 5, 23, 59, 59, 999999)
            set_time = datetime(int(time['year']), int(time['month']), int(time['day']),
                                int(time['hour']), int(time['min']), int(time['sec']), 999999)
            obj = models.JobManagement.objects.get(nn_id=str(nn_id), status__in = ['1'])
            obj.request = set_time
            obj.save()
            return set_time
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def set_pend(self, nn_id):
        """
        set stop flag
        :param nnid:
        :return:
        """
        try:
            current_time = datetime.now()
            obj = models.JobManagement.objects.get(nn_id=str(nn_id), status__in = ['1'])
            obj.end =  current_time
            obj.status = '7'
            obj.progress = '0'
            obj.save()
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def check_running(self, nn_id):
        """
        check requested nn_id is already running
        :param nn_id:
        :return:
        """
        try :
            obj = models.JobManagement.objects.get(nn_id=nn_id)
            print(obj.status)
            return obj.status
        except Exception as e:
            return 0


    def set_data_pointer(self, nn_id, number):
        """
        set pointer number
        :param nn_id:
        :return:
        """
        try :
            obj = models.JobManagement.objects.get(nn_id=str(nn_id))
            obj.datapointer = str(number)
            obj.save()
            return obj.status
        except Exception as e:
            return 0

    def get_data_pointer(self, nn_id):
        """
        get pointer number
        :param nn_id:
        :return:
        """
        try :
            obj = models.JobManagement.objects.get(nn_id=str(nn_id))
            return obj.datapointer
        except Exception as e:
            return 0

    def set_table_info(self, base, table, col_len, row_len):
        """
        set table info
        :param nn_id:
        :return:
        """
        try:
            obj, created = models.DataTableInfo.objects.get_or_create(table_name=base + ":" + table)
            if created :
                tfmsa_logger("create new with state ready")
                obj.col_len = col_len
                obj.row_len = row_len
                obj.save()
            else :
                tfmsa_logger("update finished state to ready")
                obj = models.DataTableInfo.objects.get(table_name=base + ":" + table)
                obj.col_len = col_len
                obj.row_len = row_len
                obj.save()
            return True
        except Exception as e:
            tfmsa_logger(e)
            return False


    def get_table_info(self, base, table):
        """
        get table info
        :param nn_id:
        :return:
        """
        try:
            data_set = models.DataTableInfo.objects.filter(table_name=base + ":" + table)
            return data_set
        except Exception as e:
            tfmsa_logger(e)
            return False

    def init_job_info(self, nn_id):
        """
        get table info
        :param nn_id:
        :return:
        """
        try:
            net_info = netconf.get_network_config(nn_id)
            table_info = self.get_table_info(net_info['dir'], net_info['table'])
            data_set = models.JobManagement.objects.get(nn_id=str(nn_id))
            data_set.endpointer = str(table_info.row_len)
            data_set.datapointer = '0'
            data_set.save()
            return data_set
        except Exception as e:
            tfmsa_logger(e)
            return False

    def set_curr_train_data(self, nn_id, pnt):
        """
        set_curr_train_data
        :param nn_id:
        :return:
        """
        try:
            data_set = models.JobManagement.objects.get(nn_id=str(nn_id))
            data_set.datapointer = str(pnt)
            data_set.save()
            return data_set
        except Exception as e:
            tfmsa_logger(e)
            return False

    def get_selected_job_info(self, nn_id):
        """
        get selected netowrks job parms
        :param nn_id:
        :return:
        """
        try:
            data_set = models.JobManagement.objects.get(nn_id=str(nn_id))
            if(data_set.batchsize == ''):
                data_set.batchsize = '1000'
            if(data_set.epoch == ''):
                data_set.epoch = '10'
            if (data_set.datapointer == ''):
                data_set.datapointer = '0'
            data_set.save()
            return data_set
        except Exception as e:
            tfmsa_logger(e)
            return False

    def inc_job_data_pointer(self, nn_id):
        """

        :param nn_id:
        :return:
        """
        try:
            data_set = models.JobManagement.objects.get(nn_id=str(nn_id))
            data_set.datapointer = str(int(data_set.datapointer) + int(data_set.batchsize))
            data_set.save()
            return data_set
        except Exception as e:
            tfmsa_logger(e)
            return False