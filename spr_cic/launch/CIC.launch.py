from launch import LaunchDescription
import launch_ros.actions


def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            package="turtlebot_bringup",
            node_executable="turtlebot2",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="ydlidar",
            node_executable="ydlidar_node",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="sound_system",
            node_executable="sound_system",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="control_system",
            node_executable="turn",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="control_system",
            node_executable="find_speaker",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="image_system",
            node_executable="image_system",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="realsense_ros2_camera",
            node_executable="realsense_ros2_camera",
            output="screen"
        ),
        launch_ros.actions.Node(
            package="spr_cic",
            node_executable="CIC",
            output="screen"
        ),
    ])
