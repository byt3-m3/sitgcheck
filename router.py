import re

class device:
    
    dev_num = 0
    int_count = 0
    
    interface_list = list()
    def __init__(self, mgmt_ip, username, password):  
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password
        self.hostname = None
        self.dev_type = None
        self.description = None
        self.interfaces_list = list()
        
        device.dev_num += 1
      
    def send_command(self, command):
     #Importing paramiko and time modules for use within subroutine
     import paramiko
     import time

     #Creates the paramikoe SSHClient class
     remote_conn_pre=paramiko.SSHClient()

     #Adds remote host public to local host key database
     remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

     #Initiates the connection to remote device
     remote_conn_pre.connect(self.mgmt_ip, username=self.username, password=self.password, look_for_keys=False, allow_agent=False)

     #Invokes the ssh paramiko shell
     remote_conn = remote_conn_pre.invoke_shell()

     print "Interactive SSH session established to " + self.mgmt_ip + " with Username:" + self.username
     remote_conn.send("terminal monitor\n")
     remote_conn.send("terminal length 0\n")
     remote_conn.send(command + "\n")
     time.sleep(3)

     global ssh_output
     global ssh_file

     ssh_output = remote_conn.recv(100000)
     ssh_file = open("ssh_output.txt", "w+")
     ssh_file.write(ssh_output)
     print "Command output stored in variable 'ssh_output'"
     print "Results:" + ssh_output

    def pull_hostname(self):
        connect_ssh(self.mgmt_ip, self.username, self.password, 'show run | inc hostname ')

        #creates RegEX to search for hostname
        pattern = re.compile('(?<=hostname ).*', re.I|re.M)
        results = pattern.findall(ssh_output)

        #pops first item from results
        results.pop(0)

        #iterates and assinges the value of i to the hostname attribute
        for i in results:
         self.hostname = i
                
    def pull_interfaces(self):
       
    
            try:
                connect_ssh(self.mgmt_ip, self.username, self.password, 'show ip int br')
                
                pattern = re.compile('(FastEthernet*\d+/\d+/\d+|GigabitEthernet*\d+/\d+/\d+|Ethernet.\d+/\d+.\d+|Vlan\d+)', re.I|re.M)
                results = pattern.findall(ssh_output)
                
                for i in results:
                    self.interface_list.append(i)
                    
                self.int_count = len(self.interface_list)
                
                print "{} Interfaces detected".format(len(self.interface_list))                             
            except Exception:
                print "Could not connect"
                return 0
            
                pattern = re.compile('(FastEthernet*\d+/\d+/\d+|GigabitEthernet*\d+/\d+/\d+|Ethernet.\d+/\d+.\d+|Vlan\d+)', re.I|re.M)
                results = pattern.findall(ssh_output)
                
                for i in results:
                    device.interface_list.append(i)
                    
    def __repr__(self):
        return ("\n Hostname:{} \n Managment IP: {} \n User: {}".format(self.hostname,
                                                                        self.mgmt_ip,
                                                                        self.username))

    class interface:
        link_count = 0 
        interface_list = list()
        
        def __init__(self, link_id):
            self.link_id = link_id
            device.interface.link_count += 1
            
        def set_ip(self, ip_addr):
            self.ip_addr = ip_addr 
            
        def set_mask(self, net_mask):
            self.net_mask = net_mask
        
        def set_desc(self, description):
            self.description = description
            
        def set_speed(self, speed):
            self.speed = speed
            
        def set_duplex(self, duplex):
            self.duplex = duplex
            
        def get_ip(self):   
            return self.ip_addr
        
        def get_mask(self):
            return self.net_mask
        
        def get_desc(self):
            return self.description
        
        def get_linkid(self):
            return self.link_id
        
        def get_speed(self):
            return self.speed
        
        def get_duplex(self):
            return self.duplex
       
        def __repr__(self):
            return("\nInterface {} \n Description: {} \n IP Addr: {} netmask: {} \n Speed:{}Mbps    Duplex:{}".format(self.get_linkid(), 
                                                                                                    self.get_desc(), 
                                                                                                    self.get_ip(), 
                                                                                                    self.get_mask(), 
                                                                                                    self.get_speed(),
                                                                                                    self.get_duplex()
                                                                                                    )
                   )
class router(device):
    pass
class switch(device):
    pass
class iou(device):
    def set_int(self):
        self.int_type = ("Ethernet", "Vlan", "Port-Channel")



def connect_ssh(ip, username, password, command):


 #Importing paramiko and time modules for use within subroutine
 import paramiko
 import time

 #Creates the paramikoe SSHClient class
 remote_conn_pre=paramiko.SSHClient()

 #Adds remote host public to local host key database
 remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

 #Initiates the connection to remote device
 remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

 #Invokes the ssh paramiko shell
 remote_conn = remote_conn_pre.invoke_shell()

 #print "Interactive SSH session established to " + ip + " with Username:" + username
 remote_conn.send("terminal monitor\n")
 remote_conn.send("terminal length 0\n")
 remote_conn.send(command + "\n")
 time.sleep(3)

 global ssh_output
 global ssh_file

 ssh_output = remote_conn.recv(100000)
 ssh_file = open("ssh_output.txt", "w+")
 ssh_file.write(ssh_output)
 #print "Command output stored in variable 'ssh_output'"
 #print "Results:" + ssh_output

def get_cdp_neighbors(router):
 command = "show cdp neighbor detail"
 connect_ssh(r1.mgmt_ip, r1.username, r1.password, command)
 device_pattern = re.compile('(?<=Device ID:).*', re.I|re.M)
 cdp_ip_pattern = re.compile('(^Management address....).*(\n  IP address:.*)', re.I|re.M)
 results = device_pattern.findall(ssh_output) + cdp_ip_pattern.findall(ssh_output)


#print mgmt_int['ip_address']
#print str(eth001)
#for ip, value in interface.items():
#    print(ip, value)


def main():
    
 bits_core_sw1 = device('192.168.1.2', 'cbaxter', 'pimpin12')
 bits_core_eth0 = bits_core_sw1.interface("eth0/0")
 bits_core_eth1 = bits_core_sw1.interface("eth0/1")
 bits_core_sw2 = device('192.168.1.2', 'cbaxter', 'pimpin12')

 CORE_R1 = device('10.0.0.1', 'cisco', 'cisco')   
 CORE_R1_eth0 = CORE_R1.interface("eth0/0/0")

 bits_core_eth0.set_ip("192.168.1.1")
 bits_core_eth0.set_mask("255.255.255.0")
 bits_core_eth0.set_desc("Link to Router 1")
 bits_core_eth0.set_speed("100")
 bits_core_eth0.set_duplex("Full")
 #bits_core_sw1.send_command("show ip route")
 bits_core_sw1.pull_hostname()
 bits_core_sw1.pull_interfaces()

 print bits_core_sw1.int_count
 #print bits_core_links.link_count
  #print ("Interface {} \n Description: {} \n IP Addr: {} netmask: {}".format(CORE_R1_eth0.get_linkid(), CORE_R1_eth0.get_desc(), CORE_R1_eth0.get_ip(), CORE_R1_eth0.get_mask()))


if __name__ == '__main__':
    main()
