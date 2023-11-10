#TODO: 1. aktualizacja grafu
#TODO: 2. terminal
#TODO: 3. wysyłanie onosowi


import heapq
import json

graph_file = open('graphLinks.json', 'r')
start_graph = json.load(graph_file)
tcp_graph = start_graph[:]
udp_graph = start_graph[:]

def bw_dijkstra(graph, start):
    # Inicjalizacja odległości od startowego wierzchołka do pozostałych
    distances = {vertex: [0, [], 0] for vertex in graph}
    distances[start][0] = 0

    # Kolejka priorytetowa do przechowywania wierzchołków i ich odległości
    priority_queue = [(float('infinity'), start, 0)]

    while priority_queue:
        current_distance, current_vertex, current_delay = heapq.heappop(priority_queue)
        current_path = distances[current_vertex][1][:]
        current_path.append(current_vertex)
        # Pominięcie wierzchołków, które zostały już odwiedzone
        if current_distance < distances[current_vertex][0]:
            continue

        # Iteracja po sąsiadach aktualnego wierzchołka
        for neighbor, weight, delay in graph[current_vertex]:
            distance = min(current_distance, weight)
            delay_distance = current_delay + delay
            # Aktualizacja odległości, jeśli znaleziono krótszą ścieżkę
            if distance > distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1] = current_path
                distances[neighbor][2] = delay_distance
                heapq.heappush(priority_queue, (distance, neighbor, delay_distance))
    for node,key in distances.items():
        key_copy = key[1][:]
        key_copy.append(node)
        key_copy.append(f'h{node[1]}')
        distances[node][1] = key_copy
    return distances


def delay_dijkstra(graph, start):
    # Inicjalizacja odległości od startowego wierzchołka do pozostałych
    distances = {vertex: [float('infinity'), [], 0] for vertex in graph}
    distances[start][0] = 0

    # Kolejka priorytetowa do przechowywania wierzchołków i ich odległości
    priority_queue = [(0, start, float('infinity'))]

    while priority_queue:
        current_distance, current_vertex, current_bw = heapq.heappop(priority_queue)
        current_path = distances[current_vertex][1][:]
        current_path.append(current_vertex)
        # Pominięcie wierzchołków, które zostały już odwiedzone
        if current_distance > distances[current_vertex][0]:
            continue

        # Iteracja po sąsiadach aktualnego wierzchołka
        for neighbor, bw, delay in graph[current_vertex]:
            distance = current_distance + delay
            bw_distance = min(current_bw, bw)

            # Aktualizacja odległości, jeśli znaleziono krótszą ścieżkę
            if distance < distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1] = current_path
                distances[neighbor][2] = bw_distance
                heapq.heappush(priority_queue, (distance, neighbor, bw_distance))

    for node,key in distances.items():
        key_copy = key[1][:]
        key_copy.append(node)
        key_copy.append(f'h{node[1]}')
        distances[node][1] = key_copy
    return distances


def process_stream(src,dest,type,graph,bw=0):
    delay_distances=delay_dijkstra(graph,src)
    delay_path=delay_distances[dest]
    if delay_path[2]>=bw:
        return delay_path[1]
    bw_distances = bw_dijkstra(graph,src)
    return bw_distances[dest][1]