#USING A ROS SERVICES
#in my_robot_tutorials/src make a srv directory. In this srv directory make a file name AddTwoInts.srv with following content
int64 A
int64 B
---
int64 Sum

#open package.xml, add these two lines in it
 <build_depend>message_generation</build_depend>
 <exec_depend>message_runtime</exec_depend>

#Open CMakeLists.txt Add message_generation as component in find_package
# Do not just add this line to your CMakeLists.txt, modify the existing line
find_package(catkin REQUIRED COMPONENTS
 roscpp
 rospy
 std_msgs
 message_generation
)

#Uncomment the add_service_files and add these lines
add_service_files(
 FILES
 AddTwoInts.srv
)


#Writing server: scripts/add_two_ints_server.py
#!/usr/bin/env python
from __future__ import print_function
from my_robot_tutorials.srv import AddTwoInts,AddTwoIntsResponse
import rospy
def handle_add_two_ints(req):
 print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
 return AddTwoIntsResponse(req.a + req.b)
def add_two_ints_server():
 rospy.init_node('add_two_ints_server')
 s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
 print("Ready to add two ints.")
 rospy.spin()
if __name__ == "__main__":
 add_two_ints_server()


#Writing client: scripts/add_two_ints_client.py
#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
from my_robot_tutorials.srv import *
# Function to call the add_two_ints service
def add_two_ints_client(x, y):
 # Wait for the 'add_two_ints' service to become available
 rospy.wait_for_service('add_two_ints')
 try:
 # Create a proxy to the 'add_two_ints' service
    add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
 # Call the service with provided arguments x and y
    resp1 = add_two_ints(x, y)
 # Return the sum obtained from the service response
    return resp1.sum
 except rospy.ServiceException as e:
 # Print an error message if service call fails
    print("Service call failed: %s" % e)
# Function to provide usage instructions
def usage():
 return "%s [x y]" % sys.argv[0]
if __name__ == "__main__":
 # Check if two arguments are provided
    if len(sys.argv) == 3:
 # Parse arguments as integers
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
 # Print usage instructions and exit if incorrect number of arguments
        print(usage())
        sys.exit(1)
 # Print the request being made
    print("Requesting %s+%s" % (x, y))
 # Call the add_two_ints_client function and print the result
    print("%s + %s = %s" % (x, y, add_two_ints_client(x, y)))

