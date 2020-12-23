Introduction
------------
------------

This is a github repository containing all the files required to simulate a Lidar to move in the same velocity as that of a cable robot in CASPR simulation.
It has been tested on the following versions of ROS and MATLAB.

ROS : Melodic
MATLAB: 2020b

Following steps needs to be performed to make the lidar follow the trajectory of the cable robot.

Step 1:
------
git clone this repository into a local catkin workspace.

Step 2:
-------
In your Ubuntu system install MATLAB and then change the path in Matlab to the CASPR folder in the repo you have just cloned. Start CASPR by running the initialise_CASPR.m file in MATLAB.

Step 3:
-------
Note the IP of the platform that you installed CASPR by ifconfig (Linux).
Call the following function to set the config of CASPR-RViz interface in CASPR:
CASPRRViz_configuration.SetROSConfig('[caspr-rviz IP]','[caspr IP]');
where [caspr-rviz IP] refers to the IP of your CASPR-RViz platform, and [caspr IP] refers to the IP of your CASPR platform. If both are running in same platform then they will be the same. 
After setting up at the MATLAB side, enter CASPR_GUI in the MATLAB command prompt.

Step 4:
-------
At the ROS end, catkin_make the workspace in which the the files are recently cloned. 
On the terminal, run the following command which would start the caspr-rviz interface. 

```ruby
roslaunch caspr_rviz caspr.launch
```
This will launch a new RVIZ window where the cable robot is visualized.

Step 5:
-------
On another terminal run the following command, which opens a gazebo environment with a lidar spawning.
```ruby
roslaunch caspr_lidar sim.launch
```
To run the HDL_Slam algorithm, open a new terminal and then run the following command
```ruby
roslaunch hdl_graph_slam hdl_graph_slam.launch
```
A new rviz window needs to be opened by running rviz rviz in a new terminal. Add point cloud 2 in the rviz and then select the topic hdl_graph_slam/map_points.
The lidar point cloud will then be seen.

Step 6:
-------
Once all the environments and packages have been launched, the lidar in gazebo which at (0,0,0) has to be moved to cable robot's end effector's initial position. 

For the UR3 robot, this position has been written in the move.py file (for another robot, it has to be changed). 
Before running any inverse kinematics solver, the lidar has to move to the initial position of the end effector and this can be acheived my running the followinf command.
```ruby
rosrun caspr_lidar move.py
```
Once the lidar reaches the initial position of the end effector, terminate the terminal which has the move.py running.

In the CASPR_GUI, click on the kinematics which opens a new window. In the trajectory drop down, make sure circle_end effector is selected. 
Click on the run button which runs a kinematics solver. After it has successfully finished running, click on the Rviz button which would communicate the velocity data of the end effector to ROS.

It can be seen that both the lidar in gazebo and the cable robot in rviz are moving in the same path. 

By using this flow, the cable robot can map the environment.
