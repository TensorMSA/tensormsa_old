pkill -f uwsgi -9
pkill -f nginx

uwsgi /home/dev/uwsgi/tensormsa.ini --emperor /home/dev/TensorMSA &

/usr/sbin/nginx

chmod 777 /home/dev/TensorMSA/TensorMSA.sock
