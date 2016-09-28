"""TensorMSA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
Multi Relational service (not need for now )
    ex: #url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
"""
from django.conf.urls import url
from django.contrib import admin
from tfmsarest import views as rest_view
from tfmsaview import views as ui_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', csrf_exempt(admin.site.urls)),
    url(r'^api/v1/type/cnn/train/$', csrf_exempt(rest_view.ConvNeuralNet_Train.as_view())),
    url(r'^api/type/cnn/train/$', csrf_exempt(rest_view.ConvNeuralNet_Train.as_view())),
    url(r'^api/v1/type/cnn/predict/$', csrf_exempt(rest_view.ConvNeuralNet_Predict.as_view())),
    url(r'^api/type/cnn/predict/$', csrf_exempt(rest_view.ConvNeuralNet_Predict.as_view())),
    url(r'^api/v1/type/cnn/config/(?P<pk>.*)/$',  csrf_exempt(rest_view.CNN_Config.as_view())),
    url(r'^api/type/cnn/config/(?P<pk>.*)/$',  csrf_exempt(rest_view.CNN_Config.as_view())),
    url(r'^api/v1/type/cnn/config/$',  csrf_exempt(rest_view.CNN_Config.as_view())),
    url(r'^api/type/cnn/config/$',  csrf_exempt(rest_view.CNN_Config.as_view())),
    url(r'^api/v1/type/cnn/data/(?P<pk>.*)/$', csrf_exempt(rest_view.CNN_Data.as_view())),
    url(r'^api/type/cnn/data/(?P<pk>.*)/$', csrf_exempt(rest_view.CNN_Data.as_view())),
    url(r'^api/v1/type/cnn/data/$', csrf_exempt(rest_view.CNN_Data.as_view())),
    url(r'^api/type/cnn/data/$', csrf_exempt(rest_view.CNN_Data.as_view())),
    url(r'^api/v1/type/cnn/stastics/$', csrf_exempt(rest_view.CNN_Stastics.as_view())),
    url(r'^api/type/cnn/stastics/$', csrf_exempt(rest_view.CNN_Stastics.as_view())),
    url(r'^api/v1/type/cnn/common/$', csrf_exempt(rest_view.Common_config.as_view())),
    url(r'^api/type/cnn/common/$', csrf_exempt(rest_view.Common_config.as_view())),
    url(r'^view/index/$', csrf_exempt(ui_view.UI_Service.as_view())),
] + static('/dist/', document_root='tfmsaview/dist')
#static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)