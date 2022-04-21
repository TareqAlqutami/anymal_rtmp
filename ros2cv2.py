#!/usr/bin/env python
from __future__ import print_function

import roslib
#roslib.load_manifest('anymal_rtmp')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from vidgear.gears import WriteGear


rtmp_url = "rtmp://media.inference.asia/live/stream1"

# define required FFmpeg optimizing parameters for your writer
# [NOTE]: Added VIDEO_SOURCE as audio-source, since YouTube rejects audioless streams!
# output_params = {
#     "-i": VIDEO_SOURCE,
#     "-acodec": "aac",
#     "-ar": 44100,
#     "-b:a": 712000,
#     "-vcodec": "libx264",
#     "-preset": "medium",
#     "-b:v": "4500k",
#     "-bufsize": "512k",
#     "-pix_fmt": "yuv420p",
#     "-f": "flv",
# }

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image,queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/webcam/image_raw",Image,self.callback)

    self.writer = WriteGear(output_filename = rtmp_url,logging=True,) #Define writer 

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data) #, "rgb8")
      self.writer.write(cv_image)
    except CvBridgeError as e:
      # safely close writer
      self.writer.close()
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)


