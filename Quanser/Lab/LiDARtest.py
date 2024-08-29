from pal.utilities.lidar import Lidar



# Initialize a Lidar device (e.g. RPLidar)
lidar_device = Lidar(type='RPLidar')

# Read LiDAR measurements
lidar_device.read()

# Access measurement data
print((lidar_device.distances, lidar_device.angles))

# Terminate the LiDAR device connection
lidar_device.terminate()