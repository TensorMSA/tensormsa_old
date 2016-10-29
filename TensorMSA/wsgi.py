"""
WSGI config for TensorMSA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os, sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

sys.path.append('/root/anaconda3/lib/python3.5/site-packages/')
sys.path.append('/usr/lib64/python2.7/importlib/')
sys.path.append('/home/dev/TensorMSA/TensorMSA/')
sys.path.append('/home/dev/TensorMSA/')
sys.path.append('/home/dev/TensorMSA/tfmsaview/')
sys.path.append('/home/dev/TensorMSA/tfmsarest/')
sys.path.append('/home/dev/TensorMSA/tfmsacore/')

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TensorMSA.settings")
application = get_wsgi_application()
