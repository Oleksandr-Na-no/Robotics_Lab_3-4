"""Figure-8 path - STUDENT TASK.

You have square_path.py and circle_path.py as base.
Implement a figure-8: two circles, first turning left, then turning right.

Hint: A figure-8 = circle left + circle right. Use the same timed motion
as circle_path (linear.x + angular.z for duration = 2*pi/|w|).
"""
import time
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from .diff_drive_math import twist_to_wheel_speeds

class Figure8Path(Node):
    def __init__(self):
        super().__init__('figure_8_path')

        self.declare_parameter("linear_speed", 0.3)
        self.declare_parameter("angular_speed", 0.4)
        self.declare_parameter("wheel_radius", 0.15)
        self.declare_parameter("wheel_separation", 0.7)
        self.declare_parameter("rate_hz", 20.0)

        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        v = float(self.get_parameter("linear_speed").value)
        w = float(self.get_parameter("angular_speed").value)
        dt = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)

        wheel_r = float(self.get_parameter("wheel_radius").value)
        wheel_s = float(self.get_parameter("wheel_separation").value)
        wl, wr_val = twist_to_wheel_speeds(v, w, wheel_r, wheel_s)

        duration = 2.0 * math.pi / max(abs(w), 1e-6) + 4
        self.get_logger().info(f"Circle: v={v:.2f}, w={w:.2f}, t={duration:.2f}s | wheel ω: L={wl:.2f}, R={wr_val:.2f}")

        msg = TwistStamped()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = v
        msg.twist.angular.z = w

        t_end = time.time() + duration
        while time.time() < t_end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)


        msg.twist.angular.z = -w

        t_end = time.time() + duration
        while time.time() < t_end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)

        self.pub.publish(TwistStamped())
        self.get_logger().info("Complete.")

        # self.get_logger().info("Figure-8 path - TODO: implement using circle_path logic")
        # self.get_logger().info("Hint: run circle left (w>0), then circle right (w<0)")
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = Figure8Path()
    rclpy.shutdown()
