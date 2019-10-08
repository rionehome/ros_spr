import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from time import sleep

from numpy import *

class Turn(Node):
    def __init__(self):
        super().__init__("Trun")

        self.turn = self.create_publisher(
                Twist,
                "/turtlebot2/commands/velocity",
                10
        )
        
        self.create_subscription(
                Odometry,
                "/turtlebot2/odometry",
                self.Send
        )

        self.create_subscription(
                String,
                "/control_system/command",
                self.Flag
        )

        self.cic_pub = self.create_pusbliher(
                String,
                "/cerebrum/command", 10
        )

        self.data = Twist()
        self.data.angular.z = 30.0

        self.cic_data = String()
        self.cic_data.data = "Return:0"

        self.flag = False

        sleep(1)


    def Send(self, msg):
        w = msg.pose.pose.orientation.w
        z = msg.pose.pose.orientation.z

        angle = 0

        if z > 0:
            angle = abs(1 - arccos(w)* 360 / pi)
        else:
            angle = abs(360 - arccos(w)* 360 / pi)

        if 350 > angle and angle > 180:
            self.data.angular.z = 0.0
            if self.flag:
                self.turn.publish(self.data)

            self.flag = False
            

    def Flag(self, msg):
        data = msg.data.split(":")[1]

        if data == "turn" and self.flag == False:
            self.flag = True
            print("START TURNING", flush=True)

def main():
    rclpy.init()

    node = Turn()

    rclpy.spin(node)

if __name__ == "__main__":
    main()
