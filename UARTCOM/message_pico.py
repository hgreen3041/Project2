import machine
import time

# Initialize UART0 with a baud rate of 9600
uart = machine.UART(0, baudrate=9600)
uart.init(bits=8, parity=None, stop=1)
# GPIO0 (TX) and GPIO1 (RX) are used for UART communication

while True: 
    message = "Hello from Pico!"
    print(message)

    # Delay to allow time for data to be sent
    time.sleep(2)
