import json

import flowProcessor
import flowToOnos
import prep

graph_links_file = open('graphLinks.json', 'r')
graph_links = json.load(graph_links_file)
cities = prep.read_cities()

onos_ip_message = "Enter the onos controller IP."
ask_message = "Enter the flow data: source city (or host), destination city (or host), connection type (TCP, UDP, two-way), required bandwidth."
best_flow_message = "Best possible flow is: {}, with bandwidth {} Mbps and delay {} ms."
accept_message = "Type Y if you want to accept this flow or N if not."
next_flow_message = "Type anything if you want to enter next flow or 0 to exit."
sent_to_onos_message = "Flow processed and sent to Onos."
flow_canceled_message = "Flow declined"


def to_host_name(city_name):
    if (city_name[0] == 'h') & (city_name[1:].isdigit()):
        return city_name
    city_index = cities[city_name].index
    return f'h{city_index}'


def legible_path(path):
    path_str = ""
    for i in range(len(path) - 2):
        index = int(path[i][1:])
        city_name = find_city_by_index(index)
        path_str += f'{city_name} => '
    last_name = find_city_by_index(int(path[len(path) - 2][1:]))
    path_str += last_name
    return path_str


def find_city_by_index(index):
    for city_name, city in cities.items():
        if city.index == index:
            return city_name
    return f'City with index {index} not found'


def input_text_to_stream(input_text):
    flow_data = input_text.split(' ')
    flow_data[0] = to_host_name(flow_data[0])
    flow_data[1] = to_host_name(flow_data[1])
    if len(flow_data) < 4:
        flow_data.append(0)
    return flow_data


def main():
    print(onos_ip_message)
    onos_ip = input()
    while (True):
        print(ask_message)
        flow_data = input_text_to_stream(input())
        best_flow = flowProcessor.best_stream(src_host=flow_data[0], dest_host=flow_data[1], type=flow_data[2],
                                              bw=int(flow_data[3]), graph=graph_links)
        best_bw, best_path, best_delay = best_flow
        print(best_flow_message.format(legible_path(best_path), best_bw, best_delay))
        print(accept_message)
        accept_response = input()
        if accept_response == 'Y':
            flowToOnos.post_flow(best_path,flow_data[2],onos_ip)
            flowProcessor.update_graph(best_flow,graph_links)
            print(sent_to_onos_message)
        elif accept_response == 'N':
            print(flow_canceled_message)
        print(next_flow_message)
        if input() == '0': break


if __name__ == '__main__':
    main()
