# import required libraries
from vidgear.gears import CamGear
from vidgear.gears import WriteGear
import cv2

# open any valid video stream(for e.g `foo_video.mp4` file)
stream = CamGear(source=0).start()

# add various parameters, along with custom audio
stream_params = {
    "-input_framerate": stream.framerate,  # controlled framerate for audio-video sync !!! don't forget this line !!!
    # "-i": "foo_audio.aac",  # assigns input audio-source: "foo_audio.aac"
}

rtmp_stram_params = {

    # "-input_framerate": stream.framerate,  # controlled framerate for audio-video sync !!! don't forget this line !!!
    # '-s':'480X320',
    "-f":'flv',
    "-input_framerate":30,
    # "-output_dimensions":[720,400],
    # "-fflags":'nobuffer',
    # "-flags": 'low_delay',
    # "-i": "foo_audio.aac",  # assigns input audio-source: "foo_audio.aac"
    # '-pix_fmt':'yuv420p',
    # '-preset':'ultrafast',
    # '-tune':'zerolatency'
}

rtmp_url = "rtmp://media.inference.asia/live/stream1"

# uncomment one, either write to file or rtmp stream
# writer = WriteGear(output_filename="Output.mp4", logging=True, **stream_params)
writer = WriteGear(output_filename=rtmp_url, logging=True,**rtmp_stram_params)

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # write frame to writer
    writer.write(frame)

    # Show output window
    # cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("q"):
        # break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()

# safely close writer
writer.close()
