#!/usr/bin/env python

import rospy 
from std_msgs.msg import Int32
import robotiq_gripper
from robotiq_hande_ros_driver.srv import gripper_service, gripper_serviceResponse

class HandEGripper:
    def __init__(self):
        rospy.init_node("hand_e_gripper_node", anonymous=False)
        # get the IP
        ip = rospy.get_param('~robot_ip')
        # initialize the gripper
        self.gripper = robotiq_gripper.RobotiqGripper()
        rospy.loginfo("Connecting to the gripper.....")
        self.gripper.connect(ip, 63352)
        rospy.loginfo("Activating the gripper.....")
        self.gripper.activate(auto_calibrate=False)
        # get speed and force
        self.speed = rospy.get_param('~speed', 255)
        self.force = rospy.get_param('~force', 255)
        self.sub = rospy.Subscriber("gripper_command", Int32, self.gripperCallback, queue_size=10)
        # set up server
        self.gripper_server = rospy.Service('gripper_service', gripper_service, self.serverCallback)
    
    def gripperCallback(self, data):
        rospy.loginfo("received topic data")
        rospy.loginfo(data.data)
        if data.data == 0:
            rospy.loginfo("closing the gripper. Speed={}, force={}".format(self.speed, self.force))
            self.gripper.move_and_wait_for_pos(255, self.speed, self.force)
        if data.data == 1:
            rospy.loginfo("opening the gripper. Speed={}, force={}".format(self.speed, self.force))
            self.gripper.move_and_wait_for_pos(0, self.speed, self.force)
    
    def serverCallback(self, request):
        if request.command == 0:
            rospy.loginfo("closing the gripper. Speed={}, force={}".format(self.speed, self.force))
            self.gripper.move_and_wait_for_pos(255, self.speed, self.force)
        if request.command == 1:
            rospy.loginfo("opening the gripper. Speed={}, force={}".format(self.speed, self.force))
            self.gripper.move_and_wait_for_pos(0, self.speed, self.force)
        return(gripper_serviceResponse(0))

if __name__ == '__main__':
    gripper_obj = HandEGripper()
    rospy.spin()