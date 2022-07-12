# python3 ros1_extract.py path/bagfolder

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
from graphviz import Digraph
import pandas as pd
import group_topic
import sys
import os
from datetime import datetime


def read_rosout(reader, conns):
    msgs = []
    nodes = []
    date_times = []
    stamps = []
    df = pd.DataFrame()

    for conn, timestamp, rawdata in reader.messages(list(conns)):
        msg = deserialize_cdr(rawdata, conn.msgtype)
        # print(timestamp)
        # print(msg.stamp.sec)
        # print(msg.stamp.nanosec)
        msgs.append(msg.msg)
        # _stamp = msg.stamp.sec + (msg.stamp.nanosec / 1000000000)
        # print(_stamp)
        date_times.append(datetime.fromtimestamp(msg.stamp.sec))
        nodes.append(msg.name)
        stamps.append(timestamp)
    if len(msgs) == 0:
        print("NO message in '/rosout'")
    else:
        # data = pd.DataFrame({'timestamp': stamps, 'time': times, 'node': nodes, 'msg': msgs})
        data = pd.DataFrame({'Time': stamps, 'date-time': date_times, 'node': nodes, 'msg': msgs})
        df = pd.concat([df, data], ignore_index=True)
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


def generate_edges(graph, topics):
    for topic in topics:
        if topic == '/parameter_events':
            graph.edge('/parameter_events', '/_ros2cli_rosbag2')

        graph.edge('/_ros2cli_rosbag2', topic)


def create_graph(graph, topics):
    generate_topics(graph, topics)

    # generate_nodes(graph, all_info)

    # add fixed nodes
    graph.node('/_ros2cli_rosbag2', '/_ros2cli_rosbag2')

    generate_edges(graph, topics)


def _median(values):
    values_len = len(values)
    if values_len == 0:
        return  float('nan')
    sorted_values = sorted(values)
    if values_len % 2 == 1:
        return sorted_values[int(values_len /2)]

    lower = sorted_values[int(values_len /2) -1 ]
    upper = sorted_values[int(values_len /2)]
    return float(lower+upper)/2


def label_graph(graph, topics, bagfolder):
    # label the start/end time on each topic

    # label the med_freq on the edge of each topic
    # get med_freq
    stamps = pd.read_csv(bagfolder+'/info.csv')
    stamps = stamps['Time'].tolist()
    # print(stamps)
    period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
    med_period = _median(period)
    med_freq = 1.0 / med_period

    for

def main(bagfolder):
    with Reader(bagfolder) as reader:

        topics = list(reader.topics)

        # check whether '/rosout' exist since it is the only node that log information
        connections = [x for x in reader.connections if x.topic == '/rosout']

        if len(connections) != 0:  # if there is information logged in '/rosout'
            all_info = read_rosout(reader, connections)
            if os.path.exists(bagfolder+'/info.csv'):
                os.remove(bagfolder+'/info.csv')
            all_info.to_csv(bagfolder + '/info.csv')
        else:
            print("THERE is no '/rosout' topic")
            sys.exit()

        # graph = Digraph(name='ros2_'+bagfolder, strict=True)
        graph = Digraph(directory=bagfolder+'/', name='ros2_extraction', strict=True)
        create_graph(graph, topics)
        label_graph(graph,topics,bagfolder)

        # view graph
        graph.unflatten(stagger=5, fanout=True).view()
