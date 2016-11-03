

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
    return index_list.index(target_data)