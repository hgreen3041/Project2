import serial

# Replace 'COM3' with the appropriate serial port name for your Pico (Windows) or '/dev/ttyACM0' (Linux)
ser = serial.Serial('COM4', 115200, timeout=1)  # Replace 'COM3' with the correct port

while True:
    try:
        message = ser.readline().decode().strip()
        if message:
            print(f"Received from Pico: {message}")
    except KeyboardInterrupt:
        ser.close()
        break
