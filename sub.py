from graphviz import Digraph

parent_graph = Digraph(strict=True) # root graph
list_of_str = []


def extract_unique_str(list, index):
    sub = []
    for l in list:
        # only keep the unique value
        if l[index] not in sub:
            sub.append(l[index])
    return sub


def get_sub_graph_name(flow_name):
    return '{0}_{1}'.format('cluster',flow_name)


# def get_new_name(level, name):
#     return '{0}_{1}'.format(level,name)


def rec(level, parent_graph, list_n, longest_len, flow_name):
    if level < longest_len:
        print('Start of level ------- ', level)
        # unique topic of level n
        sub = extract_unique_str(list_n, level)

        for t in sub:
            print('t is ', t)
            flow_name.append(t)
            print(flow_name)
            # list that contains topic t
            list_of_t = []
            # longest len of topic in all topics in list_of_t
            longest_len = 0
            for s in list_n:
                # print(s)
                if s[level] == t:
                    list_of_t.append(s)
                    if len(s) > longest_len:
                        longest_len = len(s)
            # print(list_of_t)
            tmp_graph = Digraph()
            if len(list_of_t) > 1:
                cluster_name = '/'.join(flow_name)
                print(cluster_name)
                sub_graph_name = get_sub_graph_name(cluster_name)
                # print(sub_graph_name)
                sub_graph = Digraph(sub_graph_name, node_attr={'shape': 'rectangle'})
                sub_graph.attr(label = cluster_name)
                for topic in list_of_t:
                    topic_name = '/'.join(topic)
                    sub_graph.node(topic_name, label=topic_name)
                parent_graph.subgraph(sub_graph)
                # parent_graph = sub_graph
                tmp_graph = sub_graph
                # print(sub_graph.source)

            rec(level+1, tmp_graph, list_of_t, longest_len, flow_name)
            # print('End of current level ----- ', level)
            parent_graph.subgraph(tmp_graph)

        # if level == 1:
        #     print("POP HERE 3")
        #     flow_name.pop()

        # print(flow_name)
        print('End of current level ----- ', level)
        print("NOW BACK TO Previous level: ", level-1)

        # for i in range(level-2):
        #     flow_name.pop()
        # flow_name = flow_name[0:2]
        print("POP HERE 1")
        flow_name.pop()
        # print("TEST, ", flow_name[0:2])
        print("HEREEEE: ", flow_name)

    else:
        print("NO MORE")
        print("POP HERE 2")
        flow_name.pop()
        # print(flow_name)
        return

def main():
    # topics = ['/a/x/1', '/a/x/2', '/a/y/1', '/a/y/2', '/a/z', '/b/x/1', '/b/x/2','/c']
    topics = ['/a/x/1/m', '/a/x/1/n', '/a/x/2', '/a/y/1', '/a/y/2', '/a/z', '/b/x/1', '/b/x/2',
              '/c', '/a/x/m/2', '/b/y/1', '/b/c', '/a/a', '/d/c/c/c/c/c/c/c', '/b/ccccccccccccccccccc']


    for topic in topics:
        parent_graph.node(topic, label=topic)

    # list_of_str = []
    longest_len = 0
    for topic in topics:
        tmp = list(topic.split('/'))
        list_of_str.append(tmp)
        if len(tmp) > longest_len:
            longest_len = len(tmp)

    level = 1

    rec(level, parent_graph, list_of_str, longest_len, flow_name=[''])
    # parent_graph.subgraph(tmp_graph)
    # for topic in topics:
        # if topic not in parent_graph.node_attr
    parent_graph.unflatten(stagger=3, fanout=True).view()


if __name__ == '__main__':
    main()