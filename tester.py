from modules.device import device as router


sw1 = router("192.168.1.2", "cisco", "cisco")
r1 = router("192.168.1.123", "cisco", "cisco")

r1.connect()
# r1.get_config()
print(r1.get_config())
# print r1.hostname
# print sw1.hostname
