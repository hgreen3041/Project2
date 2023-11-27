import tkinter as tk
import serial
import threading
def receive_data():
    while True:
        try:
            data = ser.readline().decode().strip().split()
            if len(data) == 12:
                x_val, y_val, z_val, x_mag, y_mag, z_mag, x_acc, y_acc, z_acc, lat, lon, elevation, numSat = map(float, data)
                update_display(x_val, y_val, z_val, x_mag, y_mag, z_mag, x_acc, y_acc, z_acc, lat, lon, elevation, numSat)
        except KeyboardInterrupt:
            break

def update_display(xVel, yVel, zVel, x_mag, y_mag, z_mag, x_acc, y_acc, z_acc, lat, lon, elevation, numSat):
    # Update the GUI display with the received data
    # You can modify this part according to your GUI design
    angular_velocity_label.config(text="Angular Velocity")
    x_label.config(text=f"X: {xVel}")
    y_label.config(text=f"Y: {yVel}")
    z_label.config(text=f"Z: {zVel}")

    magnetic_field_label.config(text="Magnetic Field")
    x_mag_label.config(text=f"X: {x_mag}")
    y_mag_label.config(text=f"Y: {y_mag}")
    z_mag_label.config(text=f"Z: {z_mag}")

    magnetic_field_label.config(text="Acceleration")
    x_mag_label.config(text=f"X: {x_acc}")
    y_mag_label.config(text=f"Y: {y_acc}")
    z_mag_label.config(text=f"Z: {z_acc}")

    gps_coordinates_label.config(text="GPS information")
    lat_label.config(text=f"Latitude: {lat}")
    lon_label.config(text=f"Longitude: {lon}")
    elevation_label.config(text=f"Elevation: {elevation}")
    numSat_label.config(text=f"# if satellites: {numSat}")

# Create the GUI
root = tk.Tk()
root.title("Sensor Data Display")

# Labels for Angular Velocity
angular_velocity_label = tk.Label(root, text="Angular Velocity", font=("Helvetica", 12, "bold"))
angular_velocity_label.pack()
x_label = tk.Label(root, text="X: ")
x_label.pack()
y_label = tk.Label(root, text="Y: ")
y_label.pack()
z_label = tk.Label(root, text="Z: ")
z_label.pack()

# Labels for Magnetic Field
magnetic_field_label = tk.Label(root, text="Magnetic Field", font=("Helvetica", 12, "bold"))
magnetic_field_label.pack()
x_mag_label = tk.Label(root, text="X: ")
x_mag_label.pack()
y_mag_label = tk.Label(root, text="Y: ")
y_mag_label.pack()
z_mag_label = tk.Label(root, text="Z: ")
z_mag_label.pack()

# Labels for Acceleration
magnetic_field_label = tk.Label(root, text="Acceleration", font=("Helvetica", 12, "bold"))
magnetic_field_label.pack()
x_mag_label = tk.Label(root, text="X: ")
x_mag_label.pack()
y_mag_label = tk.Label(root, text="Y: ")
y_mag_label.pack()
z_mag_label = tk.Label(root, text="Z: ")
z_mag_label.pack()

# Labels for GPS Coordinates
gps_coordinates_label = tk.Label(root, text="GPS Coordinates", font=("Helvetica", 12, "bold"))
gps_coordinates_label.pack()
lat_label = tk.Label(root, text="Latitude: ")
lat_label.pack()
lon_label = tk.Label(root, text="Longitude: ")
lon_label.pack()
elevation_label = tk.Label(root, text="Elevation: ")
elevation_label.pack()
numSat_label = tk.Label(root, text="# of Satellites")
numSat_label.pack()

# Serial communication setup
ser = serial.Serial('COM5', 115200)  # Update 'COM3' with the correct port

# Start a thread to receive and update data
receive_data_thread = threading.Thread(target=receive_data)
receive_data_thread.start()

root.mainloop()
