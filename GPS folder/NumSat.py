from machine import Pin, UART
from time import sleep

# Define UART and GPIO pin settings
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=0, rx=1)

# Function to send AT commands and print responses
def send_at_command(command):
    uart.write(command + b'\r\n')  # Send the command with a newline character
    response = uart.read()  # Read the response (adjust buffer size as needed)
    if response:
        print(response.decode())

# Function to parse GPRMC sentence
def parse_gprmc(gprmc_sentence):
    try:
        gprmc_str = gprmc_sentence.decode('ascii', 'ignore')  # Convert to a string and ignore invalid characters
        parts = gprmc_str.split(',')
        if len(parts) >= 10 and parts[2] == 'A':
            time = parts[1]
            lat = parts[3]
            lat_dir = parts[4]
            lon = parts[5]
            lon_dir = parts[6]
            speed = parts[7]
            course = parts[8]
            date = parts[9]

            print("GPRMC Data:")
            print("Time: {}, Latitude: {} {}, Longitude: {} {}, Speed: {}, Course: {}, Date: {}".format(
                time, lat, lat_dir, lon, lon_dir, speed, course, date))
    except UnicodeError:
        print("UnicodeError: Could not parse GPRMC sentence")

# Function to parse GPGGA sentence
def parse_gpgga(gpgga_sentence):
    try:
        gpgga_str = gpgga_sentence.decode('ascii', 'ignore')  # Convert to a string and ignore invalid characters
        parts = gpgga_str.split(',')
        if len(parts) >= 10:
            time = parts[1]
            lat = parts[2]
            lat_dir = parts[3]
            lon = parts[4]
            lon_dir = parts[5]
            fix_quality = parts[6]
            num_satellites = parts[7]
            hdop = parts[8]
            altitude = parts[9]
            altitude_units = parts[10]

            print("GPGGA Data:")
            print("Time: {}, Latitude: {} {}, Longitude: {} {}, Fix Quality: {}, Num Satellites: {}, HDOP: {}, Altitude: {} {}".format(
                time, lat, lat_dir, lon, lon_dir, fix_quality, num_satellites, hdop, altitude, altitude_units))

            if fix_quality == "0":
                print("GPS is searching for satellites")
    except UnicodeError:
        print("UnicodeError: Could not parse GPGGA sentence")

# Function to parse GPGSV sentence
# Function to parse GPGSV sentence
def parse_gpgsv(gpgsv_sentence):
    try:
        gpgsv_str = gpgsv_sentence.decode('ascii', 'ignore')  # Convert to a string and ignore invalid characters
        parts = gpgsv_str.split(',')
        if len(parts) >= 7:
            num_sentences = int(parts[1])
            sentence_num = int(parts[2])
            num_sv_in_view = int(parts[3])
            # Process SV (Satellite in View) data here
            sv_data = parts[4:]
            print("Number of Sentences: {}, Sentence Number: {}, Number of SV in View: {}".format(
                num_sentences, sentence_num, num_sv_in_view))
            print("SV Data:", sv_data)
    except (UnicodeError, ValueError) as e:
        print("Error parsing GPGSV sentence:", e)

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
            try:
                data_str = data.decode('ascii', 'ignore')  # Convert the data to a string and ignore invalid characters
                print(data_str)

                # Split the string into lines and process each line
                for line in data_str.split('\n'):
                    line = line.strip()
                    if line.startswith('$GPRMC'):
                        parse_gprmc(line.encode('ascii'))  # Encode back to bytes
                    if line.startswith('$GPGGA'):
                        parse_gpgga(line.encode('ascii'))  # Encode back to bytes
                    if line.startswith('$GPGSV'):
                        parse_gpgsv(line.encode('ascii'))  # Encode back to bytes
            except UnicodeError:
                print("UnicodeError: Could not decode data")
    sleep(1)
