

def make_output_matrix(index_list, target_data):
    """
    return tensorflow acceptable output list
    :param index_list:
    :param target_data:
    :return:
    """
    output_list = []
    for data in index_list:
        if(target_data == data):
            output_list.append(1)
        else:
            output_list.append(0)

    return output_list

def return_index_position(index_list, target_data):
    """
    return tensorflow acceptable output list
    :param index_list:
    :param target_data:
    :return:
    """
    if (target_data in index_list) :
        return index_list.index(target_data)
    else:
        return 0

def convert_to_index(index_list):
    """
    return tensorflow acceptable output list
    :param index_list:
    :param target_data:
    :return:
    """
    return_list = []
    for value in index_list :
        return_list.append(index_list.index(value))

    return return_list