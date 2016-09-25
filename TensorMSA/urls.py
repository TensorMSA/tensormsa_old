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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/type/cnn/service/$', rest_view.CNN_Service.as_view()),
    url(r'^api/type/cnn/service/$', rest_view.CNN_Service.as_view()),
    url(r'^api/v1/type/cnn/config/$', rest_view.CNN_Config.as_view()),
    url(r'^api/type/cnn/config/$', rest_view.CNN_Config.as_view()),
    url(r'^api/v1/type/cnn/data/$', rest_view.CNN_Data.as_view()),
    url(r'^api/type/cnn/data/$', rest_view.CNN_Data.as_view()),
    url(r'^api/v1/type/cnn/stastics/$', rest_view.CNN_Stastics.as_view()),
    url(r'^api/type/cnn/stastics/$', rest_view.CNN_Stastics.as_view()),
    url(r'^api/v1/type/cnn/common/$', rest_view.Common_config.as_view()),
    url(r'^api/type/cnn/common/$', rest_view.Common_config.as_view()),
    url(r'^view/index/$', ui_view.UI_Service.as_view()),
] + static('/dist/', document_root='tfmsaview/dist')
#static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)