import xml.etree.ElementTree as ET
from geopy.distance import geodesic

# Function to parse XML from a file


def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()


# Parse the XML file
file_path = "../hongkong_latest.xml"  # Replace with your file path
root = parse_xml(file_path)
# Extract nodes
nodes = {}
for node in root.find('nodes'):
    node_id = node.attrib['id']
    # Correctly assign latitude and longitude
    lat = float(node.attrib['y'])
    lng = float(node.attrib['x'])
    nodes[node_id] = (lat, lng)

print(nodes)
# Process links and calculate midpoints
links_with_midpoints = []
for link in root.find('links'):
    from_node = link.attrib['from']
    to_node = link.attrib['to']

    if from_node in nodes and to_node in nodes:
        from_coords = nodes[from_node]
        to_coords = nodes[to_node]

        mid_lat = (from_coords[0] + to_coords[0]) / 2
        mid_lng = (from_coords[1] + to_coords[1]) / 2

        links_with_midpoints.append({
            'link_id': link.attrib['id'],
            'midpoint': (mid_lat, mid_lng)
        })

# Function to find the nearest link to a given point


def find_nearest_link(lat, lng, links):
    min_distance = float('inf')
    nearest_link = None

    for link in links:
        midpoint = link['midpoint']
        distance = geodesic((lat, lng), midpoint).meters
        if distance < min_distance:
            min_distance = distance
            nearest_link = link

    return nearest_link


# Example usage
input_lat = 22.338  # Example latitude
input_lng = 114.143  # Example longitude
nearest_link = find_nearest_link(input_lat, input_lng, links_with_midpoints)

if nearest_link:
    print(f"Nearest link ID: {nearest_link['link_id']}")
    print(f"Midpoint: {nearest_link['midpoint']}")
else:
    print("No nearest link found.")
