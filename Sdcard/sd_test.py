from machine import Pin, UART, SPI
import sdcard
import uos
import time

# GPS setup
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=0, rx=1)

# SD card setup
cs = machine.Pin(9, machine.Pin.OUT)
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB, sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(8))
sde = sdcard.SDCard(spi, cs)
vfs = uos.VfsFat(sde)
uos.mount(vfs, "/sde")

# Initialize variables for GPS data
gps_time = ""
gps_date = ""
latitude = ""
longitude = ""
num_satellites = ""

# Function to get a unique filename based on GPS time
def get_filename():
    if gps_time and gps_date:
        # Format: gps_data_DDMMYY_HHMMSS.csv
        filename = "/sde/gps_data_{}_{}_{}_{}_{}_{}.csv".format(
            gps_date[0:2], gps_date[2:4], gps_date[4:6],  # Day, Month, Year
            gps_time[0:2], gps_time[2:4], gps_time[4:6]   # Hour, Minute, Second
        )
        return filename
    else:
        # Fallback filename if GPS time and date are not available
        return "/sde/gps_data_unknown.csv"

# Function to send AT commands
def send_at_command(command):
    uart.write(command + b'\r\n')  # Send the command with a newline character
    response = uart.read()  # Read the response (adjust buffer size as needed)
    if response:
        print(response.decode())

# Function to parse GPGGA sentence
def parse_gpgga(gpgga_sentence):
    global gps_time, latitude, longitude, num_satellites
    try:
        parts = gpgga_sentence.decode('ascii', 'ignore').split(',')
        if len(parts) >= 10 and parts[6] != '0':  # Checking for a valid fix
            gps_time = parts[1]
            latitude = parts[2] + " " + parts[3]
            longitude = parts[4] + " " + parts[5]
            num_satellites = parts[7]
            gps_date = ""  # You can assign the date here if available in GPGGA
    except UnicodeError:
        print("UnicodeError: Could not parse GPGGA sentence")

# Main loop
while True:
    led_pin.toggle()
    
    if uart.any():
        data = uart.read(256)
        if data:
            data_str = data.decode('ascii', 'ignore')  # Convert the data to a string and ignore invalid characters
            print(data_str)

            # Split the string into lines and process each line
            for line in data_str.split('\n'):
                line = line.strip()
                if line.startswith('$GPGGA'):
                    parse_gpgga(line.encode('ascii'))  # Encode back to bytes

    # Write GPS data to SD card
    filename = get_filename()
    with open(filename, "a") as file:
        if file.tell() == 0:
            # Write header to new file
            file.write("Time, Latitude, Longitude, Num Satellites\n")
        file.write(f"{gps_time}, {latitude}, {longitude}, {num_satellites}\n")
    
    time.sleep(1)

# Unmount filesystem when done
uos.unmount("/sde")
