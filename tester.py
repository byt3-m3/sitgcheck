from modules.device import device as dev
from modules import l2stig as stig
import os

if "nt" in os.name:
    os.system("cls")
else:
    os.system("clear")

# sw1 = dev("192.168.1.2", "cisco", "cisco", enable_pass="cisco")
# sw2 = dev("10.0.100.13", "cisco", "cisco", enable_pass="cisco")
sw3 = dev("10.0.100.3", "cisco", "cisco", enable_pass="cisco")
# sw2 = router("192.168.1.250", "cisco", "cisco")
# r1 = router("192.168.1.123", "c0isco", "cisco")
#


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
