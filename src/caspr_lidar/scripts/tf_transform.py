#!/usr/bin/env python
import rospy
import tf
from tf2_msgs.msg import TFMessage
import tf.transformations
from nav_msgs.msg import Odometry



def tf_function(msg):

    if msg.child_frame_id == "base_link" and msg.header.frame_id == "odom" :

        x_pos = msg.pose.pose.position.x 
        y_pos =  msg.pose.pose.position.y 
        z_pos =  msg.pose.pose.position.z 

        w_or = msg.pose.pose.orientation.w
        x_or = msg.pose.pose.orientation.x
        y_or = msg.pose.pose.orientation.y
        z_or = msg.pose.pose.orientation.z

        odom_send = tf.TransformBroadcaster()
        odom_send.sendTransform((x_pos, y_pos, z_pos), (x_or, y_or, z_or,w_or), rospy.Time.now(), "base_link","odom")


if __name__ == '__main__':

    rospy.init_node('tf_publisher',anonymous=True)

    rospy.Subscriber("/odom",Odometry, tf_function, queue_size=100)
 
    r = rospy.Rate(60) #Hz
    while not rospy.is_shutdown():
        r.sleep()