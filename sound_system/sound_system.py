import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from module import module_angular
from module import module_QandA
from module import module_pico
from module import module_detect
from module import module_count

from std_msgs.msg import String
from time import sleep

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')

        self.command = None

        self.create_subscription(
            String, 'sound_system/command',
            self.command_callback,
            10
        )

        self.senses_publisher = self.create_publisher(
            String,
            'cerebrum/command',
            10
        )

        self.angular_publisher = self.create_publisher(
            String, 'control/command',
            10
        )


    # recieve a command {Command, Content}
    def command_callback(self, msg):

        self.command = msg.data
        command = msg.data.split(',')

        # Speak a content
        if 'speak' == command[0].replace('Command:', ''):
            if module_pico.speak(command[1].replace('Content:', '')) == 1:
                self.cerebrum_publisher('Return:0,Content:None')

        # Detect hotword, "hey ducker"
        if 'detect' == command[0].replace('Command:', ''):
            print('detect',flush=True)
            if module_detect.detect() == 1:
                self.cerebrum_publisher('Return:0,Content:None')

        # Start 10 counts
        if 'count' == command[0].replace('Command:', ''):
            if module_count.count() == 1:
                self.cerebrum_publisher('Return:0,Content:None')

        # Sound localization
        if 'angular' == command[0].replace('Command:', ''):
            self.return_list = module_angular.angular()
            self.temp_angular = self.return_list[0]
            if self.temp_angular > 0:
                # "Return:1,Content:angular,saying words"
                self.turnnig_publisher(
                    'Command:find,Content:'+str(self.temp_angular))

        # Speak answer at answering with rurnning
        if 'finish' == command[0].replace('Command:', ''):
            if module_pico.speak(self.return_list[1]) == 1:
                self.cerebrum_publisher('Return:0,Content:None')

        # Start QandA, an act of repeating 5 times, content is times (ex; 5 times >> 5)
        content = 0
        if 'QandA' == command[0].replace('Command:', ''):
            content = command[1].replace('Content:', '')
            if "|" in str(content):
                if module_QandA.QandA(content) == 1:
                    self.cerebrum_publisher('Retern:0,Content:None')
            else:
                content = int(content)
                if module_QandA.QandA(content) == 1:
                    self.cerebrum_publisher('Retern:0,Content:None')

    # Publish a result of an action
    def cerebrum_publisher(self, message):
        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)

    # Publish a result of an action
    def turnnig_publisher(self, message):
        _trans_message = String()
        _trans_message.data = message

        self.angular_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)


def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
