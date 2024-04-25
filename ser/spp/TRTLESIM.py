#add the following to package.xml
<build_depend>geometry_msgs</build_depend>
<build_export_depend>geometry_msgs</build_export_depend>
<exec_depend>geometry_msgs</exec_depend>

#for circle
import rospy
fron geometry_nsgs.msg import Twist

if __name__=='__main__':
    rospy.init_node("draw_circle")
    rospy.loginfo( "started " )

    pub=rospy. publisher( "/turtle/cmd_vel" , Twist , queue_size=10)
    rate=rospy.Rate(5       )
    while not rospy.is_shutdown():
        msg=Twist()
        msg.linear.x=2
        msg.angular.z=2
        pub. publish(msg)
        rate. steep( )

#for square
import rospy
from geometry_msgs.msg import Twist

if __name__=='__main__':
    rospy.init_node("draw_square")
    rospy.loginfo("Started drawing square")

    pub = rospy.Publisher("/turtle/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(0.5)  # Adjust the rate for slower motion, if needed

    # Length of one side of the square
    side_length = 2

    # Angular velocity for turning
    angular_speed = 0.5

    # Linear velocity for moving straight
    linear_speed = 1

    for _ in range(4):  # Iterate 4 times for each side of the square
        # Move forward (linear motion)
        msg = Twist()
        msg.linear.x = linear_speed
        pub.publish(msg)
        rospy.sleep(side_length / linear_speed)  # Time = Distance / Speed

        # Stop
        msg.linear.x = 0
        pub.publish(msg)

        # Turn right (angular motion)
        msg.angular.z = angular_speed
        pub.publish(msg)
        rospy.sleep(1)  # Adjust this sleep time for the turtle to turn 90 degrees
        msg.angular.z = 0  # Stop turning
        pub.publish(msg)

        rate.sleep()  # Wait to maintain a constant rate

    rospy.loginfo("Square drawn")

#for triangle
import rospy
from geometry_msgs.msg import Twist
import math

if __name__=='__main__':
    rospy.init_node("draw_triangle")
    rospy.loginfo("Started drawing triangle")

    pub = rospy.Publisher("/turtle/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(0.5)  # Adjust the rate for slower motion, if needed

    # Length of one side of the equilateral triangle
    side_length = 2

    # Angular velocity for turning
    angular_speed = 1.047  # Corresponds to 60 degrees in radians (equivalent to pi/3)

    # Linear velocity for moving straight
    linear_speed = 1

    for _ in range(3):  # Iterate 3 times for each side of the triangle
        # Move forward (linear motion)
        msg = Twist()
        msg.linear.x = linear_speed
        pub.publish(msg)
        rospy.sleep(side_length / linear_speed)  # Time = Distance / Speed

        # Stop
        msg.linear.x = 0
        pub.publish(msg)

        # Turn right (angular motion)
        msg.angular.z = angular_speed
        pub.publish(msg)
        rospy.sleep(1)  # Adjust this sleep time for the turtle to turn 60 degrees
        msg.angular.z = 0  # Stop turning
        pub.publish(msg)

        rate.sleep()  # Wait to maintain a constant rate

    rospy.loginfo("Triangle drawn")

#to get it coordinates we need to make subscriber.py
import rospy
from turtlesim.msg import Pose

def pose_callback(msg: Pose):
    rospy.loginfo("("+ str(msg.x)+","+ str(msg.y) +")")

if __name__=="__main__":
    rospy.init_node("pose _ subscriber")
    sub=rospy.Subscriber("/turtlel/pose",Pose,callback=pose_callback)
    rospy.loginfo("node has been started")
    rospy. spin()

#to run this
roscore
python3 draw_circle.py
python3 subscriber.py
rosrun turtlesim turtlesim_node