echo "======================="
echo "set path, env variables"
echo "======================="

source ~/.bashrc
export PATH="/root/anaconda3/bin:$PATH"
source ~/anaconda3/bin/activate ~/anaconda3/
export PATH="/home/dev/java/bin:$PATH"
export SPARK_HOME=/home/dev/spark
export HADOOP_CONF_DIR=/home/dev/hadoop/conf
export M2_HOME=/usr/local/maven
export PATH=${M2_HOME}/bin:${PATH}

echo $SPARK_HOME
echo $HADOOP_CONF_DIR
echo $M2_HOME

echo "======================="
echo "step3 : stop Django"
echo "======================="

cd /home/dev/TensorMSA/
pkill -f "uwsgi"
pkill -f "nginx"
