from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
from graphviz import Digraph
import pandas as pd
import group_topic
import os
import sys
from datetime import datetime


def get_file_path(bagfolder, topic):
    return bagfolder + "/" + topic.replace("/", "-")[1:] + ".csv"


def get_msg_and_info(reader, connections, topic):
    stamps = []
    df = pd.DataFrame()
    # if topic == '/rosout':
    #     msgs = []
    #     date_times = []
    #     nodes = []
    #     for conn, timestamp, rawdata in reader.messages(list(connections)):
    #         msg = deserialize_cdr(rawdata, conn.msgtype)
    #         msgs.append(msg.msg)
    #         date_times.append(datetime.fromtimestamp(msg.stamp.sec))
    #         nodes.append(msg.name)
    #         stamps.append(timestamp * (10 ** -9))
    #
    #     data = pd.DataFrame({'Stamps': stamps, 'Date-Time': date_times, 'Node': nodes, 'Msg': msgs})
    #
    # else:
    for conn, timestamp, rawdata in reader.messages(list(connections)):
        stamps.append(timestamp * (10 ** -9))
    data = pd.DataFrame({'Stamps': stamps})
    df = pd.concat([df, data], ignore_index=True)
    return df


def generate_topics(bagfolder, graph, topics):
    for topic in topics:
        if topic not in graph:
            tmp = pd.read_csv(get_file_path(bagfolder, topic))
            stamps = tmp['Stamps'].tolist()
            period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
            med_period = _median(period)
            med_freq = round((1.0 / med_period), 2)
            if str(med_freq) != 'nan':
                graph.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq)+'Hz'))
            else:
                graph.node(topic, topic, {'shape': 'rectangle'}, xlabel=(str(med_freq)))
    group_topic.main(graph, topics)


def _median(values):
    values_len = len(values)
    if values_len == 0:
        return float('nan')
    sorted_values = sorted(values)
    if values_len % 2 == 1:
        return sorted_values[int(values_len / 2)]

    lower = sorted_values[int(values_len / 2) - 1]
    upper = sorted_values[int(values_len / 2)]
    return float(lower+upper) / 2


def generate_edges(graph, topics):
    for topic in topics:
        graph.edge('/_ros2cli_rosbag2', topic)


def create_graph(bagfolder, graph, topics):
    generate_topics(bagfolder, graph, topics)
    # generate_nodes(graph, all_info)

    # add fixed nodes
    graph.node('/_ros2cli_rosbag2', '/_ros2cli_rosbag2')

    generate_edges(graph, topics)


def get_freq(stamps):
    period = [s1 - s0 for s1, s0 in zip(stamps[1:], stamps[:-1])]
    med_period = _median(period)
    med_freq = round((1.0 / med_period), 2)
    return med_freq


def main(bagfolder, start_t, end_t):
    with Reader(bagfolder) as reader:
        # if '/rosout' not in topics:
        #     print("THERE is no '/rosout' topic")
        #     sys.exit()

        all_info = pd.DataFrame()
        for topic in list(reader.topics):
            connections = [x for x in reader.connections if x.topic == topic]
            topic_info = get_msg_and_info(reader, connections, topic)
            data = pd.DataFrame({'topics': topic,
                                 'start-time': topic_info['Stamps'].head(1).values,
                                 'end-time': topic_info['Stamps'].tail(1).values,
                                 'frequency': get_freq(topic_info['Stamps'].tolist())})

            all_info = pd.concat([all_info, data], ignore_index=True)

            file_path = get_file_path(bagfolder, topic)
            if os.path.exists(file_path):
                os.remove(file_path)
            topic_info.to_csv(file_path)
        all_info.to_csv(bagfolder + '/' + 'info.csv')

        graph = Digraph(directory=bagfolder+'/', name='ros2_extraction', strict=True)
        graph.graph_attr["rankdir"] = "LR"

        if start_t == reader.start_time and end_t == reader.end_time:
            topics = list(reader.topics)
        else:
            topics = []
            for topic in list(reader.topics):
                topic_data = all_info.loc[all_info['topics'] == topic]
                if not topic_data.empty:
                    # (10 ** 9) -> convert timestamp(sec) to timestamp(nanosec) to making comparsion with user input
                    # print("-------------------------")
                    # print(topic_data['start-time'].values[0])
                    # print(start_t)
                    # print(end_t)
                    if start_t < topic_data['start-time'].values[0] < end_t:
                        print(True)
                        topics.append(topic)

        create_graph(bagfolder, graph, topics)

        # view graph
        graph.unflatten(stagger=5, fanout=True).view()
