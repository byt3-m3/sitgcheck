from modules.device import device as router


sw1 = router("192.168.1.2", "cisco", "cisco")
r1 = router("192.168.1.123", "cisco", "cisco")

sw1.connect()
r1.connect()
sw1.get_all_interfaces()
r1.get_all_interfaces()
print(sw1.all_interface_list)
print(r1.all_interface_list)
# r1.connect()
# r1.send_command("show ip route")
