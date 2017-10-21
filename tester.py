from modules.device import device as router


sw1 = router("192.168.1.2", "cisco", "cisco")
r1 = router("192.168.1.123", "cisco", "cisco")

# sw1.connect()
print(sw1.get_neighbors())
