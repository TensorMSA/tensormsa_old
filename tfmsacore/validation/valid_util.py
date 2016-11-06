
def cal_cnn_matrix_size(curren_matrix, padding, max_pool_stride):
    if (padding == 'SAME'):
        curren_matrix[0] = int(curren_matrix[0] / max_pool_stride[0])
        curren_matrix[1] = int(curren_matrix[1] / max_pool_stride[1])
    else:
        curren_matrix[0] = int(curren_matrix[0] / max_pool_stride[0] - 1)
        curren_matrix[1] = int(curren_matrix[1] / max_pool_stride[1] - 1)
    return curren_matrix