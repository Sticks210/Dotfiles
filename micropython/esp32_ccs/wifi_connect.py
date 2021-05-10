import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("ARRIS-831A-EXT", "2W4235100567")
