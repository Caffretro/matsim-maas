import json
import osmnx as ox
import networkx as nx

# Load JSON data
json_data = {
    "0": [
        [521831, 11099239838, 22.5155683, 114.1311329, 7500889589,
            22.5057405, 114.128136, 0, 0, "Private Vehicle"],
        [654217, 11425075465, 22.3216222, 114.180721, 6900607523,
            22.3203108, 114.1935193, 0, 0, "Private Vehicle"],
        [1342614, 1700168338, 22.423418, 114.245282, 11469067160,
            22.328963, 114.1935065, 0, 0, "Private Vehicle"]
    ],
    "1": []
}

# Create a graph from OSM data
# For performance, you might want to use a bounding box or a predefined file
G = ox.graph_from_point((22.3193, 114.1694), dist=10000, network_type='drive')
print("Graph created.")
# Function to find nearest edge


def get_nearest_link_id(graph, point):
    nearest_edge = ox.nearest_edges(graph, point[1], point[0])
    return graph.edges[nearest_edge]['osmid']


# Process each passenger
for time, passengers in json_data.items():
    for passenger in passengers:
        origin = (passenger[2], passenger[3])
        destination = (passenger[5], passenger[6])

        origin_link_id = get_nearest_link_id(G, origin)
        destination_link_id = get_nearest_link_id(G, destination)

        print(
            f"Origin Link ID: {origin_link_id}, Destination Link ID: {destination_link_id}")
