#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import PointCloud2
import math
import sensor_msgs.point_cloud2 as pc2

last_x = None
last_y = None
last_time = None

def odom_callback(odom_msg):
    global last_x
    global last_y
    global last_time
    rospy.loginfo("Got an Odom message t=%sns, x=%s, y=%s" % (odom_msg.header.stamp, odom_msg.pose.pose.position.x, odom_msg.pose.pose.position.y))
    if last_x != None:
        x_diff = last_x - odom_msg.pose.pose.position.x
        y_diff = last_y - odom_msg.pose.pose.position.y
        time_diff = (odom_msg.header.stamp - last_time).to_sec()
        dist = math.sqrt(math.pow(x_diff,2) + math.pow(y_diff,2))
        rospy.loginfo("Diff x=%s, y=%s, t=%s, dist=%s, speed=%sm/s" %(x_diff, y_diff, time_diff, dist, dist/time_diff))
    last_x = odom_msg.pose.pose.position.x
    last_y = odom_msg.pose.pose.position.y
    last_time = odom_msg.header.stamp


def cloud_callback(cloud_msg):
    rospy.loginfo("Got an cloud message %s " % cloud_msg.header.stamp)
    points = ()
    for p in pc2.read_points(cloud_msg, field_names = ("x", "y", "z"), skip_nans=True):
      rospy.loginfo(" x : %f  y: %f  z: %f" %(p[0],p[1],p[2]))
      points.append((p[0],p[1],p[2]))
       

def listener():
    rospy.loginfo("Started parser")
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("odom", Odometry, odom_callback)
    rospy.Subscriber("/cloud_filtered", PointCloud2, cloud_callback)

    rospy.spin()

if __name__ == '__main__':
    listener()