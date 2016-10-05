from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger

class ServerConfLoader:

    def post(self, req):
        """
        set new server configuration
        :param net_id:
        :return:
        """
        try:
            # set state Dead to current Alive conf
            obj = models.ServerConf.objects.filter(state__contains="A")
            obj.state = "D"
            obj.save()

            # set new conf with request data
            serializer = serializers.ServerConfSerializer(data=req)
            if serializer.is_valid():
                serializer.save()
                return req["version"]
        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

    def get(self):
        """
        get current server configuration
        :param net_id:
        :return:
        """
        try:
            data_set = models.ServerConf.objects.filter(state__contains="A")

            if(data_set.count() == 0 ):
                self.set_initial()
            else:
                return data_set[:1].get().json()
        except Exception as e:
            raise Exception(e)


    def set_initial(self):
        """
        insert initial server setting
        :return:
        """
        job = models.ServerConf(state="A",
                                store_type="0",
                                fw_capa="1")
        job.save()