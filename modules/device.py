import re
from ciscoconfparse import CiscoConfParse
from errors import errmsg


class device:
    '''Class VARS'''
    id = 0

    '''Error Message VARS'''
    __connect_err_msg__ = "Error: Be sure to run the connect() method first"
    __config_err_msg__ = "Error: Unable to get latest configuration"

    def __init__(self, mgmt_ip, username, password):
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password
        self.hostname = "{}@{}".format(self.username, self.mgmt_ip)
        self.dev_type = 'cisco_ios'
        self.status = False
        self.id += 1
        self.all_interface_list = []
        self.config = ""
        self.parsed_config = ""
        self.net_connect = []
        self.up_interface_list = list()

    @property
    def __name__(self):
        try:
            self.get_hostname()
            return self.hostname
        except Exception:
            errmsg.__name__err(self)

    def connect(self):

        # Opens and writes running config on local machine
        self.get_hostname()

    def send_command(self, command):
        ''' In order to send commands to a device, \
        the connect() Method must be initiated before this routine \
        will exectue'''

        if self.status is True:
        else:
            # print(self.__connect_err_msg__)
            print(errmsg.ConnectErrorMSG(self))

    def get_hostname(self):
        if self.status is True:
            self.send_command('show run | inc hostname')

            # creates RegEX to search for hostname
            pattern = re.compile('(?<=hostname ).*', re.I | re.M)
            for i in results:
                self.hostname = i
        else:
            print(errmsg.ConnectErrorMSG(self))

    def get_all_interfaces(self):
        if self.status is True:
            self.send_command("show run | inc interface")
            pattern = re.compile('(?<=^interface ).*', re.I | re.M)
            results = str(pattern.findall((self.ssh_output)))\
                .replace("\\r", "").split(",")
            self.all_interface_list = []
            for i in results:
                self.all_interface_list.append(i)
                # local_int = i
            self.all_int_count = len(self.all_interface_list)
        else:
            print(errmsg.ConnectErrorMSG(self))

    def get_up_interfaces(self):
        if self.status is True:
            self.send_command("show ip int br | inc up")
            pattern = re.compile(
                '(Vlan\d*|FastEthernet\d*/\d*/\d*|GigabitEthernet\d*/\d*/\d*|\
                loopback\*)', re.I | re.M)
            results = str(pattern.findall((self.ssh_output)))\
                .replace("\\r", "").split(",")

            for i in results:
                self.up_interface_list.append(i)
            self.up_int_count = len(self.up_interface_list)

        else:
            print(self.__connect_err_msg__)

    def get_cmd_results(self):
        try:
            return self.ssh_output
        except Exception:
            print(self.__connect_err_msg__)

    def get_config(self):
        if self.status is True:
            self.send_command("show run")
            self.parsed_config = CiscoConfParse(self.ssh_output.split())
        else:
            print(errmsg.ConnectErrorMSG(self))

    def set_hostname(self, hostname):
        self.hostname = hostname

    def list_interfaces(self):
        if len(self.all_interface_list) > 0:
            del self.all_interface_list[:]
            self.get_all_interfaces()
            return(self.all_interface_list)
        elif len(self.all_interface_list) == 0:
            print(errmsg.ListEmptyErrMsg(self))

    def __repr__(self):
        self.get_up_interfaces()
        return ("Device Stats:\n SSH connection: {3} \n Hostname: {0} \n \
        Managment IP: {1} \n User: {2}\n Interfaces: \n  {4}"
                .format(self.hostname,
                        self.mgmt_ip,
                        self.username,
                        self.status,
                        self.up_interface_list))

    class interface:
        id = 0

        def __init__(self, int_name):
            self.id += 1
            self.int_name = int_name

        def __repr__(self):
            return("Link Name: {0}").format(self.int_name)


def list_int(device):
    '''Main Routine for testing DEVICE class'''
    device.get_hostname()
    device.get_all_interfaces()
    print("\t{} Interface Informations: ".format(device.hostname))
    print("Int Count: {}".format(device.all_int_count))
    for i in device.all_interface_list:
        print(i)


def main():
    '''Main Routine for testing DEVICE class'''


__ver__ = "1.0"

if __name__ == '__main__':
    main()
