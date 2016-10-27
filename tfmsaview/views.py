from django.views.generic.base import TemplateView

class UI_Service(TemplateView):
    template_name = 'index.html'

class FtpTest(TemplateView):
    template_name = 'ftp_test.html'

class FtpCsvPredict(TemplateView):
    template_name = 'ftp_csv_predict.html'

