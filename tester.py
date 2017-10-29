from modules.device import device
from modules import l2stig as stig
import os

os.system("clear")
sw1 = device("192.168.1.2", "cisco1", "cisco1", enable_pass="cisco")
sw2 = device("192.168.1.2", "cisco", "cisco", enable_pass="cisco")
# sw2 = router("192.168.1.250", "cisco", "cisco")
# r1 = router("192.168.1.123", "c0isco", "cisco")
#

ip_list = ['192.168.1.250', '192.168.1.11']


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
