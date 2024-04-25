####Fibonacci_client.py
#! /usr/bin/env python3
from __future__ import print_function
import rospy
# Brings in the SimpleActionClient
import actionlib
# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import my_actionlib_tutorials.msg
def fibonacci_client():
 # Creates the SimpleActionClient, passing the type of the action
 # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('fibonacci',my_actionlib_tutorials.msg.FibonacciAction)
 # Waits until the action server has started up and started
 # listening for goals.
    client.wait_for_server()
 # Creates a goal to send to the action server.
    goal = my_actionlib_tutorials.msg.FibonacciGoal(order=20)
 # Sends the goal to the action server.
    client.send_goal(goal)
 # Waits for the server to finish performing the action.
    client.wait_for_result()
 # Prints out the result of executing the action
    return client.get_result() # A FibonacciResult
if __name__ == '__main__':
    try:
 # Initializes a rospy node so that the SimpleActionClientcan
 # publish and subscribe over ROS.
        rospy.init_node('fibonacci_client_py')
        result = fibonacci_client()
        print("Result:", ', '.join([str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        print("program interrupted before completion",file=sys.stderr)

####Fibonacci_server.py
#! /usr/bin/env python3
import rospy
import actionlib
import my_actionlib_tutorials.msg
class FibonacciAction(object):
 # create messages that are used to publish feedback/result
 _feedback = my_actionlib_tutorials.msg.FibonacciFeedback()
 _result = my_actionlib_tutorials.msg.FibonacciResult()
 def __init__(self, name):
 self._action_name = name
 self._as = actionlib.SimpleActionServer(self._action_name,
my_actionlib_tutorials.msg.FibonacciAction,
execute_cb=self.execute_cb, auto_start = False)
 self._as.start()

 def execute_cb(self, goal):
 # helper variables
 r = rospy.Rate(1)
 success = True

 # append the seeds for the fibonacci sequence
 self._feedback.sequence = []
 self._feedback.sequence.append(0)
 self._feedback.sequence.append(1)

 # publish info to the console for the user
 rospy.loginfo('%s: Executing, creating fibonacci sequence of order %i with seeds %i, %i' % (self._action_name, goal.order,
self._feedback.sequence[0], self._feedback.sequence[1]))

 # start executing the action
 for i in range(1, goal.order):
 # check that preempt has not been requested by the client
    if self._as.is_preempt_requested():
        rospy.loginfo('%s: Preempted' % self._action_name)
        self._as.set_preempted()
        success = False
        break

    self._feedback.sequence.append(self._feedback.sequence[i] +
    self._feedback.sequence[i-1])
 # publish the feedback
    self._as.publish_feedback(self._feedback)
 # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
    r.sleep()

    if success:
        self._result.sequence = self._feedback.sequence
        rospy.loginfo('%s: Succeeded' % self._action_name)
        self._as.set_succeeded(self._result)

if __name__ == '__main__':
 rospy.init_node('fibonacci')
 server = FibonacciAction(rospy.get_name())
 rospy.spin()

#************************************************************************************
##Meters_to_feet_client.py

#!/usr/bin/env python3
import sys
import rospy
from my_robot_msgs.srv import ConvertMetresToFeet, ConvertMetresToFeetRequest, ConvertMetresToFeetResponse
def metres_to_feet_client(x):
 # First wait for the service to become available.
 rospy.loginfo("Waiting for service...")
 rospy.wait_for_service('metres_to_feet')
 try:
 # Create a service proxy.
 metres_to_feet = rospy.ServiceProxy('metres_to_feet',ConvertMetresToFeet)
 # Call the service here.
 service_response = metres_to_feet(x)
 print("I only got here AFTER the service call was completed!")
 # Return the response to the calling function.
 return service_response
 except rospy.ServiceException as e:
 print ("Service call failed: %s"%e)
if __name__ == "__main__":
 # Initialize the client ROS node.
 rospy.init_node("metres_to_feet_client", anonymous = False)
 # The distance to be converted to feet.
 dist_metres = 0.25
 rospy.loginfo("Requesting conversion of %4.2f m to feet"%(dist_metres))
 # Call the service client function.
 service_response = metres_to_feet_client(dist_metres)
 # Process the service response and display log messages accordingly.
 if(not service_response.success):
 rospy.logerr("Conversion unsuccessful! Requested distance in metres should be a positive real number.")
 else:
 rospy.loginfo("%4.2f(m) = %4.2f feet"%(dist_metres, service_response.distance_feet))
 rospy.loginfo("Conversion successful!")


##Meters_to_feet_server.py

#!/usr/bin/env python3

from my_robot_msgs.srv import ConvertMetresToFeet,ConvertMetresToFeetRequest, ConvertMetresToFeetResponse
import rospy
import numpy as np
_CONVERSION_FACTOR_METRES_TO_FEET = 3.28 # Metres -> Feet conversionfactor.
# Service callback function.
def process_service_request(req):
 # Instantiate the response message object.
 res = ConvertMetresToFeetResponse()
 # Perform sanity check. Allow only positive real numbers.
 # Compose the response message accordingly.
 if(req.distance_metres < 0):
 res.success = False
 res.distance_feet = -np.Inf # Default error value.
 else:
 res.distance_feet = _CONVERSION_FACTOR_METRES_TO_FEET * req.distance_metres
 res.success = True
 #Return the response message.
 return res
def metres_to_feet_server():
 # ROS node for the service server.
 rospy.init_node('metres_to_feet_server', anonymous = False)
 # Create a ROS service type.
 service = rospy.Service('metres_to_feet', ConvertMetresToFeet,
process_service_request)
 # Log message about service availability.
 rospy.loginfo('Convert metres to feet service is now available.')
 rospy.spin()
if __name__ == "__main__":
 metres_to_feet_server()

#***************************************************************************************************

###Word_count_client.py
#!/usr/bin/env python3
import rospy
from my_robot_msgs.srv import WordCount
import sys
rospy.init_node('service_client')
rospy.wait_for_service('word_count')
word_counter = rospy.ServiceProxy('word_count', WordCount)
words = ' '.join(sys.argv[1:])
word_count = word_counter(words)
print(words, '->', word_count.count)

###Word_count_server.py
#!/usr/bin/env python3
import rospy
from my_robot_msgs.srv import WordCount,WordCountResponse
def count_words(request):
 return WordCountResponse(len(request.words.split()))
rospy.init_node('service_server')
service = rospy.Service('word_count', WordCount, count_words)
rospy.spin()

# WordCount.srv
string words
---
int32 count



