import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Bool
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

        self.resetPose = self.create_publisher(
            Bool,
            "/turtlebot2/commands/reset_pose",
            10
        )

        self.flag_publisher_cerebrum = self.create_publisher(
            String,
            "/cerebrum/command",
            10
        )

        self.flag_publisher_sound = self.create_publisher(
            String,
            "/sound_system/command",
            10
        )

        self.create_subscription(
            Odometry,
            "/turtlebot2/odometry",
            self.sendVelocity,
            10
        )

        self.create_subscription(
            String,
            "/control_system/command",
            self.receiveFlag,
            10
        )

        sleep(1)

        self.velocity = Twist()
        self.velocity.angular.z = 0.0

        self.setVelocity = False
        self.did = False

        self.degree = None

    def sendVelocity(self, msg):
        w = msg.pose.pose.orientation.w
        z = msg.pose.pose.orientation.z

        angle = 0

        if z > 0:
            angle = -arccos(w)*360 / pi
        else:
            angle =  arccos(w)*360 / pi

        try:
            # if reach target angular
            if 0 <= int(self.degree) and int(self.degree) < 180:
                #print("0 ~ 180 , target={0} now={1}".format(self.degree, angle), flush=True)

                if int(self.degree)-5 < angle and angle < int(self.degree)+5:

                    self.velocity.angular.z = 0.0

                    # if not send finish flag to sender
                    if self.did == False:
                        print("[*] STOP TURN {0} DEGREE".format(self.degree), flush=True)

                        # send finish flag to sender
                        if self.sender == "sound":
                            self.sendFinishFlag("sound_system", "Command:finish,Content:None")

                        if self.sender == "cerebrum":
                            self.sendFinishFlag("cerebrum", "Command:{0},Content:None".format(self.Command))

                        self.did = True
                        self.setVelocity = False

            if -180 <= int(self.degree) and int(self.degree) < 0:
                #print("-180 ~ 0 , target={0} now={1}".format(self.degree, angle), flush=True)

                if int(self.degree)-5 < angle and angle < int(self.degree)+5:

                    self.velocity.angular.z = 0.0

                    # if not send finish flag to sender
                    if self.did == False:
                        print("[*] STOP TURN {0} DEGREE".format(self.degree), flush=True)

                        # send finish flag to sender
                        if self.sender == "sound":
                            self.sendFinishFlag("sound_system", "Command:finish,Content:None")

                        if self.sender == "cerebrum":
                            self.sendFinishFlag("cerebrum", "Command:{0},Content:None".format(self.Command))

                        self.did = True
                        self.setVelocity = False

        except TypeError:
            pass

        if self.setVelocity == True:
            if -180 <= int(self.degree) and int(self.degree) < 0:
                self.velocity.angular.z = 30.0
            else:
                self.velocity.angular.z = -30.0

        self.turn.publish(self.velocity)

    def receiveFlag(self, msg):
        self.Command, Contents = msg.data.split(",")

        Contents = Contents.split(":")
        self.degree = int(Contents[1])

        if 0 < self.degree and self.degree <= 180:
            self.degree *= -1
        else:
            self.degree = 360 - self.degree

        self.sender = Contents[2]

        print(self.degree, flush=True)

        self.Command = self.Command.split(":")[1]

        if self.Command == "turn":
            reset_flag = Bool()
            reset_flag.data = True
            self.did = False
            self.resetPose.publish(reset_flag)

            self.setVelocity = True
            print("[*] START TURN {0} DEGREE".format(self.degree), flush=True)

    def sendFinishFlag(self, topic, content):

        if topic == "sound_system":

            self.flag = String()
            self.flag.data = content + ":control_system"

            self.flag_publisher_sound.publish(self.flag)

            self.flag.data = "Command:angular,Content:None"

            self.flag_publisher_cerebrum.publish(self.flag)


        elif topic == "cerebrum":

            self.flag = String()
            self.flag.data = content + ":control_system"

            self.flag_publisher_cerebrum.publish(self.flag)


def main():
    rclpy.init()

    node = Turn()

    rclpy.spin(node)


if __name__ == "__main__":
    main()
