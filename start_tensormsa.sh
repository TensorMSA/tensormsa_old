if [ $# -eq 0 ]
  then
    echo "put your container id as parameter"
    exit 1
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

echo "======================="
echo "step1 : start postgresql"
echo "======================="

runuser -l postgres -c 'pg_ctl start'

echo "======================="
echo "step2 : start spark apps"
echo "======================="
 
sudo /home/dev/spark/sbin/stop-master.sh
sudo /home/dev/spark/sbin/start-master.sh
sudo /home/dev/spark/sbin/start-slave.sh spark://$1:7077

echo "======================="
echo "step3 : start Livy"
echo "======================="
 
cp /home/dev/spark/conf/spark-defaults.conf.template /home/dev/spark/conf/spark-defaults.conf
echo "spark.master       spark://$1:7077 " >> /home/dev/spark/conf/spark-defaults.conf


echo /home/dev/livy/bin/livy-server &
/home/dev/livy/bin/livy-server &



echo "======================="
echo "step4 : start Django"
echo "======================="

cd /home/dev/TensorMSA/
echo ./python manage.py makemigrations & 
python manage.py makemigrations &

echo ./python manage.py migrate &
python manage.py migrate &

echo ./python manage.py runserver $1:8989 &
python manage.py runserver $1:8989 &




 
