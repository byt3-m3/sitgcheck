from ciscoconfparse import CiscoConfParse
import sys, getopt
import re
import paramiko



class device:
    #Class Variables 
    dev_num = 0
    int_count = 0
    interface_list = list()
    remote_conn_pre = paramiko.SSHClient()
    remote_conn = None
    #ssh_output = None

    def __init__(self, mgmt_ip, username, password):  
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password
        self.hostname = None
        self.dev_type = None
        self.description = None
        self.interfaces_list = list()
        self.status = False
        
        device.dev_num += 1
     
    def connect(self):
     import paramiko  
     import time  
     #Creates the paramikoe SSHClient class
      
     remote_conn_pre=paramiko.SSHClient()

     #Adds remote host public to local host key database
     remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

     #Initiates the connection to remote device
     remote_conn_pre.connect(self.mgmt_ip, username=self.username, password=self.password, look_for_keys=False, allow_agent=False)
     #Invokes the ssh paramiko shell
     global remote_conn
     remote_conn = remote_conn_pre.invoke_shell()
     self.status = True
 
    def send_command(self, command):
     #Importing paramiko and time modules for use within subroutine
     import paramiko
     import time
     
     ''' In order to send commands to a device, the connect() Method must be initiated before this routine will exectue'''
     if self.status == True:
      remote_conn.send("terminal monitor\n")
      remote_conn.send("terminal length 0\n")
      remote_conn.send(command + "\n")
      time.sleep(5)
      self.ssh_output = remote_conn.recv(1000000000)
      #ssh_file = open("ssh_output.txt", "w+")
      #ssh_file.write(ssh_output)
      #ssh_file.close
     else:
       print("Must use the self.connect() method before sending commands")

    def pull_hostname(self):
        connect_ssh(self.mgmt_ip, self.username, self.password, 'show run | inc hostname ')

        #creates RegEX to search for hostname
        pattern = re.compile('(?<=hostname ).*', re.I|re.M)
        results = pattern.findall(ssh_output)
        print(ssh_output) 
        print(results)
        #pops first item from results
        results.pop(0)

        #iterates and assinges the value of i to the hostname attribute
        for i in results:
         self.hostname = i
                
    def pull_interfaces(self):
            if self.status == True:
                self.send_command("show run | inc interface")
                #output = str(self.ssh_output)
                #pattern = re.compile('(FastEthernet*\d+/\d+/\d+|GigabitEthernet*\d+/\d+/\d+|Ethernet.\d+/\d+.\d+|Vlan\d+)', re.I|re.M)
                pattern = re.compile('(?<=^interface ).*', re.I|re.M)
                #results = pattern.findall(self.ssh_output.decode())
                results = str(pattern.findall((self.ssh_output.decode()))).replace("\\r", "").split(",")

                for i in results:
                 self.interface_list.append(i)                 
                self.int_count = len(self.interface_list)
                          
            else:
                print("Could not connect") 
               # print(self.ssh_output)
                return 0

                    
    def get_cmd_results(self):
      return ssh_output

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

#CAT 1 VARs
#Network devices must be password protected, VulnID V-3012
NET0230=["V-3012","login ."]
#Group accounts must not be configured for use on the network device. not possible on IOS device** -- Needs Attention
NET0460=["V-3056"]
#The network element must be configured to ensure passwords are not viewable when displaying configuration information. must use "show run all" on cisco devices to check
NET0600=["V-3062", "^service password-encryption"]
#Network devices must not have any default manufacturer passwords, Not possible on cisco devcies
NET0240=["V-3143","password cisco"]
#the network devices must require authentication prior to establishing a management connection for administrative access.
NET1636=["V-3175","login ."]
 #The network device must use SNMP Version 3 Security Model with  FIPS 140-2 validated cryptography for any SNMP agent configured on the device.
NET1660=["V-3196","sha", "aes"]
#The network device must not use the default or well-known SNMP community strings public and private.
NET1665=["V-3210","snmp-server community public\n", "snmp-server community private\n"]
#The network device must require authentication for console acces
NET1623=["V-4582","login authentication"]
#The switch must be configured to use 802.1x authentication on host facing access switch ports.
NET_NAC_009=["V-5626","dot1x fallback", "dot1x host-mode", "dot1x port-control force-authorized"]
#The emergency administration account must be set to an appropriate authorization level to perform necessary administrative functions when the authentication server is not online.
NET0441=["V-15434","username"]


