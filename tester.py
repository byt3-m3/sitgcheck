from modules.device import device as router
from modules import l2stig as stig

sw1 = router("192.168.1.2", "cisco", "cisco")
# sw2 = router("192.168.1.250", "cisco", "cisco")
# r1 = router("192.168.1.123", "cisco", "cisco")
# sw1.get_snmp_users()
# print(sw1.int_list)
# print(sw1.get_snmp_users())
stig.check_net1623(sw1.parsed_config)
