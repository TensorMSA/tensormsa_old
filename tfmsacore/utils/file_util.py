import os, random
from django.conf import settings

def save_upload_file(request):
    """
    save http upload file on serve file system
    :param request:
    :param path:
    :return:
    """
    try:
        ran = random.randrange(1000, 9999)
        directory = settings.FILE_TEMP_UPLOAD_ROOT + "/" + str(ran)

        output_file_list = []
        for file in  request.FILES.getlist('file'):
            filename = file._name
            # save file on file system
            file_path = directory + "/" + filename
            output_file_list.append(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            fp = open(file_path, 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
        return output_file_list
    except Exception as e :
        raise Exception (e)
    finally :
        fp.close()


def delete_upload_file(directory_list):
    """
    delete file on path
    :param directory:
    :return:
    """
    for directory in directory_list:
        if os.path.isfile(directory):
            os.remove(directory)