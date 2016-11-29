#define Job types
JOB_TYPE_WDNN_TRAIN = '1'
JOB_TYPE_CNN_TRAIN = '2'
JOB_TYPE_WDNN_EVAL = '3'
JOB_TYPE_CNN_EVAL = '4'
MAX_JOB_CAPA = '2'

#define Store types
DATA_STORE_TYPE_HBASE = '1'
DATA_STORE_TYPE_IMAGE = '2'
DATA_STORE_TYPE_S3 = '3'
DATA_STORE_TYPE_LOCAL = '4'

#log_mode
LOG_MODE = True

#data & preprocess type
TYPE_DATA_FRAME = '1'
TYPE_IMAGE = '2'
TYPE_TEXT = '3'

#monitor - loss
LOG_OUT_STEPS = 50
#monitor - acc
ACC_OUT_STEPS = 30

#test data portion
TEST_DATA_PORTION = 0.2
TRAIN_DATA_PORTION = 0.8