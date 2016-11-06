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
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file._name
            # save file on file system
            file_path = directory + "/" + filename
            print(directory)
            if not os.path.exists(directory):
                os.makedirs(directory)
            fp = open(file_path, 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
        return file_path
    except Exception as e :
        raise Exception (e)
    finally :
        fp.close()


def delete_upload_file(directory):
    """
    delete file on path
    :param directory:
    :return:
    """
    if os.path.isfile(directory):
        os.remove(directory)