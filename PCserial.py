import serial
import time

port = serial.Serial('COM4', 115200)


while True: 
        time.sleep(0.1)
        data = port.readline()
        if data: 
            print("PC received: ", data)
            port.write(data)
        