from netmiko import ConnectHandler
import re
from ciscoconfparse import CiscoConfParse

# New Code addeds

# test tst


class device:
    '''Class VARS'''
    id = 0
    remote_conn = ""
    config = ""
    parsed_config = ""
    net_connect = []
    up_interface_list = list()
    all_interface_list = list()

    '''Error Message VARS'''
    __connect_err_msg__ = "Error: Be sure to run the connect() method first"
    __config_err_msg__ = "Error: Unable to get latest configuration"

    def __init__(self, mgmt_ip, username, password):
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password
        self.hostname = None
        self.dev_type = 'cisco_ios'
        self.status = False
        self.id += 1

    def connect(self):
        import paramiko
        import time

        cisco_dev = {
            'device_type': self.dev_type,
            'ip':   self.mgmt_ip,
            'username': self.username,
            'password': self.password,
            'port': 22,          # optional, defaults to 22
            'secret': 'secret',     # optional, defaults to ''
            'verbose': False,       # optional, defaults to False
        }
        self.net_connect = ConnectHandler(**cisco_dev)
        self.ssh_output = self.net_connect.send_command("show run")
        #self.config = self.ssh_output
        self.parsed_config = CiscoConfParse(self.ssh_output.split())
        self.status = True

    def send_command(self, command):
        ''' In order to send commands to a device, the connect() Method must be initiated before this routine will exectue'''
        if self.status == True:
            self.ssh_output = self.net_connect.send_command(command)
        else:
            print(self.__connect_err_msg__)

    def get_hostname(self):
        if self.status == True:
            self.send_command('show run | inc hostname')

            # creates RegEX to search for hostname
            pattern = re.compile('(?<=hostname ).*', re.I | re.M)
            results = pattern.findall(str(self.ssh_output))

            for i in results:
                self.hostname = i
        else:
            print(self.__connect_err_msg__)

    def get_all_interfaces(self):
        if self.status == True:
            local_int = []
            self.send_command("show run | inc interface")
            pattern = re.compile('(?<=^interface ).*', re.I | re.M)
            results = str(pattern.findall((self.ssh_output))).replace("\\r", "").split(",")
            del self.all_interface_list[:]

            for i in results:
                self.all_interface_list.append(i)
                #local_int = i
            self.all_int_count = len(self.all_interface_list)
        else:
            print(self.__connect_err_msg__)

    def get_up_interfaces(self):
        if self.status == True:
            self.send_command("show ip int br | inc up")
            #output = str(self.ssh_output)
            #pattern = re.compile('(FastEthernet*\d+/\d+/\d+|GigabitEthernet*\d+/\d+/\d+|Ethernet.\d+/\d+.\d+|Vlan\d+)', re.I|re.M)
            pattern = re.compile(
                '(Vlan\d*|FastEthernet\d*/\d*/\d*|GigabitEthernet\d*/\d*/\d*|loopback\*)', re.I | re.M)
            #results = pattern.findall(self.ssh_output.decode())
            results = str(pattern.findall((self.ssh_output))).replace("\\r", "").split(",")
            # print(self.ssh_output.decode())

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
        if self.status == True:
            self.send_command("show run")
            self.parsed_config = CiscoConfParse(self.ssh_output.split())
        else:
            print(self.__config_err_msg__)

    def set_hostname(self, hostname):
        self.hostname = hostname

    def list_interfaces(self):
        if len(self.all_interface_list) > 0:
            del self.all_interface_list[:]
            self.get_all_interfaces()

            print(self.all_interface_list)
            # for i in self.all_interface_list:
            #     x = i.replace("'", "").replace("["," ").replace("]"," ")
            #     self.interface(x)
            #     print("{}".format(x))
            #     # int_out = self.send_command("show run interface " + i.replace("'", ""))
            #     #self.send_command("show run interface {}".format(x))
            #     #print(self.ssh_output)
        else:
            print(self.__connect_err_msg__)

    def __repr__(self):
        self.get_up_interfaces()
        return ("Device Stats:\n SSH connection: {3} \n Hostname: {0} \n Managment IP: {1} \n User: {2}\n Interfaces: \n  {4}".format(self.hostname,
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

    sw1 = device("192.168.1.2", "cisco", "cisco")
    r1 = device("192.168.1.123", "cisco", "cisco")

    # sw1.connect()
    r1.connect()
    sw1.connect()

    list_int(r1)


if __name__ == '__main__':
    main()