#Subroutines for  STIG Checks
def connect_ssh(ip, username, password, command):
 #Importing paramiko and time modules for use within subroutine
 import paramiko
 import time
 global ssh_output
 #Creates the paramikoe SSHClient class
 remote_conn_pre=paramiko.SSHClient()

 #Adds remote host public to local host key database
 remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

 #Initiates the connection to remote device
 remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

 #Invokes the ssh paramiko shell
 remote_conn = remote_conn_pre.invoke_shell()

 print("Interactive SSH session established to " + ip + " with Username:" + username) 
 remote_conn.send("terminal monitor\n")
 remote_conn.send("terminal length 0\n")
 remote_conn.send(command + "\n")
 time.sleep(3)
 ssh_output = remote_conn.recv(100000)
 ssh_file = open("ssh_output.txt", "w+")
 ssh_file.write(ssh_output)


def check_net0230(PARSED_CONFIG):
 #Subroutine to Validate Password protected vty and console access
 net0230_line_config = PARSED_CONFIG.find_parents_wo_child("^line", NET0230[1] )

 if net0230_line_config:
  print("NET0230 Results: \"Network devices must be password protected\" \n" + (" fix " + NET0230[0] + " in {1} \n"  + " {0}" ).format(" {0}".format("  ".join(str(i) for i in net0230_line_config)), config.name))  
 else:
  print("NET0230:\n No violations detected") 

def check_net0600(PARSED_CONFIG):
 #Subroutine to Validate service password-encryption
 pattern = re.compile("no service password-encryption", re.I|re.M)

 net0600_config = PARSED_CONFIG.find_lines(pattern)
 
 if len(net0600_config) == 0:
  print("NET0600\n No violations detected") 
 else:
  print("NET0600: " + NET0600[0] + " Results: \"passwords are viewable when displaying configuration information\" \n" + (" enable 'service password-encryption'"  + " in" + " {1} \n").format(net0600_config, config.name))  

def check_net1636(PARSED_CONFIG):
 #Subroutine to Validate Password protected vty and console access
 net1636_line_config = PARSED_CONFIG.find_parents_wo_child("^line", NET1636[1] )

 if net1636_line_config:
  print("NET1636 Results: \"network devices must require authentication\" \n" + (" fix " + NET1636[0]  + " in {1} \n" + " {0}").format(" {0}".format("  ".join(str(i) for i in net1636_line_config)), config.name))  
 else:
  print("NET1636:\n No violations detected") 

def check_net1660(device):
 #opening SNMP results file
 command =  "show snmp user"
 device.connect
 device.send_command(command)

 config = open("net1660.conf", "w")
 config.write(ssh_output)
 config.close()

 parse_config("net1660.conf")
 snmp_show_results = open("net1660.conf", "r")
 snmp_show_results_str = str(snmp_show_results.readlines())

 #REGEX to find violating config for SNMP
 AES_REG_A = re.findall("3DES|DES|MD5|User name.*?,", snmp_show_results_str)

 #SNMP violation count
 COUNT_MD5 = AES_REG_A.count("MD5")
 COUNT_DES = AES_REG_A.count("DES")
 COUNT_3DES = AES_REG_A.count("3DES")
 NET1660_VIOLATION =  COUNT_3DES + COUNT_MD5 + COUNT_DES

 #Looking for SNMP version 1 and 2c related configuration
 parse = CiscoConfParse(snmp_show_results)
 snmp_lines = parse.find_lines("(snmp-server.(user|group).*v(1|2))|(snmp-server community.*)")


 #Conditional to validate if device is using FIP-140-2 compliant SNMPv3 deployment and no SNMPv2 is being utilized
 if NET1660_VIOLATION > 0 or snmp_lines :
  print("NET1660 " + NET1660[0] + " Results: \"SNMPv3 must only Use SHA and AES\" \n" + " Execute 'show snmp user' on system") 
  print(" ") 
  print("NET1660 " + NET1660[0] + " Results: \"SNMPv1 and SNMPv2 must not be used\" \n " +   "{0}").format(" ".join(str(i) for i in snmp_lines))
 else:
  print("NET1660:\n no violations detected") 

