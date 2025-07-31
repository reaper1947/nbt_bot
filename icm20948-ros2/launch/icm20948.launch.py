#!/usr/bin/python3

# Copyright 2023 University of Leeds
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


#!/usr/bin/python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    imu_driver_node = Node(
        package="icm20948_ros2",
        executable="imu_node",
        name="icm20948_driver"
    )

    imu_filter_node = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        name='imu_filter',
        parameters=[{
            'use_mag': True,
            'use_magnetic_field_msg': True,
            'publish_tf': False,
            'world_frame': 'odom',
            'orientation_stddev': 0.05,
            'gain': 0.01
        }],
        remappings=[
            ('imu/data_raw', '/imu/data_raw'),
            ('imu/data', '/imu/data')
        ]
    )

    # node_imu_link = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='base_to_laser',
    #     arguments=[
    #         '0.15', '0', '0.095',
    #         '0', '0', '0',
    #         'chassis', 'imu_link'
    #     ],
    #     output='screen'
    # )

    return LaunchDescription([
        imu_driver_node,
        imu_filter_node,
        # node_imu_link
    ])

