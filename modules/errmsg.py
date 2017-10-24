

def ConnectErrorMSG(device):
    __connect_err_msg__ = "Connection Error:\n unable command to Device {0} with username {1}".format(
        device.mgmt_ip, device.username)
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


def main():
    '''Main Routine for l2stig checks'''


__ver__ = "1.0"

if __name__ == '__main__':
    main()
