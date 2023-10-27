import machine
import time

# Configure UART0 to use the USB CDC (Communication Device Class)
uart = machine.UART(0, baudrate=115200)
led = machine.Pin('LED', machine.Pin.OUT)
led.value(0)

# while True:
#     led.value(0)
#     if uart.any(): 
#         print("Recieved: ", uart.readline())
#         led.value(1)

        
while True: 
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)

    