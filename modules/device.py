# from netmiko import ConnectHandler
import re
from ciscoconfparse import CiscoConfParse
import errmsg
import paramiko


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
        self.remote_conn = paramiko.channel
        self.config = ""
        self.parsed_config = ""
        self.net_connect = []
        self.up_interface_list = list()
        self.ssh_out = []

    @property
    def __name__(self):
        try:
            self.get_hostname()
            return self.hostname
        except Exception:
            errmsg.__name__err(self)

    def open_file(self):
        self.running_config = open("./configs/{}_running_config.cfg"
                                   .format(self.mgmt_ip), "w")

    def read_file(self):
        self.running_config = open("./configs/{}_running_config.cfg"
                                   .format(self.mgmt_ip), "r")

    def close_file(self):
        self.running_config.close()

    def connect(self):

        self.remote_conn_pre = paramiko.SSHClient()
        self.remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.remote_conn_pre.connect(self.mgmt_ip, username=self.username,
                                     password=self.password, look_for_keys=False,
                                     allow_agent=False)

        self.status = True
        self.send_command("show run\r")

        # Opens and writes running config on local machine

        self.open_file()
        self.running_config.write(self.ssh_out)
        self.close_file()

        self.read_file()
        self.parsed_config = CiscoConfParse(self.running_config)
        self.get_hostname()
        self.close_file()

    def init_ses(self):
        self.remote_conn_pre = paramiko.SSHClient()
        self.remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.remote_conn_pre.connect(self.mgmt_ip, username=self.username,
                                     password=self.password, look_for_keys=False,
                                     allow_agent=False)

        self.status = True

    def send_command(self, command):
        ''' In order to send commands to a device, \
        the connect() Method must be initiated before this routine \
        will exectue'''
        self.max_buff = 65535
        self.init_ses()
        if self.status is True:
            self.stdin, self.stdout, self.stderr = self.remote_conn_pre.exec_command(command)
            self.ssh_out = self.stdout.read()
            # return self.ssh_out
        else:
            # print(self.__connect_err_msg__)
            print(errmsg.ConnectErrorMSG(self))

    def get_hostname(self):
        if self.status is True:
            # self.send_command('show run | inc hostname')
            self.read_file()
            # creates RegEX to search for hostname
            pattern = re.compile('(?<=hostname ).*', re.I | re.M)
            # results = self.parsed_config.find_lines(pattern)
            results = pattern.findall(self.running_config.read())
            for i in results:
                self.hostname = i
        else:
            print(errmsg.ConnectErrorMSG(self))

    def get_neighbors(self):
        """ Returns a list of dicts of the switch's neighbors:
            {hostname, ip, local_port, remote_port} """

        re_text = "-+\r?\nDevice ID: (.+)\\b\r?\n.+\s+\r?\n\s*IP address:\s+(\d+\.\d+\.\d+\.\d+)\s*\r?\n.*\r?\nInterface: (.+),.+Port ID.+: (.+)\\b\r?\n"

        self.send_command("show cdp neighbors detail")

        self.neighbors = list()
        for neighbor in re.findall(re_text, self.ssh_out):
            n_dict = dict()

            n_dict['hostname'], n_dict['ip'], n_dict['local_port'], n_dict['remote_port'] = neighbor

            self.neighbors.append(n_dict)

        return self.neighbors

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
        self.read_file()
        try:
            return self.running_config.readlines()
        except Exception:
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


def connect_ssh(ip, username, password, command):
 # Importing paramiko and time modules for use within subroutine
    import paramiko
    import time
    # Creates the paramikoe SSHClient class
    remote_conn_pre = paramiko.SSHClient()

    # Adds remote host public to local host key database
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Initiates the connection to remote device
    remote_conn_pre.connect(ip, username=username, password=password,
                            look_for_keys=False, allow_agent=False)

    # Invokes the ssh paramiko shell
    remote_conn = remote_conn_pre.invoke_shell()


def main():
    '''Main Routine for testing DEVICE class'''


__ver__ = "1.0"

if __name__ == '__main__':
    main()
