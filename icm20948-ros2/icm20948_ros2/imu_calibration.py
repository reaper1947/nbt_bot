#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class GyroCalibrator(Node):
    def __init__(self, sample_count=500):
        super().__init__('gyro_calibrator')
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data_raw',
            self.imu_callback,
            10)
        self.sample_count = sample_count
        self.samples_collected = 0

        self.ax_sum = 0.0
        self.ay_sum = 0.0
        self.az_sum = 0.0

        self.gx_sum = 0.0
        self.gy_sum = 0.0
        self.gz_sum = 0.0

        self.get_logger().info(f"GyroCalibrator started, collecting {sample_count} samples...")

    def imu_callback(self, msg: Imu):
        if self.samples_collected < self.sample_count:
            
            self.ax_sum += msg.linear_acceleration.x
            self.ay_sum += msg.linear_acceleration.y
            self.az_sum += msg.linear_acceleration.z
            
            self.gx_sum += msg.angular_velocity.x
            self.gy_sum += msg.angular_velocity.y
            self.gz_sum += msg.angular_velocity.z

            self.samples_collected += 1
            if self.samples_collected % 50 == 0:
                self.get_logger().info(f"Collected {self.samples_collected}/{self.sample_count} samples")
        else:
            # Calculate average bias

            bias_ax = self.ax_sum / self.sample_count
            bias_ay = self.ay_sum / self.sample_count
            bias_az = self.az_sum / self.sample_count

            bias_gx = self.gx_sum / self.sample_count
            bias_gy = self.gy_sum / self.sample_count
            bias_gz = self.gz_sum / self.sample_count

            self.get_logger().info(f"Calibration complete!")
            self.get_logger().info(f"Accel bias (m/s): ax={bias_ax:.6f}, ay={bias_ay:.6f}, az={bias_az:.6f}")
            self.get_logger().info(f"Gyro bias (rad/s): gx={bias_gx:.6f}, gy={bias_gy:.6f}, gz={bias_gz:.6f}")

            # Shutdown after calibration
            self.destroy_node()
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = GyroCalibrator(sample_count=500)
    rclpy.spin(node)

if __name__ == '__main__':
    main()
