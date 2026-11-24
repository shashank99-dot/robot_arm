from pathlib import Path
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription 
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    package_directry = Path(get_package_share_directory('robot_arm'))

    gazebo_directory = Path(get_package_share_directory('ros_gz_sim'))

    urdf_file = package_directry / 'urdf' / 'robot_arm.urdf'

    resource_path = os.pathsep.join(path for path in [str(package_directry.parent),
                                                      os.environ.get('GZ_SIM_RESOURCE_PATH', ''), ] if path)

    gazebo_resources = SetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH', value=resource_path,)

    gazebo = IncludeLaunchDescription(
               PythonLaunchDescriptionSource(
                 str(gazebo_directory / 'launch' / 'gz_sim.launch.py')
                 ),
                 launch_arguments={ 'gz_args': '-v 4 empty.sdf',}.items(),
                 )

    spawn_arm = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-world', 'empty',
                   '-name', 'robot_arm',
                   '-file', str(urdf_file),
                   ],
                   output='screen',
    )

    return LaunchDescription([gazebo_resources,
                              gazebo,
                              spawn_arm,
                              ])