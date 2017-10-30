from modules.device import device as dev
from modules import l2stig as stig
import os

os.system("clear")
# sw1 = device("192.168.1.2", "cisco1", "cisco1", enable_pass="cisco")
# sw2 = device("192.168.1.2", "cisco", "cisco", enable_pass="cisco")
# # sw2 = router("192.168.1.250", "cisco", "cisco")
# # r1 = router("192.168.1.123", "c0isco", "cisco")
#

gns3_sw_ip = ['192.168.2.100',
              '192.168.2.101',
              '192.168.2.102',
              '192.168.2.103']

devices = list()


def create_dev(ip_addr, username, password, **kwargs):
    print("""\tPLease Wait While devices are being created
    """)
    try:
        for ip in ip_addr:
            devices.append(dev(ip, "cisco", "cisco", enable_pass="cisco"))

        for net_dev in devices:
            net_dev.get_run()

    except Exception:
        print("Failed")


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


create_dev(gns3_sw_ip, "cisco", "cisco")
# ip_list = list()
# for switch in devices:
#     switch.get_neighbors()
#     for nbr in switch.neighbors:
#         ip_list.append(nbr['ip'])
# print(ip_list)
