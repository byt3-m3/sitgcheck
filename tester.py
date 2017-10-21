from modules.device import device as router


sw1 = router("192.168.1.2", "cisco", "cisco")
sw2 = router("192.168.1.250", "cisco", "cisco")
r1 = router("192.168.1.123", "cisco", "cisco")

# sw1.connect()
sw1.get_neighbors()
print(sw1.neighbors[1]["ip"])
print(sw1.neighbors[1]["hostname"])
# print(r1.get_neighbors())
