cmake_minimum_required(VERSION 3.0.2)
project(find_my_mates)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

add_service_files(
  FILES
  isMeaning.srv
  MoveArm.srv
  SpeechToText.srv
)

add_message_files(
  FILES
  Feature.msg
  ImgData.msg
# Info.msg
  LidarData.msg
  OdomData.msg
  RealTime.msg
)

add_service_files(
  FILES
  Camera_msg.srv
  MoveArm.srv
  OdomMove.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime
)

include_directories(
# include
# ${catkin_INCLUDE_DIRS}
)