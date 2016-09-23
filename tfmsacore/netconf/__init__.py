from .nn_common_manager import create_new_network, update_network,set_train_result,get_network_config, \
    filter_network_config,set_train_datasets
from .nn_config_manager import load_conf, save_conf, load_ori_conf, chk_conf, remove_conf
from .nn_data_manager import load_trained_data, save_trained_data, test_data_move, chk_trained_data,\
    remove_trained_data