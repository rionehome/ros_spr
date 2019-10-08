import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from time import sleep

class CIC(Node):
    def __init__(self):
        super().__init__("CIC")

        self.create_subscription(String, "/cerebrum/command", self.receive, 10)

        self.timer = self.create_timer(2.0, self.state)

        self.data = String()

        sleep(1)

        self.tasks = {
                "1": ["sound", "count"],
                "2": ["control", "turn"]
        }

        self.executing = "1"
        self.did = "0"

    def state(self):
        for number, task in self.tasks.items():
            self.executing = number
            if self.executing != self.did:
                self.send(task[0], task[1])
            self.did = self.executing
            break

    def receive(self, msg):
        flag = int(msg.data.split(",")[0].split(":")[1])

        if flag == 0:
            self.tasks.pop(self.executing)

    def send(self, topic, Command):
        self.sound_system_pub = self.create_publisher(
                String,
                "/"+topic+"_system/command",
                10
        )

        sleep(1)

        self.data.data = "Command:" + Command
        self.sound_system_pub.publish(self.data)

def main():
    rclpy.init()

    node = CIC()

    rclpy.spin(node)

if __name__ == "__main__":
    main()
