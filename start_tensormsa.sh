echo "======================="
echo "set path, env variables"
echo "======================="

source ~/.bashrc
export PATH="/root/anaconda2/bin:$PATH"
source ~/anaconda2/bin/activate ~/anaconda2/
export PATH="/home/dev/java/bin:$PATH"
export SPARK_HOME=/home/dev/spark
export HADOOP_CONF_DIR=/home/dev/hadoop/conf
export M2_HOME=/usr/local/maven
export PATH=${M2_HOME}/bin:${PATH}

echo $SPARK_HOME
echo $HADOOP_CONF_DIR
echo $M2_HOME

echo "======================="
echo "step1 : start postgresql"
echo "======================="

runuser -l postgres -c 'pg_ctl start'

echo "======================="
echo "step2 : start spark apps"
echo "======================="
 
sudo /home/dev/spark/sbin/stop-master.sh
sudo /home/dev/spark/sbin/start-master.sh
sudo /home/dev/spark/sbin/start-slave.sh http://$1:7077

echo "======================="
echo "step3 : start Livy"
echo "======================="
 
echo sudo /home/dev/livy/bin/livy-server &

echo "======================="
echo "step4 : start Django"
echo "======================="

cd /home/dev/TensorMSA/
pkill -f "python manage.py runserver"
echo ./python manage.py makemigrations & 
echo ./python manage.py migrate &
echo ./python manage.py runserver $1:8989 &



 
