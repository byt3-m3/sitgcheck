

def ConnectErrorMSG(device):
    __connect_err_msg__ = "Error: unable command to Device {}\n \
Be sure to run the connect() method on object".format(device.mgmt_ip)
    return(__connect_err_msg__)


def ConfigErrMsg(device):
    __config_err_msg__ = "Error: Unable to get latest configuration from {}"\
        .format(device.mgmt_ip)
    return(__config_err_msg__)


def ListEmptyErrMsg(device):
    __ListEmptyErrMsg__ = "Error: List is empty, run get_all_int() func"
    return(__ListEmptyErrMsg__)


def __name__err(device):
    __name__err = "Not able to retrevie name of object for {}"\
        .format(device.mgmt_ip)
    return(__ListEmptyErrMsg__)
