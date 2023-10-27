from machine import I2C, Pin

scanner = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)



devAddr = scanner.scan()

for address in devAddr: 
    print(hex(address))
