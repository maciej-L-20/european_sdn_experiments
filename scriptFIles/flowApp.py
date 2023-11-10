#TODO: 1. Reprezentacja grafu
#TODO: 2. Coś co wczytuje rządania
#TODO: 3. Przetwarzanie rządań

import heapq
import json

def dijkstra(graph, start):
    # Inicjalizacja odległości od startowego wierzchołka do pozostałych
    distances = {vertex: [float('infinity'),[]] for vertex in graph}
    distances[start][0] = 0

    # Kolejka priorytetowa do przechowywania wierzchołków i ich odległości
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        current_path = distances[current_vertex][1][:]
        current_path.append(current_vertex)
        # Pominięcie wierzchołków, które zostały już odwiedzone
        if current_distance > distances[current_vertex][0]:
            continue

        # Iteracja po sąsiadach aktualnego wierzchołka
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            # Aktualizacja odległości, jeśli znaleziono krótszą ścieżkę
            if distance < distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1] = current_path
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances

def delay_dijkstra(graph,start):
    for node_links  in graph.values():
        for link in node_links:
            link.pop(1)
    return dijkstra(graph,start)


graph_file = open('graphLinks.json','r')

# Przykładowy graf
graph = json.load(graph_file)
# Wierzchołek początkowy
start_vertex = "s1"


shortest_paths = delay_dijkstra(graph, start_vertex)

for vertex, distance in shortest_paths.items():
    print(f"Najkrótsza ścieżka od {start_vertex} do {vertex} wynosi {distance}")
