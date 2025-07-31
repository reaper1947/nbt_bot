import os
from glob import glob
from setuptools import setup

package_name = 'icm20948_ros2'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join("share", package_name + "/launch"),
            glob("launch/*launch.[pxy][yma]*"),
        ),
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    maintainer='Andy Blight',
    maintainer_email='a.j.blight@leeds.ac.uk',
    description='ICM20948 IMU ROS 2 Driver for Raspberry Pi',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "imu_node = icm20948_ros2.imu:main",
            "imu_calibration = icm20948_ros2.imu_calibration:main",
        ],
    },
)
