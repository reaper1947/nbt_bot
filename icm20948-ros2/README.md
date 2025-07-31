# ROS 2 driver for ICM20948 IMU

This ROS 2 driver of the ICM20948 implements a ROS2 wrapper around the Pimoroni Python library: [ICM20948-Python](https://github.com/pimoroni/icm20948-python/tree/master).

My development notes can be found [here](development.md).

## ROS Interfaces

This implementation has one node, `imu_icm20948`, that publishes on the following data:

| Message | Topic | Default Rate |
|:--|:--|:--|
| [sensor_msgs/msg/Imu](https://docs.ros2.org/latest/api/sensor_msgs/msg/Imu.html) | "imu/data_raw" | 20 Hz |
| [sensor_msgs/msg/MagneticField](https://docs.ros2.org/latest/api/sensor_msgs/msg/MagneticField.html) | "imu/mag" | 20 Hz |
| [sensor_msgs/msg/Temperature](https://docs.ros2.org/latest/api/sensor_msgs/msg/Temperature.html) | "imu/temp" | 1 Hz |

Note: If you need a position estimate (Quaternion), the package `[IMU tools for ROS](https://github.com/CCNYRoboticsLab/imu_tools/tree/humble)` should be installed and launched.  Two filters are provided, Madgwick and complimentary (recommended).

## To install and run on the Raspberry Pi

To install on a Raspberry Pi, install ROS2 Humble on RPi.  Then run:

```bash
sudo pip3 install icm20948
sudo apt install i2c-tools
```

Connect the IMU as per the wiring schedule in [development.md](development.md).  This should work.

```bash
sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

Now to allow the user to use the I2C buses without `sudo`.

```bash
sudo adduser $USER dialout
```

Log out and in again.  Verify that `i2cdetect -y 1` works without `sudo``.

## Getting the ROS 2 driver working

Now that the basics are set up, time to create a ROs2 driver.  Fortunately, I wrote a Python driver for the BNO055 a while ago so I'm starting with that.

Imported most of the files to create a package, changed the names but left the actual code in `imu.py` unchanged.  Made sure that `colcon build` worked and that I could launch the node (event though I know it would not run).

Then I started modifying the code in

## Known issues

Work in progress so expect nothing to work!

Please raise a GitHub issue on this repo if you find a problem.

## Acknowledgements

&copy; 2023 University of Leeds.

The author, A. Blight, asserts his moral rights.
