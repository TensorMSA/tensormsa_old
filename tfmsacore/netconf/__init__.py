from .nn_common_manager import create_new_network, update_network,set_train_result,get_network_config, \
    filter_network_config,set_train_datasets, delete_net_info, get_net_summary
from .nn_config_manager import load_conf, save_conf, load_ori_conf, chk_conf, remove_conf
from .nn_model_manager import load_trained_data, save_trained_data, chk_trained_data,remove_trained_data
from .nn_format_manager import chk_format,load_format,load_ori_format,remove_format,save_format
from .nn_train_manager import get_train_acc,get_train_loss,post_train_acc,post_train_loss,delete_train_acc,delete_train_loss
from .nn_flag_manager import set_off_data,set_off_data_conf,set_off_net_conf,set_off_net_vaild,set_off_train,\
    set_on_data,set_on_data_conf,set_on_net_conf,set_on_net_vaild,set_on_train, set_on_eval,set_off_eval, get_thread_status
from .nn_items_manager import get_category_list, get_subcategory_list, get_namespace