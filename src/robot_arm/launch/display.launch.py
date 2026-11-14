from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription 
from launch_ros.actions import Node



def generate_launch_description():
    package_directory = Path(get_package_share_directory('robot_arm'))

    urdf_file = package_directory / 'urdf' / 'robot_arm.urdf'
    rviz_config = package_directory / 'rviz' / 'display.rviz'

    robot_description = urdf_file.read_text()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}],
        output = 'screen',
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', str(rviz_config)],
        output='screen',
    )

    return LaunchDescription([robot_state_publisher, 
                              joint_state_publisher_gui,
                              rviz,])













