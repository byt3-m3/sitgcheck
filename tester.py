from modules.device import device as dev
from modules import l2stig as stig
import os

<<<<<<< HEAD
os.system("clear")
sw1 = device("192.168.1.2", "cisco1", "cisco1", enable_pass="cisco")
sw2 = device("192.168.1.2", "cisco", "cisco", enable_pass="cisco")
=======
if "nt" in os.name:
    os.system("cls")
else:
    os.system("clear")

# sw1 = dev("192.168.1.2", "cisco", "cisco", enable_pass="cisco")
# sw2 = dev("10.0.100.13", "cisco", "cisco", enable_pass="cisco")
sw3 = dev("10.0.100.3", "cisco", "cisco", enable_pass="cisco")
>>>>>>> 3882a36e2f6838cb7bc3149577eabedc85c79ed4
# sw2 = router("192.168.1.250", "cisco", "cisco")
# r1 = router("192.168.1.123", "c0isco", "cisco")
#

ip_list = ['192.168.1.250', '192.168.1.11']

<<<<<<< HEAD

def create_dev(ip_addr, username, password, **kwargs):
    devices = list()
    print("""\tPLease Wait While devices are being created
    """)
    for ip in ip_addr:
        devices.append(device(ip, "cisco", "cisco", enable_pass="cisco"))

    for dev in devices:
        print(dev.get_run())


def test_stigs(devices):
    for device in devices:
        device.get_run()
        stig.check_cat1_nac009(device.parsed_config, sw1)
        stig.check_cat1_net0230(device.parsed_config, sw1)
        stig.check_cat1_net0600(device.parsed_config, sw1)
        stig.check_cat1_net1636(device.parsed_config, sw1)
        stig.check_cat1_net1665(device.parsed_config, sw1)
        stig.check_cat1_net1623(device.parsed_config, sw1)
        stig.check_cat1_net0441(device.parsed_config, sw1)
        stig.check_cat2_net1639(device.parsed_config, sw1)
        stig.check_cat1_net1660(device.parsed_config, sw1)


create_dev(ip_list, "cisco", "cisco")
test_stigs(devices)

# sw1.get_neighbors()
# print(sw2.enable_pass)
# ip_addr = list()
# for neighbor in sw1.neighbors:
#     ip_addr.append(neighbor['ip'])
# print(ip_addr)
#
# switches = list()
# for ip in ip_addr:
#     switches.append(device(ip, "cisco", "cisco", enable_pass="cisco"))
#
# for switch in switches:
#     print(switch.send_command('show ip int br'))
# print(sw1.send_command("show ip int br"))
# devices = [sw1]
# #
# for device in devices:
#     device.get_run()
#     stig.check_cat1_nac009(device.parsed_config, sw1)
#     stig.check_cat1_net0230(device.parsed_config, sw1)
#     stig.check_cat1_net0600(device.parsed_config, sw1)
#     stig.check_cat1_net1636(device.parsed_config, sw1)
#     stig.check_cat1_net1665(device.parsed_config, sw1)
#     stig.check_cat1_net1623(device.parsed_config, sw1)
#     stig.check_cat1_net0441(device.parsed_config, sw1)
#     stig.check_cat2_net1639(device.parsed_config, sw1)
#     stig.check_cat1_net1660(device.parsed_config, sw1)
=======
# sw1.get_neighbors()

# print(sw1.send_command("show ip int br"))
devices = [sw3]
#
for device in devices:
    device.get_run()
    print(stig.check_cat1_nac009(device.parsed_config, device))
    print(stig.check_cat1_net0230(device.parsed_config, device))
    print(stig.check_cat1_net0600(device.parsed_config, device))
    print(stig.check_cat1_net1636(device.parsed_config, device))
    print(stig.check_cat1_net1665(device.parsed_config, device))
    print(stig.check_cat1_net1623(device.parsed_config, device))
    print(stig.check_cat1_net0441(device.parsed_config, device))
    print(stig.check_cat1_net1660(device.parsed_config, device))
    for interfaces in device.ports_wo_dot1x:
        print(interfaces)
>>>>>>> 3882a36e2f6838cb7bc3149577eabedc85c79ed4
