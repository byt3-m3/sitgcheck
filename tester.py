from modules.device import device as router
from modules import l2stig as stig
import os
os.system("clear")

sw1 = router("192.168.1.2", "cisco1", "cisco1", enable_pass="cisco")
# sw2 = router("192.168.1.250", "cisco", "cisco")
# r1 = router("192.168.1.123", "c0isco", "cisco")
#


# print(sw1.send_command("show ip route"))
# print(sw1.get_run())

sw1.get_run()
stig.check_cat1_nac009(sw1.parsed_config, sw1)