def check_net1665(PARSED_CONFIG):
 #Extracts SNMP configuration, the re.complie, uses the re compile functon to create a REGEX pattern to be used with cisco conf parse
 snmp_pattern = re.compile("snmp-server.community.(public|private)", re.I|re.M)

 net1665_config_lines = PARSED_CONFIG.find_lines(snmp_pattern)

 #Stores Human Readable List in VAR
 net1665_config = "{0}".format("   ".join(str(i) for i in net1665_config_lines))

 #Conditional to test if  the private or public communty is there
 if len(net1665_config_lines) > 0:
  print("\nNET1665 Results: \"Device must not use the default or well-known SNMP community strings public and private.\" \n  Remidiation  for" + NET1665[0] +  ": \n  Remove lines: \n   {0}").format(net1665_config)
 else:
  print("NET1665:\n No violations detected") 

def check_net1623(PARSED_CONFIG):
 pattern = re.compile("(login.authentication..[a-z]?)", re.I|re.M)
 
 net1623_config_list = PARSED_CONFIG.find_parents_wo_child('^line con.[0-9]', pattern)
 
 #Stores Human Readable List in VAR
 net1623_config = "{0}".format("   ".join(str(i) for i in net1623_config_list))
 
 if len(net1623_config_list) > 0:
  print ("\nNET1623 Results: 'Network device must require authentication for console access' \n Please enable authentication for the following lines: \n   {}").format(net1623_config)
 else:
  print("NET1623:\n No violations detected") 

def parse_config(FILE):
 #opening Text File
 filename = "./" + FILE
 config = open(FILE, "r")
 #Creatting CiscoConfParse  obj.
 parse = CiscoConfParse(config)

def results(DEVICE):
  #Generates generic Results Method or Main Routine
  print("\t\tResults for {}").format(DEVICE.mgmt_ip) 



#subroutine to test STIG checks

def test_sub(device, conf_file):
    import paramiko
    command =  "show run"
    global config
    #Tries to connect to SSH
    try:
        connect_ssh(device.mgmt_ip, device.username, device.password, command)
        config = open("ssh_config.conf", "w")
        config.write(ssh_output)
        config.close()
        config = open("ssh_config.conf", "r")
        parse = CiscoConfParse(config)
        #subroutine to check
        check_net1660(device)
        check_net0230(parse)
        check_net0600(parse)
        check_net1636(parse)
        check_net1665(parse)
        check_net1623(parse)

        return 1
    #Execption if SSH fails
    except paramiko.ssh_exception.NoValidConnectionsError as err:
        print(err) 
    #Opens Locally Specefied file
        config_file = conf_file
        parse_config(config_file)
        #subroutine to check
        check_net1623(parse)
        check_net0230(parse)
        check_net0600(parse)
        return

def check_net0441(device):
 #user_pattern = re.compile("^username.*.secret|password", re.I|re.M)
 user_pattern = re.compile("username(?=.*privilege)", re.I|re.M)
 aaa_pattern = re.compile("^aaa.authentication.login.*local\\r\\n", re.I|re.M)
 #aaa_pattern = re.compile("(?=authentication).*local$", re.I|re.M)
 #aaa_pattern = re.compile("local\\r\\n", re.I|re.M)

 device.send_command("show run | inc ^username \n show run | inc aaa authentication")
 results =  device.ssh_output.decode()
 #user_final =  user_pattern.findall(device.ssh_output.decode())

 
 aaa_final =  aaa_pattern.findall(results)

 print(aaa_final)

 #if "secret" in str(user_final):
 #print("It works")




def main():


 #config = None
 #ssh_file = None

 sw1 = device("192.168.1.2", "cisco", "cisco")
 r1 = device("192.168.1.123", "cisco", "cisco")

 sw1.connect()
 #sw1.pull_interfaces()
 #print(sw1.interface_list)
 #print(dir(r1))

 #r1.send_command("show ip route")
 #cmd =  r1.get_cmd_results()

 #test_sub(sw1, "test.conf")
 check_net0441(sw1)



if __name__ == '__main__':
 main()