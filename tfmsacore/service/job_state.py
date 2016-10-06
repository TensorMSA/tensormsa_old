from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger
from datetime import datetime


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
            if(len(data_set) > 0 ):
                return data_set[0].json()
            else:
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