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
from django.conf.urls import url, include
from django.contrib import admin
from tfmsarest import views as rest_view
from tfmsaview import views as ui_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [

    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^admin/', csrf_exempt(admin.site.urls)),
    # network info
    url(r'^api/v1/type/common/nninfo/(?P<nnid>.*)/category/(?P<cate>.*)/subcate/(?P<sub>.*)/',
        csrf_exempt(rest_view.CommonNetInfo.as_view())),
    url(r'^api/v1/type/common/nninfo/$',
        csrf_exempt(rest_view.CommonNetInfo.as_view())),
    url(r'^api/v1/type/common/nninfo/(?P<nnid>.*)/$',
        csrf_exempt(rest_view.CommonNetInfo.as_view())),

    # pre process for dataframe data
    url(r'^api/v1/type/dataframe/base/(?P<baseid>.*)/table/(?P<tb>.*)/pre/(?P<nnid>.*)/',
        csrf_exempt(rest_view.DataFramePre.as_view())),

    #data upload, search
    url(r'^api/v1/type/dataframe/base/(?P<baseid>.*)/table/(?P<tb>.*)/data/(?P<args>.*)/',
        csrf_exempt(rest_view.DataFrameData.as_view())),
    url(r'^api/v1/type/dataframe/base/(?P<baseid>.*)/table/(?P<tb>.*)/data/',
        csrf_exempt(rest_view.DataFrameData.as_view())),

    #manage column data types
    url(r'^api/v1/type/dataframe/base/(?P<baseid>.*)/table/(?P<tb>.*)/format/(?P<nnid>.*)/',
        csrf_exempt(rest_view.DataFrameFormat.as_view())),
    # get manage column data types
    url(r'^api/v1/type/dataframe/format/(?P<nnid>.*)/type/(?P<type>.*)/',
          csrf_exempt(rest_view.DataFrameFormat.as_view())),

    #manage table
    url(r'^api/v1/type/dataframe/base/(?P<baseid>.*)/table/(?P<tb>.*)/',
        csrf_exempt(rest_view.DataFrameTable.as_view())),
    url(r'^api/v1/type/dataframe/base/(?P<baseid>.*)/table/',
        csrf_exempt(rest_view.DataFrameTable.as_view())),

    #manage data frame
    url(r'^api/v1/type/dataframe/base/(?P<baseid>\w+:?(?=/))/',
        csrf_exempt(rest_view.DataFrameSchema.as_view())),
    url(r'^api/v1/type/dataframe/base/',
        csrf_exempt(rest_view.DataFrameSchema.as_view())),

    # CNN config data manage
    url(r'^api/v1/type/cnn/conf/(?P<nnid>.*)/',
        csrf_exempt(rest_view.ConvNeuralNetConfig.as_view())),


    # WDNN config data manage
    url(r'^api/v1/type/wdnn/conf/(?P<nnid>.*)/',
        csrf_exempt(rest_view.WideDeepNetConfig.as_view())),

    # WDNN predict
    url(r'^api/v1/type/wdnn/predict/(?P<nnid>.*)/',
        csrf_exempt(rest_view.WideDeepNetPredict.as_view())),

    # WDNN Train
    url(r'^api/v1/type/wdnn/train/(?P<nnid>.*)/',
        csrf_exempt(rest_view.WideDeepNetTrain.as_view())),

    # WDNN Eval
      url(r'^api/v1/type/wdnn/eval/(?P<nnid>.*)/',
          csrf_exempt(rest_view.WideDeepNetEval.as_view())),

    # CNN training
    url(r'^api/v1/type/cnn/train/(?P<nnid>.*)/',
        csrf_exempt(rest_view.ConvNeuralNetTrain.as_view())),

    # CNN predict
    url(r'^api/v1/type/cnn/predict/(?P<nnid>.*)/',
        csrf_exempt(rest_view.ConvNeuralNetPredict.as_view())),

    # Common Server status (spark, livy, train task, s3)
    url(r'^api/v1/type/common/env/',
        csrf_exempt(rest_view.CommonEnvInfo.as_view())),

    # Job Tracker Information
    url(r'^api/v1/type/common/job/(?P<nnid>.*)/',
        csrf_exempt(rest_view.CommonJobInfo.as_view())),
    url(r'^api/v1/type/common/job/',
        csrf_exempt(rest_view.CommonJobInfo.as_view())),

    # Server configuration information
    url(r'^api/v1/type/common/env/',
        csrf_exempt(rest_view.CommonEnvInfo.as_view())),

    # Livy Session Control API
    url(r'^api/v1/type/common/livy/',
        csrf_exempt(rest_view.CommonLivySession.as_view())),

    # Check Cnn configuration validation
    url(r'^api/v1/type/cnn/checker/(?P<nnid>.*)/',
         csrf_exempt(rest_view.ConvNeuralNetChecker.as_view())),

    # Evaluate accuracy of CNN model
     url(r'^api/v1/type/cnn/eval/(?P<nnid>.*)/',
          csrf_exempt(rest_view.ConvNeuralNetEval.as_view())),

    # imagedata - manage column data types
    url(r'^api/v1/type/imagefile/base/(?P<baseid>.*)/table/(?P<table>.*)/format/(?P<nnid>.*)/',
      csrf_exempt(rest_view.ImageFileFormat.as_view())),

    # imagedata - data upload, search
    url(r'^api/v1/type/imagefile/base/(?P<baseid>.*)/table/(?P<table>.*)/label/(?P<label>.*)/data/(?P<nnid>.*)/',
      csrf_exempt(rest_view.ImageFileData.as_view())),
    url(r'^api/v1/type/imagefile/base/(?P<baseid>.*)/table/(?P<table>.*)/label/(?P<label>.*)/data/',
      csrf_exempt(rest_view.ImageFileData.as_view())),

    # imagedata - data upload, search
    url(r'^api/v1/type/imagefile/label/(?P<label>.*)/nnid/(?P<nnid>.*)/',
      csrf_exempt(rest_view.ImageFileLabel.as_view())),
    url(r'^api/v1/type/imagefile/label/(?P<nnid>.*)/',
      csrf_exempt(rest_view.ImageFileLabel.as_view())),

    # imagedata - manage table
    url(r'^api/v1/type/imagefile/base/(?P<baseid>.*)/table/(?P<table>.*)/',
      csrf_exempt(rest_view.ImageFileTable.as_view())),
    url(r'^api/v1/type/imagefile/base/(?P<baseid>.*)/table/',
      csrf_exempt(rest_view.ImageFileTable.as_view())),

    # imagedata - manage data frame
    url(r'^api/v1/type/imagefile/base/(?P<baseid>.*)/',
      csrf_exempt(rest_view.ImageFileSchema.as_view())),
    url(r'^api/v1/type/imagefile/base/',
      csrf_exempt(rest_view.ImageFileSchema.as_view())),

    # image fire preview
    url(r'^api/v1/type/imgpreview/nnid/(?P<nnid>.*)/',
      csrf_exempt(rest_view.ImageFilePreview.as_view())),

    # cifar
    url(r'^api/v1/type/cifar/kind/ten/',
      csrf_exempt(rest_view.CifarTenPredict.as_view())),

    # common stat result
    url(r'^api/v1/type/common/stat/(?P<nnid>.*)/',
      csrf_exempt(rest_view.CommonResultStatInfo.as_view())),

    # search item list
    url(r'^api/v1/type/common/item/(?P<type>.*)/(?P<condition>.*)/',
      csrf_exempt(rest_view.CommonItems.as_view())),

    # Schema data
    url(r'^api/v1/type/schema/datatype/(?P<datatype>.*)/preprocess/(?P<preprocess>.*)/category/(?P<category>.*)/subcategory/(?P<subcategory>.*)/',
      csrf_exempt(rest_view.CommonSchema.as_view())),

    # UI / View index
    url(r'^$', csrf_exempt(ui_view.UI_Service.as_view())),
    url(r'^view/index/$', csrf_exempt(ui_view.UI_Service.as_view())),
    url(r'^view/ftptest/$', csrf_exempt(ui_view.FtpTest.as_view())),
    url(r'^view/ftpcsvpredict/$', csrf_exempt(ui_view.FtpCsvPredict.as_view())),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)