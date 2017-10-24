from modules.device import device
from modules import l2stig as stig


sw1 = device("192.168.1.2", "cisco1", "cisco1", enable_pass="cisco")
sw2 = device("192.168.1.2", "cisco", "cisco", enable_pass="cisco")
# sw2 = router("192.168.1.250", "cisco", "cisco")
# r1 = router("192.168.1.123", "c0isco", "cisco")
#


# sw1.get_neighbors()
print(sw2.enable_pass)

test
print(sw1.send_command("show ip int br"))
# devices = [sw1]
#
# for device in devices:
#     stig.check_cat1_nac009(device.parsed_config, sw1)
#     stig.check_cat1_net0230(device.parsed_config, sw1)
#     stig.check_cat1_net0600(device.parsed_config, sw1)
#     stig.check_cat1_net1636(device.parsed_config, sw1)
#     stig.check_cat1_net1665(device.parsed_config, sw1)
#     stig.check_cat1_net1623(device.parsed_config, sw1)
#     stig.check_cat1_net0441(device.parsed_config, sw1)
#     stig.check_cat2_net1639(device.parsed_config, sw1)
#     stig.check_cat1_net1660(device.parsed_config, sw1)
