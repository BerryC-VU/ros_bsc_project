# python3 ros1_extract.py path/bagfile

import group_topic
import pandas as pd
import sys
import ast
from bagpy import bagreader
from graphviz import Digraph
from rosbag import ROSBagException


def read_rosout(b, bagname):
    csvfiles = []
    data = b.message_by_topic('/rosout')
    csvfiles.append(data)

    rosout = pd.read_csv(bagname + '/rosout.csv')
    all_info = rosout[['name', 'msg', 'topics']]
    return all_info


def generate_topics(graph, all_topics):
    for topic in all_topics:
        if topic not in graph:
            graph.node(topic, topic, {'shape': 'rectangle'})

    group_topic.main(graph, all_topics)


def generate_edges(graph, all_info):
    nodes = all_info['name'].unique()
    # merge subscribers for each node
    edge_info = pd.DataFrame(data={'name': nodes}, columns=['name', 'topics'])
    for i in range(len(nodes)):
        list_of_topics = []
        for j in range(len(all_info)):
            # merge topics with the same node name
            # print(all_info['name'][j])
            if all_info['name'][j] == nodes[i]:
                # evaluate string as list and merge them into one list
                list_of_topics += ast.literal_eval(all_info['topics'][j])
        # keep the unique value in the list of topics
        edge_info['topics'][i] = list(set(list_of_topics))

    # relationship contained in 'topics'
    for i in range(len(nodes)):
        publisher = nodes[i]
        for j in range(len(edge_info['topics'][i])):
            subscriber = edge_info['topics'][i][j]
            graph.edge(publisher, subscriber)

    # relationship contained in 'msg'
    substring = "Subscribing to "
    valid_msg = all_info['msg'].dropna()
    for i in range(len(valid_msg)):
        if substring in valid_msg.iloc[i]:
            publisher = valid_msg.iloc[i].split(substring)[1]
            subscriber = all_info['name'].iloc[i]
            graph.edge(publisher, subscriber)


def generate_nodes(graph, all_info):
    nodes = all_info['name'].unique()
    for node in nodes:
        graph.node(node, node, {'shape': 'oval'})


def create_graph(topics, all_info, graph):
    generate_topics(graph, topics)
    generate_nodes(graph, all_info)
    generate_edges(graph, all_info)

    # add fixed node and edges
    graph.node("/fixed node", "/rosout", {'shape': 'oval'})
    graph.edge("/rosout", "/fixed node")
    graph.edge("/fixed node", "/rosout_agg")


def main(bagfile):
    # bagfile = sys.argv[1]
    bagname = bagfile.replace('.bag', '')

    while True:
        try:
            b = bagreader(bagfile)
            break
        except ROSBagException as err:
            print("ERROR: ", err)
            sys.exit()

    if '/rosout' in b.topics:
        print("TRUE")
        all_info = read_rosout(b, bagname)
        if len(all_info) == 0:
            print("NO message in '/rosout'")
            sys.exit()
    else:
        print("THERE is no '/rosout' topic")
        sys.exit()

    graph = Digraph(directory=bagfile+'/', name='ros1_extraction', strict=True)
    create_graph(b.topics, all_info, graph)

    # view graph
    graph.unflatten(stagger=3, fanout=True).view()

