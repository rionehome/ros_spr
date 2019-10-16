import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

from numpy import arange, array
from numpy import argmin
from numpy import sqrt, cos, sin, deg2rad
from numpy import Inf

from matplotlib import pyplot as plt

class FindSpeaker(Node):
    def __init__(self):
        super().__init__("find_speaker")

        self.create_subscription(String, "/control_system/command", self.recieve_flag, 10)
        self.create_subscription(LaserScan, "/scan", self.recieve_points, 10)

        self.timer = self.create_timer(0.1, self.find)

        self.X = array([])
        self.Y = array([])

        self.angle_min = None
        self.angle_max = None
        self.angle_increment = None

        self.degree = None

        self.pos_x = None
        self.pos_y = None

    def recieve_points(self, msg):
        self.angle_min = msg.angle_min
        self.angle_max = msg.angle_max+msg.angle_increment
        self.angle_increment = msg.angle_increment

        angles = arange(msg.angle_min, msg.angle_max+msg.angle_increment, msg.angle_increment)
        ranges = array(msg.ranges)

        ranges[ranges<0.3] = Inf

        self.X = ranges*cos(angles)
        self.Y = ranges*sin(angles)

    def recieve_flag(self, msg):
        Command, Content = msg.data.split(",")

        if Command.split(":")[1] == "find":
            self.degree = int( Content.split(":")[1] )


    def find(self):

        if self.degree != None and self.X.any():
            min_degree = deg2rad(self.degree - 30)
            max_degree = deg2rad(self.degree + 30)

            angle = arange(self.angle_min, self.angle_max, self.angle_increment)
            angle[angle < min_degree] = Inf
            angle[max_degree < angle] = Inf

            self.X[angle == Inf] = Inf
            self.Y[angle == Inf] = Inf

            min_number = argmin( sqrt(self.X**2+self.Y**2) )
            self.pos_x = self.X[min_number]
            self.pos_y = self.Y[min_number]

            self.degree = None

        elif self.degree == None and self.pos_x != None:
            ranges = sqrt( (self.pos_x - self.X)**2 + (self.pos_y - self.Y)**2 )
            min_number = argmin(ranges)
            self.pos_x = self.X[min_number]
            self.pos_y = self.Y[min_number]

            plt.cla()
            plt.xlim(-5, 5)
            plt.ylim(-5, 5)
            plt.scatter(self.X, self.Y, s=0.5)
            plt.scatter(self.pos_x, self.pos_y)
            plt.pause(0.1)


def main():
    rclpy.init()

    node = FindSpeaker()

    rclpy.spin(node)


if __name__ == "__main__":
    main()
