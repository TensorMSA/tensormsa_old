from .nn_common_manager import create_new_network, update_network,set_train_result,get_network_config, \
    filter_network_config,set_train_datasets, delete_net_info
from .nn_config_manager import load_conf, save_conf, load_ori_conf, chk_conf, remove_conf
from .nn_model_manager import load_trained_data, save_trained_data, chk_trained_data,remove_trained_data
from .nn_format_manager import chk_format,load_format,load_ori_format,remove_format,save_format
from .nn_train_manager import get_train_acc,get_train_loss,post_train_acc,post_train_loss