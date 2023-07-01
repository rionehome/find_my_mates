import pyrealsense2 as rs
import numpy as np
import cv2
# create a pipeline object for the RealSense camera
pipeline = rs.pipeline()

# create a configuration object and enable the depth stream
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# start the pipeline and get the depth sensor's intrinsic parameters
profile = pipeline.start(config)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
intrinsics = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()

try:
    while True:
        # wait for a new frame from the camera
        frames = pipeline.wait_for_frames()

        # extract the depth frame and convert it to a numpy array
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())

        # calculate the distance between the top of the person's head and the floor
        top_row = 150  # the top row of the depth image to use
        depth_values = depth_image[top_row, :] * depth_scale
        valid_depth_values = depth_values[depth_values != 0]  # exclude invalid depth values
        distance = np.mean(valid_depth_values)

        # convert distance from millimeters to meters and print it
        distance_m = distance / 2.1
        if distance_m <= 1.4:
            print("Your height is less than 1.4m")
        elif distance_m <= 1.8:
            print("Your height is 1.4m to 1.8m")
        elif distance_m > 1.8:
            print("Your height is more than 1.8m")
        

        
        
finally:
    # stop the pipeline
    pipeline.stop()
