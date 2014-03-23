__author__ = 'vineeth'


def validate_common_data(node_name, run_list):
    if node_name is None:
        return False
    if run_list is None:
        return False
    return True


def validate_onprem_data(node_name, ip_address, run_list, username, password):
    if not validate_common_data(node_name, run_list):
        return False
    if ip_address is None:
        return False
    if username is None:
        return False
    if password is None:
        return False
    return True


def validate_cloud_data(node_name, access_key, secret_key, run_list, instance_type):
    if not validate_common_data(node_name, run_list):
        return False
    if access_key is None:
        return False
    if secret_key is None:
        return False
    if instance_type is None:
        return False