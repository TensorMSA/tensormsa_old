echo "======================="
echo "Starting TensorMSA !!!!"
echo "======================="

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

echo "==========================================="
echo "step1 : start postgresql"
echo "==========================================="

runuser -l postgres -c 'pg_ctl start'

echo "==========================================="
echo "step2 : start spark apps"
echo "==========================================="

sudo /home/dev/spark/sbin/start-master.sh &
sudo /home/dev/spark/sbin/start-slave.sh spark://${LOC}:7077 -m 6G -c 2
#sudo /home/dev/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://${loc}:7077 -m 6G -c 2 &
#sudo /home/dev/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://${loc}:7077 -m 3G -c 1 &

echo "==========================================="
echo "step3 : Skip Livy (Not use any more)       "
echo "==========================================="
 
#cp /home/dev/spark/conf/spark-defaults.conf.template /home/dev/spark/conf/spark-defaults.conf
#echo "spark.master       spark://$loc:7077 " >> /home/dev/spark/conf/spark-defaults.conf
#echo /home/dev/livy/bin/livy-server &
#/home/dev/livy/bin/livy-server &

echo "==========================================="
echo "step4 : Set HDFS Server Info      "
echo "==========================================="
#if [ $TYPE -eq  1 ]
#  then
#    cp /root/.hdfscli_temp.cfg /root/.hdfscli.cfg
#    echo "[global]"   >>  /root/.hdfscli.cfg
#    echo "default.alias = dev"   >>  /root/.hdfscli.cfg
#    echo "[dev.alias]"   >>  /root/.hdfscli.cfg
#    echo "url = http://${HDFS}:50070"   >>  /root/.hdfscli.cfg
#    echo "[prod.alias]"   >>  /root/.hdfscli.cfg
#    echo "url = http://${HDFS}:50070"   >>  /root/.hdfscli.cfg
#fi

echo "==========================================="
echo "step5 : Django Settings      "
echo "==========================================="

cd /home/dev/TensorMSA/
echo python manage.py makemigrations &
python manage.py makemigrations &

echo python manage.py migrate &
python manage.py migrate &

echo python manage.py collectstatic --noinput -i admin -i node_modules
python manage.py collectstatic --noinput -i admin -i node_modules  &

echo webpack
cd /home/dev/TensorMSA/tfmsaview/static
npm install
webpack

echo "==========================================="
echo "step6 : Start TensorMSA Webserver      "
echo "==========================================="

echo ./python manage.py runserver $HOSTNAME:8989 &
cd /home/dev/TensorMSA/
python manage.py runserver $HOSTNAME:8989 &




 
