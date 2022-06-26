import graphviz
from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
from graphviz import Digraph
import rosbags
from rosbags.rosbag2 import ReaderError
import sys
import sqlite3

# # create reader instance and open for reading
# with Reader('/home/ros/rosbag_2020_03_24') as reader:
#     for connection, timestamp, rawdata in reader.messages(['/imu_raw/Imu']):
#         msg = deserialize_cdr(rawdata, connection.msgtype)
#         print(msg.header.frame_id)

# bagfolder = sys.argv[1]
bagfolder = 'ros2/rosbag2_2022_06_02-08_49_23_0'
graph = Digraph()


# with Reader(bagfolder) as reader: # 这个地方用的是folder name,读取的是folder里面的metadata.yaml文件
#     topics = reader.topics
#     print("-----------------------")
#     connections = [x for x in reader.connections if x.topic == '/amcl_pose/in_world']
#     for connection, timestamp, rawdata in reader.messages(connections=connections):
#         msg = deserialize_cdr(rawdata,connection.msgtype)
#         print(msg,'\n')

# conn = sqlite3.connect(bagfolder+'/'+'rosbag2_2022_06_02-08_49_23_0.db3')
# print("Opened database successfully")

