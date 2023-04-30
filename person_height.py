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
        top_row = 200  # the top row of the depth image to use
        depth_values = depth_image[top_row, :] * depth_scale
        valid_depth_values = depth_values[depth_values != 0]  # exclude invalid depth values
        distance = np.mean(valid_depth_values)

        # convert distance from millimeters to meters and print it
        distance_m = distance / 2.0
        print(f"Person's height is {distance_m:.2f} meters.")

        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image = cv2.convertScaleAbs(depth_image, alpha=0.03)
        depth_colormap = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)
        cap = cv2.VideoCapture(0)
        cv2.imshow('Depth Image', depth_image)
        key = cv2.waitKey(1)
        
finally:
    # stop the pipeline
    pipeline.stop()
