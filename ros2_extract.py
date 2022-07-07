# python3 ros1_extract.py path/bagfolder

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
from graphviz import Digraph
import pandas as pd
import group_topic
import sys


def read_rosout(bagfolder, reader, conns):
    msgs = []
    nodes = []
    stamps = []
    df = pd.DataFrame()

    for conn, timestamp, rawdata in reader.messages(list(conns)):
        msg = deserialize_cdr(rawdata, conn.msgtype)
        stamps.append(msg.stamp.sec)
        nodes.append(msg.name)
        msgs.append(msg.msg)
        if "Subscribing to" in msg.msg:
            print("TRUE")
    if len(msgs) == 0:
        print("NO message in '/rosout'")
    else:
        data = pd.DataFrame({'timestamp': stamps, 'node': nodes, 'msg': msgs})
        df = pd.concat([df,data])
        df.to_csv(bagfolder + '/info.csv')
    return df


def generate_topics(graph, all_topics):
    for topic in all_topics:
        if topic not in graph:
            graph.node(topic, topic, {'shape': 'rectangle'})

    group_topic.main(graph, all_topics)


# def generate_nodes(graph, all_info):
#     nodes = all_info['node'].unique()
#     for node in nodes:
#         graph.node(node, node, {'shape': 'oval'})


def generate_edges(graph, all_topics):
    for topic in all_topics:
        if topic == '/parameter_events':
            graph.edge('/parameter_events', '/_ros2cli_rosbag2')

        graph.edge('/_ros2cli_rosbag2', topic)


def create_graph(graph, topics, all_info):
    generate_topics(graph, topics)

    # generate_nodes(graph, all_info)

    # add fixed nodes
    graph.node('/_ros2cli_rosbag2', '/_ros2cli_rosbag2')

    generate_edges(graph, topics)

def main(bagfolder):
    with Reader(bagfolder) as reader:

        topics = list(reader.topics)

        # check whether '/rosout' exist since it is the only node that log information
        connections = [x for x in reader.connections if x.topic == '/rosout']

        if len(connections) != 0: # if there is information logged in '/rosout'
            all_info = read_rosout(bagfolder, reader, connections)
            # print(len(connections))
        else:
            print("THERE is no '/rosout' topic")
            sys.exit()

        graph = Digraph(name='ros2_'+bagfolder, strict=True)
        create_graph(graph, topics, all_info)

        # view graph
        graph.unflatten(stagger=5, fanout=True).view()