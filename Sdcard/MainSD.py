import time
from machine import Pin, UART, SPI, I2C, SPI
import sdcard
import uos
import math
from LSM6DSL import *
import IMU_I2C as IMU
import lis3mdl

# Initialize UART for GPS
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=0, rx=1)

# Initialize I2C for IMU
i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
lis = lis3mdl.LIS3MDL(i2c)
lis.operation_mode = lis3mdl.CONTINUOUS
IMU.initIMU()  # Initialize the IMU

# SD card setup
cs = Pin(9, Pin.OUT)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
sd = sdcard.SDCard(spi, cs)
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# IMU constants
G_GAIN = 0.070  # [deg/s/LSB] Update this value based on your gyro's configuration
DEG_TO_RAD = math.pi / 180

# Function to create a new CSV file with the current timestamp
def create_new_csv():
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = f'/sd/gps_imu_data_{timestamp}.csv'
    with open(filename, 'w') as f:
        f.write("Timestamp, Latitude, Longitude, Elevation, Satellites, Accel X, Accel Y, Accel Z, Gyro X, Gyro Y, Gyro Z, Mag X, Mag Y, Mag Z\n")
    return filename

# Create a new CSV file for this session
current_csv_file = create_new_csv()

# Main loop
while True:
    led_pin.toggle()

    # Read IMU data
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()

    # Convert Gyro raw to radians per second
    rate_gyr_x = GYRx * G_GAIN * DEG_TO_RAD
    rate_gyr_y = GYRy * G_GAIN * DEG_TO_RAD
    rate_gyr_z = GYRz * G_GAIN * DEG_TO_RAD

    # Get magnetic field strength
    magx, magy, magz = lis.magnetic

    # Convert accelerometer values to meters per second squared
    accel_x = (((ACCx * 0.12) / 1000) * 9.80665)
    accel_y = (((ACCy * 0.12) / 1000) * 9.80665)
    accel_z = (((ACCz * 0.12) / 1000) * 9.80665)

    # Read GPS data (integrate your GPS data extraction logic here)
    # ...

    # Construct CSV data line
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    csv_line = f"{timestamp}, {latitude}, {longitude}, {elevation}, {satellites}, {accel_x}, {accel_y}, {accel_z}, {rate_gyr_x}, {rate_gyr_y}, {rate_gyr_z}, {magx}, {magy}, {magz}\n"

    # Append the data line to the current CSV file
    with open(current_csv_file, 'a') as f:
        f.write(csv_line)
    
    time.sleep(1)

# Unmount filesystem when done
uos.unmount("/sd")
