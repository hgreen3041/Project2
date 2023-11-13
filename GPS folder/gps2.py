from machine import Pin, UART
from time import sleep
 
# Define UART and GPIO pin settings
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=0, rx=1)
 
# Initialize variables to store GPS data
latest_gps_data = {
    "Time": "",
    "Latitude": "",
    "Latitude Direction": "",
    "Longitude": "",
    "Longitude Direction": "",
    "Speed": "",
    "Course": "",
    "Date": "",
    "Fix Quality": "",
    "Num Satellites": "",
    "HDOP": "",
    "Altitude": "",
    "Altitude Units": ""
}
 
# Function to send AT commands and print responses
def send_at_command(command):
    uart.write(command + b'\r\n')  # Send the command with a newline character
    response = uart.read(256)  # Read the response (adjust buffer size as needed)
    if response:
        print(response.decode())
 
# Function to parse GPRMC sentence
def parse_gprmc(gprmc_sentence):
    try:
        parts = gprmc_sentence.split(b',')
        if len(parts) >= 10 and parts[2] == b'A':
            latest_gps_data["Time"] = parts[1].decode('ascii', 'ignore')
            latest_gps_data["Latitude"] = parts[3].decode('ascii', 'ignore')
            latest_gps_data["Latitude Direction"] = parts[4].decode('ascii', 'ignore')
            latest_gps_data["Longitude"] = parts[5].decode('ascii', 'ignore')
            latest_gps_data["Longitude Direction"] = parts[6].decode('ascii', 'ignore')
            latest_gps_data["Speed"] = parts[7].decode('ascii', 'ignore')
            latest_gps_data["Course"] = parts[8].decode('ascii', 'ignore')
            latest_gps_data["Date"] = parts[9].decode('ascii', 'ignore')
    except UnicodeError:
        print("UnicodeError: Could not parse GPRMC sentence")
 
# Function to parse GPGGA sentence
def parse_gpgga(gpgga_sentence):
    try:
        parts = gpgga_sentence.split(b',')
        if len(parts) >= 10:
            latest_gps_data["Fix Quality"] = parts[6].decode('ascii', 'ignore')
            latest_gps_data["Num Satellites"] = parts[7].decode('ascii', 'ignore')
            latest_gps_data["HDOP"] = parts[8].decode('ascii', 'ignore')
            latest_gps_data["Altitude"] = parts[9].decode('ascii', 'ignore')
            latest_gps_data["Altitude Units"] = parts[10].decode('ascii', 'ignore')
    except UnicodeError:
        print("UnicodeError: Could not parse GPGGA sentence")
 
# Send AT commands to configure the GPS module
send_at_command(b'AT')  # Send AT command to check module response
 
# You can send more AT commands here as needed to configure your GPS module
 
# Main loop
while True:
    led_pin.toggle()
    sleep(0.5)
 
    if uart.any():
        data = uart.read(256)  # Read data from the UART buffer
        if data:
            print(data.decode())
 
            # Parse GPRMC sentence if found
            if data.startswith(b'$GPRMC'):
                parse_gprmc(data)
            # Parse GPGGA sentence if found
            if data.startswith(b'$GPGGA'):
                parse_gpgga(data)
 
    # Print the latest GPS data
    print("Latest GPS Data:")
    for key, value in latest_gps_data.items():
        print(f"{key}: {value}")
 
    sleep(1)