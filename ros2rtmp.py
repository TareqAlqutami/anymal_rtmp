# import roslib
import roslib

roslib.load_manifest("anymal_rtmp")

# import other required libraries
import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from vidgear.gears import WriteGear, streamgear

# rtmp_url = "rtmp://media.inference.asia/live/stream1"
rtmp_url = "rtmp://192.168.0.94:1935/live/stream1"

# output_args_examples = ['ffmpeg',
#            '-y',
#            '-f', 'rawvideo',
#            '-vcodec', 'rawvideo',
#            '-pix_fmt', 'bgr24',
#            '-s', "{}x{}".format(640, 480),
#            '-i', '-',
#            '-c:v', 'libx264',
#         #    '-pix_fmt', 'yuv420p',
#            '-preset', 'ultrafast',
#            '-f', 'flv',
#            rtmp_url]

stream_params = {
    # "-input_framerate": 20,  # controlled framerate 
    "-vcodec": "libx264",
    "-preset": "ultrafast",
    # "-b:v": "4500k",
    '-c:v': 'libx264',

    # "-bufsize": "112k",
    # "-pix_fmt": "yuv420p",
    "-f": "flv",
    # "-tune": "zerolatency",
    "-crf":18 # Vary the CRF between around 18 and 24 — the lower, the higher the bitrate.
}
# custom publisher class
class image_subscriber:
    def __init__(self, output_filename):
        # create CV bridge
        self.bridge = CvBridge()
        # define publisher topic
        self.image_pub = rospy.Subscriber("/wide_angle_camera_rear/image_color", Image, self.callback)
        # self.image_pub = rospy.Subscriber("/webcam/image_raw", Image, self.callback)
        # Define writer with default parameters
        self.writer = WriteGear(output_filename=output_filename,logging=True, **stream_params)

    def callback(self, data):
        # convert recieved data to frame
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # check if frame is valid
        if cv_image is not None:
        
            # {do something with the frame here}
            # let's add a circle
            # (rows, cols, channels) = cv_image.shape
            # if cols > 60 and rows > 60:
                # cv2.circle(cv_image, (50, 50), 10, 255)

            # write frame to writer
            self.writer.write(cv_image)

            # cv2.imshow("Image window", cv_image)
            # cv2.waitKey(3)
            
        def close(self):
            # safely close video stream
            self.writer.close()


def main(args):

    # define publisher with suitable output filename
    # such as `Output.mp4` for saving output
    ic = image_subscriber(output_filename=rtmp_url)
    # initiate ROS node on publisher
    rospy.init_node("image_subscriber", anonymous=True)
    try:
        # run node
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        # close publisher
        ic.close()


if __name__ == "__main__":
    main(sys.argv)
