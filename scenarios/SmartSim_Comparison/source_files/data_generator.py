import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
from datetime import timedelta


def generate_taxis(link_ids, num_taxis=1000):
    vehicles = ET.Element('vehicles')

    for i in range(1, num_taxis + 1):
        vehicle = ET.SubElement(vehicles, 'vehicle')
        vehicle.set('id', f'taxi-{i}')
        vehicle.set('start_link', random.choice(link_ids))
        vehicle.set('t_0', '0')
        vehicle.set('t_1', '86400')

    return vehicles


def write_vehicles_to_xml(vehicles, output_file):
    xml_declaration = '<?xml version="1.0" ?>\n<!DOCTYPE vehicles SYSTEM "http://matsim.org/files/dtd/dvrp_vehicles_v1.dtd">\n'
    rough_string = ET.tostring(vehicles, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml_content = reparsed.toprettyxml(indent="  ")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(xml_declaration)
        file.write(pretty_xml_content)


def generate_passengers(link_ids, num_passengers=30000, day_seconds=86400):
    population = ET.Element('population')

    for i in range(1, num_passengers + 1):
        person = ET.SubElement(population, 'person')
        person.set('id', f'{i:07d}')

        plan = ET.SubElement(person, 'plan')
        plan.set('selected', 'yes')

        start_link = random.choice(link_ids)
        end_link = random.choice(link_ids)

        # Calculate evenly distributed end_time
        end_time_seconds = ((i - 1) * day_seconds) // num_passengers
        end_time = str(timedelta(seconds=end_time_seconds))

        act1 = ET.SubElement(plan, 'act')
        act1.set('type', 'dummy')
        act1.set('link', start_link)
        act1.set('end_time', end_time)

        leg = ET.SubElement(plan, 'leg')
        leg.set('mode', 'taxi')

        act2 = ET.SubElement(plan, 'act')
        act2.set('type', 'dummy')
        act2.set('link', end_link)

    return population


def write_population_to_xml(population, output_file):
    xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v5.dtd">\n'
    rough_string = ET.tostring(population, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml_content = reparsed.toprettyxml(indent="  ")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(xml_declaration)
        file.write(pretty_xml_content)


def taxi_generator():
    taxi_num = 1000

    link_file = 'link_ids.csv'
    output_file = f'taxis-{taxi_num}.xml'

    with open(link_file, 'r') as file:
        link_ids = [line.strip() for line in file.readlines()][1:]

    vehicles = generate_taxis(link_ids)
    write_vehicles_to_xml(vehicles, output_file)

    print(f"Taxis have been written to {output_file}.")


def passenger_generator():
    passenger_num = 30000

    link_file = 'link_ids.csv'
    output_file = f'passengers-{passenger_num}.xml'

    with open(link_file, 'r') as file:
        link_ids = [line.strip() for line in file.readlines()][1:]

    population = generate_passengers(link_ids)
    write_population_to_xml(population, output_file)

    print(f"Passengers have been written to {output_file}.")


if __name__ == '__main__':
    taxi_generator()
    # passenger_generator()
