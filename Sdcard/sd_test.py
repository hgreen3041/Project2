import machine
import sdcard
import uos
import time

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(9, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(8))

# Initialize SD card
sde = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sde)
uos.mount(vfs, "/sde")

# Generate a unique filename using current date and time
current_time = time.localtime()
filename = "/sde/data_{}_{}_{}_{}_{}_{}.csv".format(current_time[0], current_time[1], 
                                                   current_time[2], current_time[3], 
                                                   current_time[4], current_time[5])

# Open the file in 'a' (append) mode
with open(filename, "a") as file:
    # Write header if the file is empty (only once)
    if file.tell() == 0:
        file.write("latitude,longitude,elevation,satellites,angular_velocity,acceleration,magnetic_field\n")

    # Main loop for continuous data logging
    for a in range(10):
        # Read sensor data here
        # Replace the following with actual data from your sensors
        latitude = 69
        longitude = 56.78   
        elevation = 100
        satellites = 8
        angular_velocity = 0.1
        acceleration = 9.8
        magnetic_field = 40

        # Write data to CSV
        file.write(f"{latitude},{longitude},{elevation},{satellites},{angular_velocity},{acceleration},{magnetic_field}\n")

        # Wait for a short period to control the sampling rate
        time.sleep(1)  # Adjust the sleep duration as needed

# Unmount the filesystem
uos.unmount("/sde")
