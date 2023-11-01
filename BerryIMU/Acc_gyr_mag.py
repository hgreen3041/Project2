import time
from machine import Pin, I2C
import lis3mdl
from LSM6DSL import *
import IMU_I2C as IMU


i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
lis = lis3mdl.LIS3MDL(i2c)
lis.operation_mode = lis3mdl.POWER_DOWN
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
DEG_TO_RAD = 1/57.2958





while True:
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()

    # Convert Gyro raw to degrees per second
    rate_gyr_x =  (GYRx * G_GAIN)*DEG_TO_RAD
    rate_gyr_y =  (GYRy * G_GAIN)*DEG_TO_RAD
    rate_gyr_z =  (GYRz * G_GAIN)*DEG_TO_RAD

    


      
    magx, magy, magz = lis.magnetic
    lis.operation_mode = lis3mdl.CONTINUOUS

    print(f"X={rate_gyr_x:0.2f}\tY={rate_gyr_y:0.2f}\tZ={rate_gyr_z:0.2f} rads/S")
    print(f"X={magx:0.2f}\tY={magy:0.2f}\tZ={magz:0.2f} uT")
    print(f"X={(((ACCx * 0.12)/1000)*9.80665):0.2f}" + f"\tY={(((ACCy * 0.12)/1000)*9.80665):0.2f}" +  f"\tZ={(((ACCz * 0.12)/1000)*9.80665):0.2f} m/S^2")
    time.sleep(0.2)

    