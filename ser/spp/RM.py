#Creating a new package separately for Message Definition
catkin_create_pkg my_robot_msgs roscpp rospy std_msgs

#Remove include and src folder
lab22@205A-scope--36:~/catkin_ws/src/my_robot_msgs$ rm -rf include/
lab22@205A-scope--36:~/catkin_ws/src/my_robot_msgs$ rm -rf src/

#Open package.xml
#Add the following two lines as seen in the screenshot
<build_depend>message_generation</build_depend>
<exec_depend>message_runtime</exec_depend>

#in ~/catkin_ws/src/my_robot_msgs$ nano CMakeLists.txt Adding message_generation 
find_package(catkin REQUIRED COMPONENTS
roscpp
rospy
std_msgs
message generation
)

#uncomment the following
generate messages(
DEPENDENCIES
std_msgs
)

#uncomment the following and update
catkin_package(
#INCLUDE_DIRS include
#LIBRARIES my_robot_msgs
CATKIN DEPENDS roscpp rospy std_msgs message_runtime
#DEPENDS system_lib
)

#in catkin_ws/src/my_robot_msgs$ mkdir msg
#inside it make:
#catkin_ws/src/my_robot_msgs/msg$ touch HardwareStatus.msg
#add the following content:
int64 temperature
bool are_motors_up
string debug_message

#uncomment in the cmakelist
add_message_files(
FILES
HardwareStatus.msg
)

#in :~/catkin_ws/devel/include/my_robot_msgs a header file will be created automatically

#now in :~/catkin_ws/src/my_robot_tutorials Open package.xml in my_robot_tutorials and add the following
<depend>my_robot_msgs</depend>

#in cmakelist add
find_package(catkin REQUIRED COMPONENTS
roscpp
rospy
std_msgs
my_robot_msgs
)

#create a script folder, inside make a publisher.py file

#!/usr/bin/env python3
import rospy
from my_robot_msgs.msg import HardwareStatus
if __name__ == '__main__':
        rospy.init_node("hardware_status_publisher")
        pub = rospy.Publisher("/my_robot/hardware_status", HardwareStatus, queue_size=10)
        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
                msg = HardwareStatus()
                msg.temperature = 45
                msg.are_motors_up = True
                msg.debug_message = "Hello World"
                pub.publish(msg)
                rate.sleep()
#to run
rosrun my_robot_tutorials publisher.py
rostopic echo /my_robot/hardware_status
