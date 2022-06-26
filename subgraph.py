from graphviz import Digraph

# class TreeNode:
#     def __init__(self, data, depth):
#         self.data = data
#         self.depth = depth
#         self.leftChild = None
#         self.rightChild = None
# some global variable
# index = 1 # root level是0， 所有topic都至少会有index 1
graph = Digraph(strict=True) # root graph
parent_graph = graph # parent graph现在是=root

topics = ['/a/x/1', '/a/x/2', '/a/y/1', '/a/y/2', '/a/z', '/b/x/1', '/b/x/2', '/c']

for topic in topics:
    graph.node(topic, label=topic)

# def get_sub_graph_name( flow_name):
#     return '{0}_{1}'.format('cluster',flow_name)

list_of_str = []
longest_list = 0
# print(list(('/a/x/1').split('/')))

for topic in topics:
    tmp = list(topic.split('/'))
    list_of_str.append(tmp)

# print(list_of_topics_str)
# [['', 'a', 'x', '1'], ['', 'a', 'x', '2'], ['', 'a', 'y', '1'],
#  ['', 'a', 'y'], ['', 'a', 'z'], ['', 'b', 'x', '1'], ['', 'b', 'x', '2'], ['', 'c']]


def extract_path(list, index):
    sub = []
    for l in list:
        # only keep the unique value
        if l[index] not in sub:
            sub.append(l[index])
    return sub

# level 1 topic
# sub_1 = extract_path(list_of_str, 1)
sub_1 = ['a']
# print(sub_1)
# ['a', 'b', 'c']
# print('/'.join(list_of_str[0]))
# /a/x/1

# each element in sub_1 is a topic, others are subtopics
for t in sub_1:
    level = 1 # root level是0， 所有topic都至少会有index 1

    # list that contains topic t
    list_of_t = []
    # longest len of topic in all topics in list_of_t
    longest_len = 0
    for s in list_of_str:
        # print(longest_len)
        if s[level] == t:
            list_of_t.append(s)
            if len(s) > longest_len:
                longest_len = len(s)
    print(list_of_t)
    print(longest_len)

    # create 1st subgraph
    sub_graph = Digraph('{0}_{1}'.format('cluster',t), node_attr={'shape': 'rectangle'})
    sub_graph.attr(label = t)
    for topic in list_of_t:
        topic_name = '/'.join(topic)
        sub_graph.node(topic_name, label=topic_name)
    parent_graph.subgraph(sub_graph)
    parent_graph = sub_graph
    level += 1

    while level < longest_len:
        print('level ----------------' , level)
        new_list = []
        for t in list_of_t:
            if len(t) > level:
                new_list.append(t)
        print(new_list)

        # get a list of unique subtopics with index i
        if len(new_list) != 0:
            t_list = extract_path(new_list, level)
            print(t_list)
        print('end of level ----------' , level)

        # generate subgraph
        # sub_graph = Digraph('{0}_{1}'.format('cluster',t), node_attr={'shape': 'rectangle'})
        # sub_graph_1.attr(label = t)
        # for topic in list_of_t:
        #     topic_name = '/'.join(topic)
        #     sub_graph_1.node(topic_name, label=topic_name)
        # graph.subgraph(sub_graph_1)
        # old_graph = sub_graph_1

        # connect with old graph

        level += 1

# graph.unflatten(stagger=3, fanout=True).view()
def main():
    level = 0


if __name__ == "__main__":
    main()