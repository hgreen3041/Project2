from machine import I2C, Pin

scanner = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)



devAddr = scanner.scan()

for address in devAddr: 
    print(hex(address))
