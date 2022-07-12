from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
from graphviz import Digraph
import pandas as pd
import group_topic
import sys
import os
from datetime import datetime


def get_file_path(bagfolder, topic):
    return bagfolder + "/" + topic.replace("/", "-") + ".csv"


def read_rosout(reader, connections):
    msgs = []
    date_times = []
    nodes = []
    stamps = []

    df = pd.DataFrame()

    for conn, timestamp, rawdata in reader.messages(list(connections)):
        msg = deserialize_cdr(rawdata, conn.msgtype)
        msgs.append(msg.msg)
        date_times.append(datetime.fromtimestamp(msg.stamp.sec))
        nodes.append(msg.name)
        stamps.append(timestamp * (10 ** -9))

    data = pd.DataFrame({'Stamps': stamps, 'Date-Time': date_times, 'Node': nodes, 'Msg': msgs})
    df = pd.concat([df, data], ignore_index=True)
    return df


def get_msg_and_info(reader, connections):
    stamps = []
    df = pd.DataFrame()
    for conn, timestamp, rawdata in reader.messages(list(connections)):
        stamps.append(timestamp * (10 ** -9))
    data = pd.DataFrame({'Stamps': stamps})
    df = pd.concat([df, data], ignore_index=True)
    return df


def generate_topics(bagfolder,graph, topics):
    for topic in topics:
        if topic not in graph:
            tmp = pd.read_csv(get_file_path(bagfolder,topic))
            stamps = tmp['Stamps'].tolist()
            period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
            med_period = _median(period)
            med_freq = round((1.0 / med_period),2)
            graph.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq)+'Hz'))
    group_topic.main(graph, topics)


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


def generate_edges(graph, topics):
    for topic in topics:
        graph.edge('/_ros2cli_rosbag2', topic)


def create_graph(bagfolder, graph, topics):
    generate_topics(bagfolder, graph, topics)
    # generate_nodes(graph, all_info)

    # add fixed nodes
    graph.node('/_ros2cli_rosbag2', '/_ros2cli_rosbag2')

    generate_edges(graph, topics)


def main(bagfolder):
    with Reader(bagfolder) as reader:

        topics = list(reader.topics)

        if '/rosout' not in topics:
            print("THERE is no '/rosout' topic")
            sys.exit()

        for topic in topics:
            connections = [x for x in reader.connections if x.topic == topic]
            if topic == '/rosout':
                data = read_rosout(reader, connections)
            else:
                data = get_msg_and_info(reader, connections)

            file_path = get_file_path(bagfolder, topic)
            if os.path.exists(file_path):
                os.remove(file_path)
            data.to_csv(file_path)

        graph = Digraph(directory=bagfolder+'/', name='ros2_extraction', strict=True)
        create_graph(bagfolder, graph, topics)

        # view graph
        graph.unflatten(stagger=5, fanout=True).view()

