from machine import Pin, UART, SPI
import sdcard
import os
import time
import utime

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
        # print("gps time: ", gps_time)
        gps_time = convertGPSTime(gps_time)
        # print("Converted gps time: ", gps_time)
        latitude = parts[2] + " " + parts[3]
        longitude = parts[4] + " " + parts[5]
        elevation = parts[9] + " " + parts[10]
        satellites = parts[7]

def convertGPSTime(gpsTime):
    floatAsString = str(gpsTime)
    time = floatAsString[0:2] + ":" + floatAsString[2:4] + ":" + floatAsString[4:6]
    return time

# Function to parse GPRMC sentence
def parse_gprmc(gprmc_sentence):
    try:
        global gps_date
        parts = gprmc_sentence.decode('ascii', 'ignore').split(',')
        if parts[2] == 'A':  # Data is valid
            gps_date = parts[9]
            # print("gps date: ", gps_date)
            gps_date = convertGPSDate(gps_date)
            # print("Converted GPS date: ", gps_date)

    except IndexError:
        print("Error reading list.")
# Convert the integer from gps to a string with the date
def convertGPSDate(gps_date):
    gps_date = str(gps_date)
    month = gps_date[2:4]
    day = gps_date[0:2]
    year = gps_date[4:6]
    date = month + "/" + day + "/" + year
    return date

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
        f.write("Date, time, Latitude, Longitude, Elevation, Satellites\n")
    return filename


# Create a new CSV file for this session
current_csv_file = create_new_csv()
try: 
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
        # current_time = time.localtime()
        # timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])
        csv_line = f"{gps_date}, {gps_time}, {latitude}, {longitude}, {elevation}, {satellites}\n"
        # print("Latitude: ", latitude)
        # print("Longitude: ", longitude)
        # print("Elevation: ", elevation)
        # print("# of satellites: ", satellites)

        # Append the data line to the current CSV file
        with open(current_csv_file, 'a') as f:
            f.write(csv_line)
        
        time.sleep(1)

except UnicodeError:
    print("GPS malfunction.")
    os.umount("/sd")

except KeyboardInterrupt:
    print("Stopping program.")
    # Unmount filesystem when done
    os.umount("/sd")


