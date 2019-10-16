from detect_modules.detect_human.detect_human import detect_human

from detect_modules.detect_sex.detect_sex import detect_sex

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge

from time import sleep


class ImageSystem(Node):
    def __init__(self):
        super(ImageSystem, self).__init__('ImageSystem')

        self.senses_publisher = self.create_publisher(
                                    String,
                                    'cerebrum/command',
                                    10
                                    )

        self.create_subscription(
                String,
                '/image_system/command',
                self.command_callback,
                10
        )

        self.create_subscription(
                Image,
                '/camera/color/image_raw',
                self.get_image,
                10
        )

        self.message = None
        self.command = None
        self._trans_message = String()

        self.bridge = CvBridge()

        sleep(1)

    def command_callback(self, msg):

        # contain command data
        self.command = msg.data

        # Command:speak , Content:hello!
        command = msg.data.split(',')

        if 'capture' == command[0].replace('Command:', ''):
            print("HUMAN : {0}".format(self.detect_human()), flush=True)
            print("SEX : {0}".format(self.detect_sex()), flush=True)

            #self.cerebrum_publisher('Return:1,Content:'+self.message)
        if 'sex' == command[0].replace('Command:', ''):
            self.message = self.detect_sex()
            self.cerebrum_publisher('Return:1,Content:'+self.message)
        if 'object' == command[0].replace('Command:', ''):
            self.detect_object()

    # detect number's human
    def detect_human(self):
        number = detect_human(self.image)
        print(number)
        return number

    # detect human sex
    def detect_sex(self):
        woman, man = detect_sex(self.image)
        return woman + '|' + man

    # send data to cerebrum
    def cerebrum_publisher(self, message):

        self._trans_message.data = message
        self.senses_publisher.publish(self._trans_message)

    # get image from realsense
    def get_image(self, msg):
        self.image = self.bridge.imgmsg_to_cv2(msg)

    # only one time execute
    def one_time_execute(self, now, previous):
        flag = False

        if now != previous:
            flag = True

        return flag


def main():
    rclpy.init()
    node = ImageSystem()
    rclpy.spin(node)

if __name__ == "__main__":
    main()
