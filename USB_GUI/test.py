import machine
import utime

# Set up UART communication
uart = machine.UART(0, baudrate=115200, tx=0, rx=1)  # Assuming TX on Pin 0, RX on Pin 1

# Function to read sensor data and send it via UART
def send_sensor_data():
    while True:
        x_val = 0.00  # Replace with actual sensor reading
        y_val = 0.07  # Replace with actual sensor reading
        z_val = 0.02  # Replace with actual sensor reading
        x_mag = -41.63  # Replace with actual sensor reading
        y_mag = 39.58  # Replace with actual sensor reading
        z_mag = 6.71  # Replace with actual sensor reading

        # Format the data and send it via UART
        data = "{:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format(
            x_val, y_val, z_val, x_mag, y_mag, z_mag
        )
        uart.write(data + "\n")

        # Wait for a short duration before sending the next set of data
        utime.sleep(1)

# Start sending sensor data via UART
send_sensor_data()
