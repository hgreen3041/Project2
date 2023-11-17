from machine import Pin, UART, SPI
import sdcard
import os
import time

# Define UART and GPIO pin settings for GPS
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# GPS Data Variables
latitude = None
longitude = None
elevation = None
satellites = None
gps_time = None
gps_date = None

# Function to parse GPGGA sentence
def parse_gpgga(gpgga_sentence):
    global latitude, longitude, elevation, satellites, gps_time
    parts = gpgga_sentence.decode('ascii', 'ignore').split(',')
    if parts[6] != '0':  # Valid fix
        gps_time = parts[1]
        latitude = parts[2] + " " + parts[3]
        longitude = parts[4] + " " + parts[5]
        elevation = parts[9] + " " + parts[10]
        satellites = parts[7]

# Function to parse GPRMC sentence
def parse_gprmc(gprmc_sentence):
    global gps_date
    parts = gprmc_sentence.decode('ascii', 'ignore').split(',')
    if parts[2] == 'A':  # Data is valid
        gps_date = parts[9]

# SD card setup
cs = Pin(9, Pin.OUT)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
sd = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# Function to create a new CSV file with the current timestamp
def create_new_csv():
    year, month, day, hour, minute, second, _, _ = time.localtime()
    timestamp = "{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(year, month, day, hour, minute, second)
    filename = f'/sd/gps_data_{timestamp}.csv'
    with open(filename, 'w') as f:
        f.write("Date, Time, Latitude, Longitude, Elevation, Satellites\n")
    return filename


# Create a new CSV file for this session
current_csv_file = create_new_csv()

# Main loop
while True:
    led_pin.toggle()

    # Read GPS data
    if uart.any():
        gps_data = uart.read(256).decode('utf-8', 'ignore')
        for line in gps_data.split('\r\n'):
            if line.startswith('$GPGGA'):
                parse_gpgga(line.encode('ascii'))
            elif line.startswith('$GPRMC'):
                parse_gprmc(line.encode('ascii'))

    # Construct CSV data line
    current_time = time.localtime()
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])
    csv_line = f"{timestamp}, {latitude}, {longitude}, {elevation}, {satellites}\n"

    # Append the data line to the current CSV file
    with open(current_csv_file, 'a') as f:
        f.write(csv_line)
    
    time.sleep(1)

# Unmount filesystem when done
os.umount("/sd")
