from queue import Queue
import heapq

def bfs(graph, start_node, search_node=None):
    
    queue = Queue()
    queue.put(start_node)
    visited_nodes = set([start_node])
    nodes_visited_order = [start_node]
    if search_node:
        search_node_found = False
    else:
        search_node_found = None
    
    while not queue.empty():
        current_node = queue.get()
        if search_node and current_node == search_node:
            search_node_found = True
            break
        
        for neighbor in graph[current_node]:
            if neighbor not in visited_nodes:
                queue.put(neighbor)
                visited_nodes.add(neighbor)
                nodes_visited_order.append(neighbor)
    
    if search_node:
        return int(search_node_found)
    else:
        return nodes_visited_order


def dfs(graph, start_node, visited=None, path=None, search_node=None):

    
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start_node)
    path.append(start_node)

    if start_node == search_node:
        if search_node is not None:
            return 1

    for neighbor in graph[start_node]:
        if neighbor not in visited:
            result = dfs(graph, neighbor, visited, path, search_node)
            if result == 1:
                return 1

    if search_node is not None:
        return 0

    return path
    

def dijkstra(graph, start_node, end_node):

    total_distance = {}
    for node in graph:
        total_distance[node] = float('inf')
   
    total_distance[start_node] = 0
    heap = [(0, start_node)]
    
    prev_nodes = {}

    edge_count = {}
    for node in graph:
        edge_count[node] = float('inf')
    edge_count[start_node] = 0
    
    while heap:
        curr_distance, curr_node = heapq.heappop(heap)
        
        if curr_node == end_node:
            break
        
        if curr_distance > total_distance[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node].items():
            distance = curr_distance + weight
            edge = edge_count[curr_node] + 1
            if distance < total_distance[neighbor]:
                total_distance[neighbor] = distance
                edge_count[neighbor] = edge                
                prev_nodes[neighbor] = curr_node                
                heapq.heappush(heap, (distance, neighbor))
            elif distance == total_distance[neighbor] and edge < edge_count[neighbor]:
                edge_count[neighbor] = edge
                prev_nodes[neighbor] = curr_node
    
    if end_node not in prev_nodes:
        return 0
    
    path = [end_node]
    curr_node = end_node
    while curr_node != start_node:
        curr_node = prev_nodes[curr_node]
        path.append(curr_node)
    path.reverse()
    
    return [path, total_distance[end_node], edge_count[end_node]]



# (strongly connected components)
def kosaraju(graph):
    
    visited_nodes = set()
    stack = []
    components = []

    for node in graph:
        if node not in visited_nodes:
            dfs(graph, node, visited_nodes, stack)

    reversed_graph = graph_reverse(graph)

    visited_nodes.clear()
    
    while stack:
        node = stack.pop()
        if node not in visited_nodes:
            component = []
            kosaraju_dfs(node, visited_nodes, reversed_graph, component)
            components.append(component)

    return components



def kosaraju_dfs(node, visited_nodes, graph, component):
    visited_nodes.add(node)
    component.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited_nodes:
            kosaraju_dfs(neighbor, visited_nodes, graph, component)


def graph_reverse(graph):
    reversed_graph = {}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in reversed_graph:
                reversed_graph[neighbor] = {}
            reversed_graph[neighbor][node] = graph[node][neighbor]
    return reversed_graph

    
