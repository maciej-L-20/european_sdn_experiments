import heapq
import json

graph_file = open('graphLinks.json', 'r')
start_graph = json.load(graph_file)

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
    for node, key in distances.items():
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

    for node, key in distances.items():
        key_copy = key[1][:]
        key_copy.append(node)
        key_copy.append(f'h{node[1]}')
        distances[node][1] = key_copy
    return distances


def best_stream(src_host, dest_host, type, graph, bw=0):
    #translating hosts to switches
    src = f's{src_host[1:]}'
    dest = f's{dest_host[1:]}'
    delay_distances = delay_dijkstra(graph, src)
    delay_path = delay_distances[dest]
    if delay_path[2] >= bw:
        # zmiana indeksowania
        temp = delay_path[0]
        delay_path[0] = bw
        delay_path[2] = temp
        return delay_path
    bw_distances = bw_dijkstra(graph, src)[dest]
    if bw_distances[0] >= bw:
        bw_distances[0] = bw
        return bw_distances
    return bw_distances


def update_graph(stream, graph):
    bw = stream[0]
    path = stream[1]
    # iterates through link in one way
    for i in range(len(path) - 2):
        node = path[i]
        next_node = path[i + 1]
        links = graph[node]
        for link in links:
            if link[0] == next_node:
                link[1] -= bw
    back_path = path[::-1]
    # iterates through link backwards
    for i in range(1, len(back_path) - 1):
        node = path[i]
        next_node = path[i - 1]
        links = graph[node]
        for link in links:
            if link[0] == next_node:
                link[1] -= bw