#!/usr/bin/env python
import rospy
import time
import tf
from std_msgs.msg import Float32MultiArray
from gazebo_msgs.msg import LinkStates
from nav_msgs.msg import Odometry

def odom_pub(msg):

    message = msg.name
    for i in range(len(message)):
        if(message[i] == "lidar_sim::base_link"):
            
            x_pos = msg.pose[i].position.x 
            y_pos =  msg.pose[i].position.y
            z_pos =  msg.pose[i].position.z

            w_or = msg.pose[i].orientation.w
            x_or = msg.pose[i].orientation.x
            y_or = msg.pose[i].orientation.y
            z_or = msg.pose[i].orientation.z

            x_vel = msg.twist[i].linear.x
            y_vel =  msg.twist[i].linear.y
            z_vel =  msg.twist[i].linear.z 

            x_ang = msg.twist[i].angular.x
            y_ang = msg.twist[i].angular.y
            z_ang = msg.twist[i].angular.z 


            odom = Odometry()
            odom.header.stamp = rospy.Time.now()
            odom.header.frame_id = "odom"
            odom.child_frame_id = "base_link"
            odom.pose.pose.position.x = x_pos
            odom.pose.pose.position.y = y_pos
            odom.pose.pose.position.z = z_pos
             
            odom.pose.pose.orientation.x = x_or
            odom.pose.pose.orientation.y = y_or
            odom.pose.pose.orientation.z = z_or
            odom.pose.pose.orientation.w = w_or

            odom.twist.twist.linear.x = x_vel
            odom.twist.twist.linear.y = y_vel
            odom.twist.twist.linear.z = z_vel

            odom.twist.twist.angular.x = x_ang
            odom.twist.twist.angular.y = y_ang
            odom.twist.twist.angular.z = z_ang

            odom_pub.publish(odom)
            
  
if __name__ == '__main__':

    rospy.init_node('odom_publisher',anonymous=True)
    rospy.Subscriber("/gazebo/link_states",LinkStates, odom_pub) #, queue_size=100)

    r = rospy.Rate(30) #Hz
   
    while not rospy.is_shutdown():
        odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
        r.sleep()