import xml.etree.ElementTree as ET
import csv


def extract_ids_from_network(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract node and link IDs
    node_ids = [node.attrib['id']
                for node in root.find('nodes').findall('node')]
    link_ids = [link.attrib['id']
                for link in root.find('links').findall('link')]

    return node_ids, link_ids


def write_ids_to_csv(node_ids, link_ids, node_file, link_file):
    # Write node IDs to a CSV file
    with open(node_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Node ID'])
        for node_id in node_ids:
            writer.writerow([node_id])

    # Write link IDs to a CSV file
    with open(link_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link ID'])
        for link_id in link_ids:
            writer.writerow([link_id])
    print(f"Node IDs have been written to {node_file}.")
    print(f"Link IDs have been written to {link_file}.")


def extract_node_link_id():
    network_file = 'hongkong_latest.xml'  # Path to your network file
    node_file = 'node_ids.csv'
    link_file = 'link_ids.csv'

    node_ids, link_ids = extract_ids_from_network(network_file)
    write_ids_to_csv(node_ids, link_ids, node_file, link_file)


if __name__ == '__main__':

    extract_node_link_id()
