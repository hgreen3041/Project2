import machine
import time

# Configure UART0 to use the USB CDC (Communication Device Class)
uart = machine.UART(0, baudrate=115200)
led = machine.Pin('LED', machine.Pin.OUT)
led.value(0)

time.sleep(5)
message = "starting comms session/r/n"
print(message)


while True:
        data = uart.readline()
        time.sleep(0.1)
        print(data)
    
    

        
# while True: 
#     led.value(1)
#     time.sleep(0.5)
#     led.value(0)
#     time.sleep(0.5)

    