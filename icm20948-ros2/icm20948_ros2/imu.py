#!/usr/bin/env python3
# ... (MIT License as before)

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Temperature, MagneticField
from icm20948 import ICM20948
import math

PUBLISH_RATE = 50
PUBLISH_INTERVAL_S = 1 / PUBLISH_RATE
SLOW_PUBLISH_INTERVAL_S = 1.0

# === Bias calibration (you should update these from your own calibration)
GYRO_BIAS = {
    'x': -0.016107,
    'y': 0.007654,
    'z': 0.004414,
}

ACCEL_BIAS = {
    'x': -0.016176,  # Add your accelerometer bias values here
    'y': -0.101146,
    'z': 0.0,
}

ACCEL_THRESHOLD = 0.005  # rad/s
GYRO_THRESHOLD = 0.05

class ImuNode(Node):
    def __init__(self, imu):
        super().__init__("imu_icm20948")
        self._imu = imu
        self.get_logger().info("IMU has started!")
        
        self.imu_raw_publisher_ = self.create_publisher(Imu, "imu/data_raw", 10)
        self.imu_temp_publisher_ = self.create_publisher(Temperature, "imu/temp", 10)
        self.imu_mag_publisher_ = self.create_publisher(MagneticField, "imu/mag", 10)
        
        self.data_timer_ = self.create_timer(PUBLISH_INTERVAL_S, self._publish_all)
        self.temperature_timer_ = self.create_timer(SLOW_PUBLISH_INTERVAL_S, self._publish_temperature)

    def _publish_all(self):
        self._publish_raw()
        self._publish_magnetic()

    def _publish_raw(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"
        
        # Read raw sensor data
        ax, ay, az, gx, gy, gz = self._imu.read_accelerometer_gyro_data()
        
        # --- Bias correction (after remapping)
        ax_corr = ax - ACCEL_BIAS['x']
        ay_corr = ay - ACCEL_BIAS['y'] 
        az_corr = az - ACCEL_BIAS['z']
        
        gx_corr = gx - GYRO_BIAS['x']
        gy_corr = gy - GYRO_BIAS['y']
        gz_corr = gz - GYRO_BIAS['z']
        
        # --- Noise thresholding for gyroscope
        ax_corr = 0.0 if abs(ax_corr) < ACCEL_THRESHOLD else ax_corr
        ay_corr = 0.0 if abs(ay_corr) < ACCEL_THRESHOLD else ay_corr
        az_corr = 0.0 if abs(az_corr) < ACCEL_THRESHOLD else az_corr

        gx_corr = 0.0 if abs(gx_corr) < GYRO_THRESHOLD else gx_corr
        gy_corr = 0.0 if abs(gy_corr) < GYRO_THRESHOLD else gy_corr
        gz_corr = 0.0 if abs(gz_corr) < GYRO_THRESHOLD else gz_corr
        
        # Convert gyroscope from degrees/s to radians/s
        msg.angular_velocity.x = math.radians(float(gx_corr))
        msg.angular_velocity.y = math.radians(float(gy_corr))
        msg.angular_velocity.z = math.radians(float(gz_corr))
        
        # Set angular velocity covariance
        msg.angular_velocity_covariance[0] = 0.01
        msg.angular_velocity_covariance[4] = 0.01
        msg.angular_velocity_covariance[8] = 0.01
        
        # Linear acceleration (already in m/s²)
        msg.linear_acceleration.x = float(ax_corr)
        msg.linear_acceleration.y = float(ay_corr)
        msg.linear_acceleration.z = float(az_corr)
        
        # Set linear acceleration covariance
        msg.linear_acceleration_covariance[0] = 0.01
        msg.linear_acceleration_covariance[4] = 0.01
        msg.linear_acceleration_covariance[8] = 0.01
        
        # Leave orientation blank — this is for raw data
        msg.orientation_covariance[0] = -1.0  # Means: orientation not available
        
        self.imu_raw_publisher_.publish(msg)

    def _publish_magnetic(self):
        msg = MagneticField()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"
        
        # Read raw magnetometer data
        x, y, z = self._imu.read_magnetometer_data()
        
        # Convert to Tesla (assuming input is in milli-Tesla)
        msg.magnetic_field.x = float(x) / 1000.0
        msg.magnetic_field.y = float(y) / 1000.0
        msg.magnetic_field.z = float(z) / 1000.0
        
        # Set covariance (optional)
        msg.magnetic_field_covariance[0] = 0.01
        msg.magnetic_field_covariance[4] = 0.01
        msg.magnetic_field_covariance[8] = 0.01
        
        self.imu_mag_publisher_.publish(msg)

    def _publish_temperature(self):
        msg = Temperature()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"
        msg.temperature = float(self._imu.read_temperature())
        
        # Set temperature variance (optional)
        msg.variance = 0.1
        
        self.get_logger().info("pub imu_temp " + str(msg.temperature))
        self.imu_temp_publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    imu = ICM20948()
    node = ImuNode(imu)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()