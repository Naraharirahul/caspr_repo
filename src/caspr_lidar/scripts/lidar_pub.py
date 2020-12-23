#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Float32MultiArray
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import LinkStates
import tf.transformations

def pose_function(msg):
    vel = Twist()
    data = msg.data
    vel.linear.x = data[0]
    vel.linear.y = data[1] 
    vel.linear.z = data[2] 
    vel.angular.x = data[3] 
    vel.angular.y = data[4] 
    vel.angular.z = data[5] 

    odom_pub.publish(vel)


if __name__ == '__main__':

    rospy.init_node('lidar_Caspr',anonymous=True)
    rospy.Subscriber("/joint_vel",Float32MultiArray,pose_function,queue_size=1000)   
    r = rospy.Rate(60) #Hz
    odom_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    while not rospy.is_shutdown():
        r.sleep()