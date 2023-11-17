from machine import Pin, UART, SPI, I2C
import sdcard
import os
import time
import math
from LSM6DSL import LSM6DSL
import IMU_I2C as IMU
import lis3mdl

# Initialize UART for GPS
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Initialize I2C for IMU
i2c = I2C(1, sda=Pin(2), scl=Pin(3))
lis3 = lis3mdl.LIS3MDL(i2c)
imu = LSM6DSL(i2c)
imu.enable()

# SD card setup
cs = Pin(9, Pin.OUT)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
sd = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# Constants
G_GAIN = 0.070  # [deg/s/LSB]
DEG_TO_RAD = math.pi / 180

# GPS Data Variables
latitude = None
longitude = None
elevation = None
satellites = None
date = None
time = None

# Create a new CSV file with the current timestamp
def create_new_csv():
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = f'/sd/gps_imu_data_{timestamp}.csv'
    with open(filename, 'w') as f:
        f.write("Timestamp, Latitude, Longitude, Elevation, Satellites, Accel X, Accel Y, Accel Z, Gyro X, Gyro Y, Gyro Z, Mag X, Mag Y, Mag Z\n")
    return filename

current_csv_file = create_new_csv()

# Function to parse GPGGA sentence (GPS)
def parse_gpgga(data_str):
    global latitude, longitude, elevation, satellites, time
    parts = data_str.split(',')
    if parts[6] != '0':  # Valid fix
        time = parts[1]
        latitude = parts[2] + " " + parts[3]
        longitude = parts[4] + " " + parts[5]
        elevation = parts[9] + " " + parts[10]
        satellites = parts[7]

# Main loop
while True:
    led_pin.toggle()

    # Read GPS data
    if uart.any():
        gps_data = uart.read(256).decode('utf-8', 'ignore')
        for line in gps_data.split('\r\n'):
            if line.startswith('$GPGGA'):
                parse_gpgga(line)

    # Read IMU data
    acc_data = imu.read_acceleration()
    gyro_data = imu.read_gyroscope()
    mag_data = lis3.magnetic

    # Convert Gyro raw to radians per second
    gyro_x, gyro_y, gyro_z = [gyro * G_GAIN * DEG_TO_RAD for gyro in gyro_data]

    # Construct CSV data line
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    csv_line = f"{timestamp}, {latitude}, {longitude}, {elevation}, {satellites}, {acc_data[0]}, {acc_data[1]}, {acc_data[2]}, {gyro_x}, {gyro_y}, {gyro_z}, {mag_data[0]}, {mag_data[1]}, {mag_data[2]}\n"

    # Append the data line to the current CSV file
    with open(current_csv_file, 'a') as f:
        f.write(csv_line)
    
    time.sleep(1)

# Unmount filesystem when done
os.umount("/sd")
