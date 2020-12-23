#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include "geometry_msgs/Twist.h"
#include "nav_msgs/Odometry.h"
#include <iostream>

// tf::TransformBroadcaster broadcaster;

// void odom_callback(const nav_msgs::Odometry &msg)
// {
//   std::cout<< "ddd tf sent" << std:: endl;
//   double x_pos = msg.pose.pose.position.x;
//   double y_pos =  msg.pose.pose.position.y;
//   double z_pos =  msg.pose.pose.position.z; 

//   double w_or = msg.pose.pose.orientation.w;
//   double x_or = msg.pose.pose.orientation.x;
//   double y_or = msg.pose.pose.orientation.y;
//   double z_or = msg.pose.pose.orientation.z;

//   tf::TransformBroadcaster broadcaster;

//   // std::cout<< "tf sent" << std:: endl;
    
//   broadcaster.sendTransform(tf::StampedTransform(
//         tf::Transform(tf::Quaternion(w_or, x_or, y_or, z_or), tf::Vector3(x_pos, y_pos, z_pos)),
//         ros::Time::now(),"base_link", "odom"));
// }

int main(int argc, char** argv){
  ros::init(argc, argv, "lidar_tf_publisher");
  ros::NodeHandle n;

  ros::Rate r(100);

  tf::TransformBroadcaster broadcaster;

  // ros::Subscriber sub = n.subscribe("/odom", 1000, odom_callback);
  
  // std::cout<< "tf sent" << std:: endl;

  while(n.ok()){

    
    // ros::Subscriber sub = n.subscribe("/odom", 1000, odom_callback);   
    broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0, 0, 0)),
        ros::Time::now(),"base_link", "velodyne_base_link")); 
    // broadcaster.sendTransform(
    //   tf::StampedTransform(
    //     tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.1, 0.0, 0.2)),
    //     ros::Time::now(),"base_link", "velodyne_base_link"));

    r.sleep();
  }
}