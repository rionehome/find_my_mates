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
  ArmAction.msg
  MoveAction.msg
  LidarData.msg
  RealTime.msg
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