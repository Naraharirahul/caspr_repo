#!/usr/bin/env python
#Subscribes to the velocity that is being published from CASPR in MATLAB
import rospy
import time
import matplotlib.pyplot as ml
from std_msgs.msg import Float32MultiArray
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import LinkStates
import tf.transformations

global tf_data
tf_data = 0
global x_trans_error
global y_trans_error
global z_trans_error

global x_rot_error
global y_rot_error
global z_rot_error
global w_rot_error
global quarternion_transform

x_trans_error = 0
x_rot_error = 0
y_rot_error = 0
y_trans_error = 0
z_rot_error = 0
z_trans_error = 0
quarternion_transform = 0
global gazebo_tf_data
gazebo_tf_data = 0


def linkstates_function(msg):

    global gazebo_tf_data
    global x_trans_error
    global y_trans_error
    global z_trans_error

    global x_rot_error
    global y_rot_error
    global z_rot_error
    global w_rot_error

    gazebo_tf_data = msg.pose[1] 

def tf_function(msg):
    global tf_data
    global x_trans_error
    global y_trans_error
    global z_trans_error

    global x_rot_error
    global y_rot_error
    global z_rot_error
    global w_rot_error

    global quarternion_transform

    if(msg.transforms[0].child_frame_id == "Spatial Manipulator"):
        tf_data = msg.transforms[0].transform

    x_trans_error = tf_data.translation.x - gazebo_tf_data.position.x
    y_trans_error = tf_data.translation.y - gazebo_tf_data.position.y
    z_trans_error = tf_data.translation.z - gazebo_tf_data.position.z + 0.15

    x_rot_error = tf_data.rotation.x - gazebo_tf_data.orientation.x
    y_rot_error = tf_data.rotation.y - gazebo_tf_data.orientation.y
    z_rot_error = tf_data.rotation.z - gazebo_tf_data.orientation.z
    w_rot_error = tf_data.rotation.w - gazebo_tf_data.orientation.w

    quarternion_transform = tf.transformations.euler_from_quaternion((x_rot_error, y_rot_error, z_rot_error, w_rot_error))

xii = []
yii = []
i = 0                                                   

def pose_function(msg):
    global i
    global xii, yii
    vel = Twist()

    i = i + 1
    data = msg.data

    if i == 100:
        print(i)
        ml.plot(xii)
        ml.show()


    # for i in range(0,101):

    vel.linear.x = data[3*i]
    vel.linear.y = data[3*i+1]
    vel.linear.z = data[3*i+2]
    vel.angular.z = 0
    vel.angular.x = 0
    vel.angular.y = 0

    xii.append(vel.linear.x)
    yii.append(vel.linear.y)

    # print("y",vel.linear.y)
    

    # if i > 300:
    #     print(i)
    #     vel.linear.x = 0
    #     vel.linear.y = 0
    #     vel.linear.z = 0

    odom_pub.publish(vel)


if __name__ == '__main__':

    rospy.init_node('caspr_vel',anonymous=True)
    # x_val = rospy.get_param("x_val")
    # y_val = rospy.get_param("y_val")
    # z_val = rospy.get_param("z_val")
    rospy.Subscriber("/joint_vel",Float32MultiArray,pose_function,queue_size=1000)
    r = rospy.Rate(3) #Hz
    
    while not rospy.is_shutdown():
        odom_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        r.sleep()

        