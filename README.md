# TensorMSA : Tensorflow Micro Service Architecture 
<b>1.TensorMSA </b> </br>
   - Tensor Micro Service Architecture is a project started to make TensorFlow more accessable from Java legacy systems
   with out modifying too much source codes. 

<b>2. Function </b></br>
   - REST APIs corresponding to Tensorflow 
   - JAVA API component interface with python REST APIS inside
   - Easy to use UI component provide NN configuration, train remotly, save & load NN models, handling train data sets
   - Train NN models via Spark cluster supported 
   
<b>3. Schedule </b></br>
   - We just started this projects (2016.8)
   - We are still on research process now
   - Expected to release first trial version on December 2016 
</br>

# Overview
Like described bellow, purpose of this project is provide deep learning management system via rest service so that non 
python legacy systems can use deep learning effectivly 
<p align="center">
  <img src="https://raw.githubusercontent.com/seungwookim/TensorMSA/master/ProjectDesc2.png" width="750"/>
</p>

# Install
*[install guide here](http://hugrypiggykim.com/2016/09/03/python-tensorflow-django-%ea%b0%9c%eb%b0%9c%ed%99%98%ea%b2%bd-%ea%b5%ac%ec%b6%95-%ec%a2%85%ed%95%a9/)*.
<b>1.Install Anaconda </b> </br>
   - download Anaconda :  https://www.continuum.io/downloads
   - install (be assure anaconda works as default interpreter) 
   '''
    bash /home/user/Downloads/Anaconda2-4.1.1-Linux-x86_64.sh
   '''
   '''
    vi ~/.bashrc
    export PATH="$HOME/anaconda2/bin;$PATH"
   '''

<b>2.Install Tensorflow</b> </br>
   - install Tensorflow using conda 
   '''
    $ conda create -n tensorflow python=2.7
    $ source activate tensorflow
    $ conda install -c conda-forge tensorflow
   '''

<b>3.Install Django</b> </br>
   - install Tensorflow using conda 
   '''
    [Django]
    conda install -c anaconda django=1.9.5
    [Django Rest Frame Work]
    conda install -c ioos djangorestframework=3.3.3
    [postgress plugin]
    conda install -c anaconda psycopg2=2.6.1
    [pygments]
    conda install -c anaconda pygments=2.1.3
   '''

<b>4.Install Postgresql</b> </br>
   - install Tensorflow using conda 

[install]
'''
    yum install postgresql-server
'''
[check account and set pass]
'''
    cat /etc/passwd | grep postgres
     sudo passwd postgres
'''
[check PGDATA]
'''
    cat /var/lib/pgsql/.bash_profile
     env | grep PGDATA
'''
[init and run]
'''
    sudo -i -u postgres
    initdb
    pg_ctl start
    ps -ef | grep postgress
'''
[connect and create database]
'''
    # psql
    postgres=# create database test1  ;
    postgres=# select *   from pg_database  ;
'''    
[create user for TesorMsA]
'''
    postgres=#CREATE USER testuser WITH PASSWORD '1234';
    postgres=#ALTER ROLE testuser SET client_encoding TO 'utf8'; 
    postgres=#ALTER ROLE testuser SET default_transaction_isolation TO 'read committed'; postgres=#ALTER ROLE testuser SET timezone TO 'UTC';
    postgres=#GRANT ALL PRIVILEGES ON DATABASE test1 TO testuser;
'''

<b>5.get TensorMSA form git</b> </br>
'''
   git clone 
'''

<b>5.migrate database</b> </br>
get to project folder where you can see 'manage.py'
'''
   python manage.py makemigrations 
   python manage.py migrate
'''

<b>6.run server</b> </br>
run server with bellow command
'''
   ip addr | grep "inet "
   python manage.py runserver localhost:8989
'''

# REST API / JAVA API Documents (yet)

