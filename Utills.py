import networkx as nx
import matplotlib.pyplot as plt


#@TODO graph mutiedge collapse, self edge label missing
class AccepterUtill():
    def lambda_cnt(trans):
        cnt = 0
        for key in trans.keys():
            for target in trans[key].keys():
                if target == "lambda":
                    cnt += 1
        return cnt
    
    def draw_graph(accepter):
        graph = nx.MultiDiGraph()
        for state in accepter.trans.keys():
            graph.add_node(state)
        edge_labels = {}
        for keyf in accepter.trans.keys():
            for edge in accepter.trans[keyf].keys():
                for keyt in accepter.trans[keyf][edge]:
                    graph.add_edge(keyf,keyt, label = edge)
                    if (keyf, keyt) in edge_labels.keys():
                        edge_labels[(keyf, keyt)] += f',{edge}'
                    else:
                        edge_labels[(keyf, keyt)] = edge
        color_map = []
        for node in graph:
            if node in accepter.final:
                color_map.append('red')
            else: 
                color_map.append('blue')     
        ax = plt.plot()
        pos = nx.shell_layout(graph)
        nx.draw_shell(graph, node_color = color_map,with_labels = True)
        nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels)
        plt.show()
        return



def states_to_string(states):
    if len(states)==0:
        return "none"
    ret = ""
    for state in sorted(states):
        ret += state
    return ret
def states_is_final(states,final):
    for state in states:
        if state in final:
            return True
    return False