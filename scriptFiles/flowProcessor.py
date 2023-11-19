import heapq
import json
import copy

graph_file = open('graphLinks.json', 'r')
start_graph = json.load(graph_file)
udp_graph = copy.deepcopy(start_graph)
tcp_graph = copy.deepcopy(start_graph)

# słownik przechowywujący wszystkie połączenia (potrzebne do liczenia bw później)
flows = {f's{i}':{} for i in range(1,11)}

def bw_dijkstra(type, start):
    if type == "TCP":
        graph = tcp_graph
    else:
        graph = udp_graph

    distances = {vertex: [0, [], 0] for vertex in graph}
    distances[start][0] = 0
    priority_queue = [(float('infinity'), start, 0)]

    while priority_queue:
        current_distance, current_vertex, current_delay = heapq.heappop(priority_queue)
        current_path = distances[current_vertex][1][:]
        current_path.append(current_vertex)
        if current_distance < distances[current_vertex][0]:
            continue
        for neighbor, weight, delay in graph[current_vertex]:
            distance = min(current_distance, weight)
            delay_distance = current_delay + delay
            # Aktualizacja odległości
            if distance > distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1] = current_path
                distances[neighbor][2] = delay_distance
                heapq.heappush(priority_queue, (distance, neighbor, delay_distance))
    for node, key in distances.items():
        key_copy = key[1][:]
        key_copy.append(node)
        key_copy.append(f'h{node[1:]}')
        distances[node][1] = key_copy
    return distances


def delay_dijkstra(type, start):
    if type == "TCP":
        graph = tcp_graph
    else:
        graph = udp_graph

    distances = {vertex: [float('infinity'), [], 0] for vertex in graph}
    distances[start][0] = 0
    priority_queue = [(0, start, float('infinity'))]

    while priority_queue:
        current_distance, current_vertex, current_bw = heapq.heappop(priority_queue)
        current_path = distances[current_vertex][1][:]
        current_path.append(current_vertex)
        if current_distance > distances[current_vertex][0]:
            continue
        for neighbor, bw, delay in graph[current_vertex]:
            distance = current_distance + delay
            bw_distance = min(current_bw, bw)

            # Aktualizacja odległości
            if distance < distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1] = current_path
                distances[neighbor][2] = bw_distance
                heapq.heappush(priority_queue, (distance, neighbor, bw_distance))

    for node, key in distances.items():
        key_copy = key[1][:]
        key_copy.append(node)
        key_copy.append(f'h{node[1:]}')
        distances[node][1] = key_copy
    return distances


def best_stream(src_host, dest_host, type, bw=0):
    #translating hosts to switches
    src = f's{src_host[1:]}'
    dest = f's{dest_host[1:]}'
    delay_distances = delay_dijkstra(type, src)
    delay_path = delay_distances[dest]
    if delay_path[2] >= bw:
        # zmiana indeksowania
        temp = delay_path[0]
        delay_path[0] = bw
        delay_path[2] = temp
        return delay_path
    bw_distances = bw_dijkstra(type, src)[dest]
    if bw_distances[0] >= bw:
        bw_distances[0] = bw
        return bw_distances
    return bw_distances


def update_graph(stream, type):
    if type not in ["TCP","UDP"]:
        type = "UDP"
    update_flows(stream, type)
    path = stream[1]
    ## TODO to się da w jednej pętli 100%
    # iterates through link in one way
    for i in range(len(path) - 2):
        node = path[i]
        next_node = path[i + 1]
        tcp_links = tcp_graph[node]
        udp_links = udp_graph[node]
        for link in tcp_links:
            if link[0] == next_node:
                new_tcp_bw = compute_link_bw(node,next_node,"TCP")
                link[1] = new_tcp_bw
        for link in udp_links:
            if link[0] == next_node:
                new_udp_bw = compute_link_bw(node,next_node,"UDP")
                link[1] = new_udp_bw
    back_path = path[::-1]
    # iterates through link backwards
    for i in range(1, len(back_path) - 1):
        node = path[i]
        next_node = path[i - 1]
        tcp_links = tcp_graph[node]
        udp_links = udp_graph[node]
        for link in tcp_links:
            if link[0] == next_node:
                new_tcp_bw = compute_link_bw(node,next_node,"TCP")
                link[1] = new_tcp_bw
        for link in udp_links:
            if link[0] == next_node:
                new_udp_bw = compute_link_bw(node,next_node,"UDP")
                link[1] = new_udp_bw
    #LEFT for testing purpose
    #DEBUG
    #print("tcp_graph")
    #print(tcp_graph)
    #print("udp_graph")
    #print(udp_graph)
    #END DEBUG


# Przejeżdża po strumieniu i dodaje do listy połączeń 
def update_flows(stream, type):
    bw = stream[0]
    path = stream[1]
    for i in range(len(path) - 2):
        node = path[i]
        next_node = path[i + 1]
        if next_node not in flows[node].keys():
            flows[node][next_node] = []
            flows[next_node][node] = []
        flows[node][next_node].append([type, bw])
        flows[next_node][node].append([type, bw])
def compute_flow_info(start,end):
    current_max_tcp = 0
    current_connected_tcp = 0
    udp_bandwidth_sum = 0
    sum_of_used_bandwidth = 0
    for flow in flows[start][end]:
        if flow[0] == "TCP":
            current_connected_tcp +=1
            if flow[1] > current_max_tcp:
                current_max_tcp = flow[1]
        if flow[0] == "UDP":
            udp_bandwidth_sum += flow[1]
        sum_of_used_bandwidth += flow[1]
    return current_max_tcp, current_connected_tcp, udp_bandwidth_sum, sum_of_used_bandwidth

def compute_link_bw(start,end,type):
    max_tcp_bandwidth, connected_tcp_flows, udp_bandwidth_sum, sum_of_used_bandwidth = compute_flow_info(start,end)
    original = compute_original_bw(start,end)
    if type == "UDP":
        if original - (max_tcp_bandwidth * connected_tcp_flows) - udp_bandwidth_sum < 0:
            return 0
        return original - (max_tcp_bandwidth * connected_tcp_flows) - udp_bandwidth_sum
    if type == "TCP":
        left_bandwidth = (original - udp_bandwidth_sum) / (connected_tcp_flows+1)
        if left_bandwidth >= max_tcp_bandwidth: 
            return left_bandwidth
        return 0

def compute_original_bw(start,end):
    for links in start_graph[start]:
        if links[0] == end:
            return links[1]