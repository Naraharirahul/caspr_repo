#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
x = 0
y = 0
z = 0
roll = 0 
pitch = 0
yaw = 0
def Odom(msg):

    global x
    global y
    global z
    global roll
    global pitch
    global yaw

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    z = msg.pose.pose.position.z

    rot_q = msg.pose.pose.orientation
    (roll, pitch, yaw) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


rospy.init_node("move_robot")

sub = rospy.Subscriber("/odom", Odometry, Odom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=100)

speed = Twist()

r = rospy.Rate(4)

target_x = 1.4450
target_y = 1.0005
target_z = 0.9025

while not rospy.is_shutdown():
    
    diff_x = target_x - x
    diff_y = target_y - y    
    diff_z = target_z - z

    angle_to_target = atan2(diff_y, diff_x)


    if (abs(diff_z) > 0.01):
        speed.linear.z = 0.1
        speed.linear.x = 0
        speed.linear.y = 0


    elif(abs(diff_x) > 0.01):
        speed.linear.x = 0.1
        speed.linear.z = 0
        speed.linear.y = 0

    elif(abs(diff_y) > 0.01):
        speed.linear.y = 0.1
        speed.linear.z = 0
        speed.linear.x = 0

    else:
        speed.linear.z = 0
        speed.linear.x = 0
        speed.linear.y = 0

    pub.publish(speed)

    r.sleep()

