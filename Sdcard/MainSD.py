from machine import Pin, UART, SPI, I2C
import sdcard
import uos
import time
import math
from LSM6DSL import *
import IMU_I2C as IMU
import lis3mdl

# GPS setup
led_pin = Pin(25, Pin.OUT)
uart = UART(0, baudrate=9600, tx=0, rx=1)

# IMU setup
i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
lis = lis3mdl.LIS3MDL(i2c)
IMU.initIMU()  # Initialise the accelerometer, gyroscope and compass

# SD card setup
cs = Pin(9, Pin.OUT)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
sd = sdcard.SDCard(spi, cs)
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Constants
G_GAIN = 0.070  # [deg/s/LSB] Update this value based on your gyro's configuration
DEG_TO_RAD = math.pi / 180

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
    lis.operation_mode = lis3mdl.CONTINUOUS

    # Convert accelerometer values to meters per second squared
    accel_x = (((ACCx * 0.12) / 1000) * 9.80665)
    accel_y = (((ACCy * 0.12) / 1000) * 9.80665)
    accel_z = (((ACCz * 0.12) / 1000) * 9.80665)

    # GPS data collection
    if uart.any():
        data = uart.read(256)
        if data:
            # Process GPS data just like you would in your GPS script
            # ...

    # Construct CSV data line
            csv_line = f"{time.gmtime()}, {accel_x}, {accel_y}, {accel_z}, {rate_gyr_x}, {rate_gyr_y}, {rate_gyr_z}, {magx}, {magy}, {magz}\n"

    # Write to CSV
    with open('/sd/gps_imu_data.csv', 'a') as f:
        if f.tell() == 0:
            # Write header if file is empty
            f.write("Time, Accel X, Accel Y, Accel Z, Gyro X, Gyro Y, Gyro Z, Mag X, Mag Y, Mag Z\n")
        f.write(csv_line)

    time.sleep(0.5)  # Adjust as needed for your application

# Properly unmount the SD card before removing it
uos.unmount("/sd")
