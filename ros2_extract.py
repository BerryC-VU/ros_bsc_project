from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
from graphviz import Digraph
import pandas as pd
# import sys

# bagfolder = sys.argv[1]
bagfolder = 'turtlesim_test/test4'
graph = Digraph()
df = pd.DataFrame()

with Reader(bagfolder) as reader: # 这个地方用的是folder name,读取的是folder里面的metadata.yaml文件
    topics = reader.topics
    print(list(topics))

    connections = [x for x in reader.connections if x.topic == '/rosout']

    if len(connections) != 0:
        print(len(connections))
        msgs = []
        nodes = []
        stamps = []
        for connection, timestamp, rawdata in reader.messages(list(connections)):
            msg = deserialize_cdr(rawdata, connection.msgtype)
            # print(msg.stamp.sec)
            stamps.append(msg.stamp.sec)
            nodes.append(msg.name)
            msgs.append(msg.msg)
            # print(msg.topics)
        if len(msgs) == 0:
            print("NO message in '/rosout'")
        else:
            data = pd.DataFrame({'timestamp': stamps, 'node': nodes, 'msg': msgs})
            df = pd.concat([df,data])
            print(df)
            df.to_csv(bagfolder + '/info.csv')
    else:
        print("THERE is no '/rosout'")


