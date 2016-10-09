echo "======================="
echo "Starting TensorMSA !!!!"
echo "======================="

echo "[A] set up server info"
echo "location : /home/dev/TensorMSA/TensorMSA/setting.py"
echo "[B] First Param : choose data source types"
echo "- 1) HDFS - SPARK"
echo "- 2) HDFS - HIVE - SPARK"
echo "- 3) S3 - SPARK"
echo "- 4) LOCAL - SPARK"
echo "[C] Second Param : "
echo "- 1) HDFS - SPARK : IP:PORT of HDFS "
echo "- 2) HDFS - HIVE - SPARK : on development" 
echo "- 3) S3 - SPARK : on development "
echo "- 4) LOCAL - SPARK : no parm needed" 
echo "[D] more info :  http://github.com/tensormsa"

if [ $# -lt 1 ]
  then
    echo "======================="
    echo "[Parameter Error]      "
    echo "======================="

    echo "[ERROR : select Data Source Mode]"
    echo "choose data souce type"
    echo "[First parm] : data source mode "
    echo "- 1 : HDFS - SPARK"
    echo "- 2 : HDFS - HIVE - SPARK"
    echo "- 3 : S3 - SPARK"
    echo "- 4 : LOCAL - SPARK"
    echo "Select Type [1 ~ 4] : "
    read TYPE
    echo "Insert Your Container ID(or IP)"
    read LOC
fi


if [ $TYPE -eq 1 ]
  then 
    echo "Insert HDFS Container ID(or IP)"
    read HDFS
fi 

if [ $TYPE -eq 2 ]
  then 
    echo "HIVE mode not supported yet"
    exit 1
fi 

if [ $TYPE -eq 3 ]
  then
    echo "S3 mode not supported yet"
    exit 1
fi

if [ $TYPE -eq 4 ]
  then
    echo "[WARNING] Local mode store all data on local disk"
fi


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
if [ $TYPE -eq  1 ]
  then
    cp /root/.hdfscli_temp.cfg /root/.hdfscli.cfg
    echo "[global]"   >>  /root/.hdfscli.cfg
    echo "default.alias = dev"   >>  /root/.hdfscli.cfg
    echo "[dev.alias]"   >>  /root/.hdfscli.cfg
    echo "url = http://${HDFS}:50070"   >>  /root/.hdfscli.cfg
    echo "[prod.alias]"   >>  /root/.hdfscli.cfg
    echo "url = http://${HDFS}:50070"   >>  /root/.hdfscli.cfg
fi

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

echo ./python manage.py runserver ${LOC}:8989 &
cd /home/dev/TensorMSA/
python manage.py runserver ${LOC}:8989 &




 
