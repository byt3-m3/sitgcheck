from modules.device import device as router
import os


sw1 = router("192.168.1.2", "cisco", "cisco")
r1 = router("192.168.1.123", "cisco", "cisco")

r1.connect()
print r1.hostname
